#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jendela Utama MCP Ngobrol (Versi Refaktor)
==========================================

Jendela utama yang disederhanakan, fokus pada tanggung jawab utama: manajemen jendela dan koordinasi berbagai komponen untuk ngobrol interaktif dengan AI.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QPushButton, QMessageBox, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut

from .config_manager import ConfigManager
from .tab_manager import TabManager
from ..utils import apply_widget_styles
from ...i18n import t, get_i18n_manager
from ...debug import gui_debug_log as debug_log


class FeedbackWindow(QMainWindow):
    """Jendela utama MCP Ngobrol untuk ngobrol interaktif dengan AI"""
    language_changed = Signal()
    timeout_occurred = Signal()  # Sinyal timeout terjadi

    def __init__(self, project_dir: str, summary: str, timeout_seconds: int = None):
        super().__init__()
        self.project_dir = project_dir
        self.summary = summary
        self.result = None
        self.i18n = get_i18n_manager()
        self.mcp_timeout_seconds = timeout_seconds  # Waktu timeout yang diteruskan MCP

        # Inisialisasi komponen
        self.config_manager = ConfigManager()

        # Muat pengaturan bahasa yang disimpan
        saved_language = self.config_manager.get_language()
        if saved_language:
            self.i18n.set_language(saved_language)

        self.combined_mode = self.config_manager.get_layout_mode()
        self.layout_orientation = self.config_manager.get_layout_orientation()

        # Set timer debounce untuk menyimpan status jendela
        self._save_timer = QTimer()
        self._save_timer.setSingleShot(True)
        self._save_timer.timeout.connect(self._delayed_save_window_position)
        self._save_delay = 500  # Delay 500ms, menghindari penyimpanan yang terlalu sering

        # Setup UI
        self._setup_ui()
        self._setup_shortcuts()
        self._connect_signals()

        debug_log("Inisialisasi jendela utama selesai")

        # Jika timeout diaktifkan, otomatis mulai countdown
        self.start_timeout_if_enabled()

        # Set timer untuk auto focus ke input box setelah jendela ditampilkan (jika diaktifkan)
        if self.config_manager.get_auto_focus_enabled():
            self._focus_timer = QTimer()
            self._focus_timer.setSingleShot(True)
            self._focus_timer.timeout.connect(self._auto_focus_input)
            self._focus_timer.start(300)  # Delay 300ms memastikan jendela dan elemen UI sepenuhnya dimuat
        else:
            debug_log("Auto focus dinonaktifkan")

    def _setup_ui(self) -> None:
        """Setup antarmuka pengguna dengan desain yang lebih modern"""
        self.setWindowTitle(t('app.title'))
        self.setMinimumSize(800, 600)  # Ukuran minimum yang lebih lebar
        self.resize(1400, 900)  # Ukuran default yang lebih lebar dan nyaman

        # Posisi jendela cerdas
        self._apply_window_positioning()

        # Widget pusat dengan container untuk membatasi lebar maksimal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout wrapper untuk centering dan max width
        wrapper_layout = QHBoxLayout(central_widget)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)

        # Container utama dengan lebar maksimal yang lebih lebar
        main_container = QWidget()
        main_container.setMaximumWidth(1600)  # Lebar maksimal yang lebih besar
        main_container.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
            }
        """)

        # Layout utama dengan spacing yang lebih baik
        main_layout = QVBoxLayout(main_container)
        main_layout.setSpacing(16)  # Spacing yang lebih besar
        main_layout.setContentsMargins(32, 24, 32, 24)  # Padding yang lebih besar

        # Tambahkan container ke wrapper dengan centering
        wrapper_layout.addStretch()
        wrapper_layout.addWidget(main_container)
        wrapper_layout.addStretch()

        # Informasi header direktori proyek atas
        self._create_project_header(main_layout)

        # Area tab
        self._create_tab_area(main_layout)

        # Tombol aksi
        self._create_action_buttons(main_layout)

        # Terapkan tema gelap
        self._apply_dark_style()

    def _create_project_header(self, layout: QVBoxLayout) -> None:
        """Buat header proyek dengan desain yang lebih clean"""
        # Container header dengan background dan padding
        header_container = QWidget()
        header_container.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 8px;
            }
        """)

        # Layout horizontal untuk header
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(16, 12, 16, 12)
        header_layout.setSpacing(16)

        # Project info dengan icon
        project_info_layout = QVBoxLayout()
        project_info_layout.setSpacing(4)

        # Title
        title_label = QLabel("📁 " + t('app.projectDirectory'))
        title_label.setStyleSheet("""
            color: #ffffff;
            font-size: 13px;
            font-weight: bold;
            margin: 0;
        """)
        project_info_layout.addWidget(title_label)

        # Path
        self.project_label = QLabel(self.project_dir)
        self.project_label.setStyleSheet("""
            color: #b0b0b0;
            font-size: 11px;
            font-family: 'Consolas', 'Monaco', monospace;
            margin: 0;
        """)
        self.project_label.setWordWrap(True)
        project_info_layout.addWidget(self.project_label)

        header_layout.addLayout(project_info_layout)
        header_layout.addStretch()

        # Countdown display
        self._create_countdown_display(header_layout)

        layout.addWidget(header_container)

    def _create_countdown_display(self, layout: QHBoxLayout) -> None:
        """創建倒數計時器顯示組件（僅顯示）"""
        # 倒數計時器標籤
        self.countdown_label = QLabel(t('timeout.remaining'))
        self.countdown_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        self.countdown_label.setVisible(False)  # 預設隱藏
        layout.addWidget(self.countdown_label)

        # 倒數計時器顯示
        self.countdown_display = QLabel("--:--")
        self.countdown_display.setStyleSheet("""
            color: #ffa500;
            font-size: 14px;
            font-weight: bold;
            font-family: 'Consolas', 'Monaco', monospace;
            min-width: 50px;
            margin-left: 8px;
        """)
        self.countdown_display.setVisible(False)  # 預設隱藏
        layout.addWidget(self.countdown_display)

        # 初始化超時控制邏輯
        self._init_timeout_logic()

    def _init_timeout_logic(self) -> None:
        """初始化超時控制邏輯"""
        # 載入保存的超時設置
        timeout_enabled, timeout_duration = self.config_manager.get_timeout_settings()

        # 如果有 MCP 超時參數，且用戶設置的時間大於 MCP 時間，則使用 MCP 時間
        if self.mcp_timeout_seconds is not None:
            if timeout_duration > self.mcp_timeout_seconds:
                timeout_duration = self.mcp_timeout_seconds
                debug_log(f"用戶設置的超時時間 ({timeout_duration}s) 大於 MCP 超時時間 ({self.mcp_timeout_seconds}s)，使用 MCP 時間")

        # 保存超時設置
        self.timeout_enabled = timeout_enabled
        self.timeout_duration = timeout_duration
        self.remaining_seconds = 0

        # 創建計時器
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self._update_countdown)

        # 更新顯示狀態
        self._update_countdown_visibility()



    def _create_tab_area(self, layout: QVBoxLayout) -> None:
        """Buat area tab dengan desain modern dan responsive"""
        # Container untuk tab area
        tab_container = QWidget()
        tab_container.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 8px;
            }
        """)

        tab_container_layout = QVBoxLayout(tab_container)
        tab_container_layout.setContentsMargins(0, 0, 0, 0)
        tab_container_layout.setSpacing(0)

        # Scroll area dengan styling yang lebih modern
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setMinimumHeight(300)  # Tinggi minimum yang lebih reasonable
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                border-radius: 8px;
                background-color: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
            QScrollArea QScrollBar:vertical {
                background-color: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollArea QScrollBar::handle:vertical {
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                min-height: 30px;
                margin: 1px;
            }
            QScrollArea QScrollBar::handle:vertical:hover {
                background-color: rgba(255, 255, 255, 0.5);
            }
            QScrollArea QScrollBar::handle:vertical:pressed {
                background-color: rgba(0, 122, 204, 0.8);
            }
            QScrollArea QScrollBar::add-line:vertical,
            QScrollArea QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollArea QScrollBar:horizontal {
                background-color: rgba(255, 255, 255, 0.1);
                height: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollArea QScrollBar::handle:horizontal {
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                min-width: 30px;
                margin: 1px;
            }
            QScrollArea QScrollBar::handle:horizontal:hover {
                background-color: rgba(255, 255, 255, 0.5);
            }
            QScrollArea QScrollBar::handle:horizontal:pressed {
                background-color: rgba(0, 122, 204, 0.8);
            }
            QScrollArea QScrollBar::add-line:horizontal,
            QScrollArea QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                width: 0px;
            }
        """)

        # Tab widget dengan styling modern
        self.tab_widget = QTabWidget()
        self.tab_widget.setMinimumHeight(300)
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Inisialisasi tab manager
        self.tab_manager = TabManager(
            self.tab_widget,
            self.project_dir,
            self.summary,
            self.combined_mode,
            self.layout_orientation
        )

        # Buat tabs
        self.tab_manager.create_tabs()
        self.tab_manager.connect_signals(self)

        # Masukkan tab widget ke scroll area
        scroll_area.setWidget(self.tab_widget)
        tab_container_layout.addWidget(scroll_area)

        # Tambahkan container ke layout utama
        layout.addWidget(tab_container, 1)

    def _create_action_buttons(self, layout: QVBoxLayout) -> None:
        """Buat tombol aksi dengan desain modern"""
        # Container untuk buttons dengan background
        button_container = QWidget()
        button_container.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 16px;
                margin-top: 8px;
            }
        """)

        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(16, 16, 16, 16)
        button_layout.setSpacing(12)

        # Spacer kiri
        button_layout.addStretch()

        # Cancel button dengan styling modern
        self.cancel_button = QPushButton("✕ " + t('buttons.cancel'))
        self.cancel_button.clicked.connect(self._cancel_feedback)
        self.cancel_button.setFixedSize(140, 44)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #606060;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #505050;
                border-color: #707070;
            }
            QPushButton:pressed {
                background-color: #353535;
            }
        """)
        button_layout.addWidget(self.cancel_button)

        # Submit button dengan styling modern
        self.submit_button = QPushButton("✓ " + t('buttons.submit'))
        self.submit_button.clicked.connect(self._submit_feedback)
        self.submit_button.setFixedSize(160, 44)
        self.submit_button.setDefault(True)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: #ffffff;
                border: 1px solid #005a9e;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1e88e5;
                border-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QPushButton:default {
                border: 2px solid #42a5f5;
            }
        """)
        button_layout.addWidget(self.submit_button)

        layout.addWidget(button_container)

    def _setup_shortcuts(self) -> None:
        """Setup keyboard shortcuts"""
        # Ctrl+Enter (main keyboard) kirim pesan
        submit_shortcut_main = QShortcut(QKeySequence("Ctrl+Return"), self)
        submit_shortcut_main.activated.connect(self._submit_feedback)

        # Ctrl+Enter (numpad) kirim pesan
        submit_shortcut_keypad = QShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Enter), self)
        submit_shortcut_keypad.activated.connect(self._submit_feedback)

        # macOS support Cmd+Return (main keyboard)
        submit_shortcut_mac_main = QShortcut(QKeySequence("Meta+Return"), self)
        submit_shortcut_mac_main.activated.connect(self._submit_feedback)

        # macOS support Cmd+Enter (numpad)
        submit_shortcut_mac_keypad = QShortcut(QKeySequence(Qt.Modifier.META | Qt.Key.Key_Enter), self)
        submit_shortcut_mac_keypad.activated.connect(self._submit_feedback)

        # Escape batalkan ngobrol
        cancel_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        cancel_shortcut.activated.connect(self._cancel_feedback)

    def _connect_signals(self) -> None:
        """連接信號"""
        # 連接語言變更信號
        self.language_changed.connect(self._refresh_ui_texts)

        # 連接分頁管理器的信號
        self.tab_manager.connect_signals(self)

    def _apply_dark_style(self) -> None:
        """Terapkan tema gelap modern"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #1a1a1a, stop: 1 #2b2b2b);
                color: #ffffff;
            }
            QGroupBox {
                font-weight: 600;
                border: 2px solid #404040;
                border-radius: 10px;
                margin-top: 12px;
                padding: 16px;
                background-color: rgba(255, 255, 255, 0.02);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px 0 8px;
                color: #ffffff;
                font-size: 13px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 12px;
                color: #ffffff;
                font-size: 13px;
                line-height: 1.4;
                selection-background-color: #007acc;
            }
            QTextEdit:focus {
                border-color: #007acc;
                background-color: #252525;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 10px 12px;
                color: #ffffff;
                font-size: 13px;
                selection-background-color: #007acc;
            }
            QLineEdit:focus {
                border-color: #007acc;
                background-color: #252525;
            }
            QTabWidget::pane {
                border: 1px solid #404040;
                border-radius: 8px;
                background-color: #2b2b2b;
                margin-top: -1px;
            }
            QTabBar::tab {
                background-color: #1e1e1e;
                color: #b0b0b0;
                border: 1px solid #404040;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 12px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #007acc;
                color: #ffffff;
                border-bottom-color: #007acc;
            }
            QTabBar::tab:hover:!selected {
                background-color: #353535;
                color: #ffffff;
            }
            QSplitter {
                background-color: transparent;
            }
            QSplitter::handle {
                background-color: #404040;
                border: none;
                border-radius: 4px;
                margin: 2px;
            }
            QSplitter::handle:horizontal {
                width: 8px;
                background-color: #404040;
                border-radius: 4px;
                margin: 2px;
            }
            QSplitter::handle:vertical {
                height: 8px;
                background-color: #404040;
                border-radius: 4px;
                margin: 2px;
            }
            QSplitter::handle:hover {
                background-color: #606060;
            }
            QSplitter::handle:pressed {
                background-color: #007acc;
            }
            /* Scrollbar styling untuk consistency */
            QScrollBar:vertical {
                background-color: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                min-height: 30px;
                margin: 1px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(255, 255, 255, 0.5);
            }
            QScrollBar::handle:vertical:pressed {
                background-color: rgba(0, 122, 204, 0.8);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
        """)

    def _on_layout_change_requested(self, combined_mode: bool, orientation: str) -> None:
        """處理佈局變更請求（模式和方向同時變更）"""
        try:
            # 保存當前內容
            current_data = self.tab_manager.get_feedback_data()

            # 記住當前分頁索引
            current_tab_index = self.tab_widget.currentIndex()

            # 保存新設置
            self.combined_mode = combined_mode
            self.layout_orientation = orientation
            self.config_manager.set_layout_mode(combined_mode)
            self.config_manager.set_layout_orientation(orientation)

            # 重新創建分頁
            self.tab_manager.set_layout_mode(combined_mode)
            self.tab_manager.set_layout_orientation(orientation)
            self.tab_manager.create_tabs()

            # 恢復內容
            self.tab_manager.restore_content(
                current_data["interactive_feedback"],
                current_data["command_logs"],
                current_data["images"]
            )

            # 重新連接信號
            self.tab_manager.connect_signals(self)

            # 刷新UI文字
            self._refresh_ui_texts()

            # 恢復到設定頁面（通常是倒數第二個分頁）
            if self.combined_mode:
                # 合併模式：回饋、命令、設置、關於
                settings_tab_index = 2
            else:
                # 分離模式：回饋、摘要、命令、設置、關於
                settings_tab_index = 3

            # 確保索引在有效範圍內
            if settings_tab_index < self.tab_widget.count():
                self.tab_widget.setCurrentIndex(settings_tab_index)

            mode_text = "合併模式" if combined_mode else "分離模式"
            orientation_text = "（水平布局）" if orientation == "horizontal" else "（垂直布局）"
            if combined_mode:
                mode_text += orientation_text
            debug_log(f"佈局已切換到: {mode_text}")

        except Exception as e:
            debug_log(f"佈局變更失敗: {e}")
            QMessageBox.warning(self, t('errors.title'), t('errors.interfaceReloadError', error=str(e)))



    def _on_reset_settings_requested(self) -> None:
        """處理重置設定請求"""
        try:
            # 重置配置管理器的所有設定
            self.config_manager.reset_settings()

            # 重置應用程式狀態
            self.combined_mode = False  # 重置為分離模式
            self.layout_orientation = 'vertical'  # 重置為垂直布局

            # Reset bahasa ke Bahasa Indonesia sebagai default
            self.i18n.set_language('id')

            # 保存當前內容
            current_data = self.tab_manager.get_feedback_data()

            # 重新創建分頁
            self.tab_manager.set_layout_mode(self.combined_mode)
            self.tab_manager.set_layout_orientation(self.layout_orientation)
            self.tab_manager.create_tabs()

            # 恢復內容
            self.tab_manager.restore_content(
                current_data["interactive_feedback"],
                current_data["command_logs"],
                current_data["images"]
            )

            # 重新連接信號
            self.tab_manager.connect_signals(self)

            # 重新載入設定分頁的狀態
            if self.tab_manager.settings_tab:
                self.tab_manager.settings_tab.reload_settings_from_config()

            # 刷新UI文字
            self._refresh_ui_texts()

            # 重新應用視窗定位（使用重置後的設定）
            self._apply_window_positioning()

            # 切換到設定分頁顯示重置結果
            settings_tab_index = 3  # 分離模式下設定分頁是第4個（索引3）
            if settings_tab_index < self.tab_widget.count():
                self.tab_widget.setCurrentIndex(settings_tab_index)

            # 顯示成功訊息
            QMessageBox.information(
                self,
                t('settings.reset.successTitle'),
                t('settings.reset.successMessage'),
                QMessageBox.Ok
            )

            debug_log("設定重置成功")

        except Exception as e:
            debug_log(f"重置設定失敗: {e}")
            QMessageBox.critical(
                self,
                t('errors.title'),
                t('settings.reset.error', error=str(e)),
                QMessageBox.Ok
            )

    def _submit_feedback(self) -> None:
        """Kirim pesan ngobrol"""
        # Dapatkan semua data ngobrol
        data = self.tab_manager.get_feedback_data()

        self.result = data
        debug_log(f"Pesan dikirim: panjang teks={len(data['interactive_feedback'])}, "
                  f"panjang log perintah={len(data['command_logs'])}, "
                  f"jumlah gambar={len(data['images'])}")

        # Tutup window
        self.close()

    def _cancel_feedback(self) -> None:
        """Batalkan ngobrol"""
        debug_log("Batalkan ngobrol")
        self.result = ""
        self.close()

    def force_close(self) -> None:
        """強制關閉視窗（用於超時處理）"""
        debug_log("強制關閉視窗（超時）")
        self.result = ""
        self.close()

    def _on_timeout_occurred(self) -> None:
        """處理超時事件"""
        debug_log("用戶設置的超時時間已到，自動關閉視窗")
        self._timeout_occurred = True
        self.timeout_occurred.emit()
        self.force_close()

    def start_timeout_if_enabled(self) -> None:
        """如果啟用了超時，自動開始倒數計時"""
        if hasattr(self, 'tab_manager') and self.tab_manager:
            timeout_widget = self.tab_manager.get_timeout_widget()
            if timeout_widget:
                enabled, _ = timeout_widget.get_timeout_settings()
                if enabled:
                    timeout_widget.start_countdown()
                    debug_log("窗口顯示時自動開始倒數計時")

    def _on_timeout_settings_changed(self, enabled: bool, seconds: int) -> None:
        """處理超時設置變更（從設置頁籤觸發）"""
        # 檢查是否超過 MCP 超時限制
        if self.mcp_timeout_seconds is not None and seconds > self.mcp_timeout_seconds:
            debug_log(f"用戶設置的超時時間 ({seconds}s) 超過 MCP 限制 ({self.mcp_timeout_seconds}s)，調整為 MCP 時間")
            seconds = self.mcp_timeout_seconds

        # 更新內部狀態
        self.timeout_enabled = enabled
        self.timeout_duration = seconds

        # 保存設置
        self.config_manager.set_timeout_settings(enabled, seconds)
        debug_log(f"超時設置已更新: {'啟用' if enabled else '停用'}, {seconds} 秒")

        # 更新倒數計時器顯示
        self._update_countdown_visibility()

        # 重新開始倒數計時
        if enabled:
            self.start_countdown()
        else:
            self.stop_countdown()

    def start_timeout_if_enabled(self) -> None:
        """如果啟用了超時，開始倒數計時"""
        if self.timeout_enabled:
            self.start_countdown()
            debug_log("超時倒數計時已開始")

    def stop_timeout(self) -> None:
        """停止超時倒數計時"""
        self.stop_countdown()
        debug_log("超時倒數計時已停止")

    def start_countdown(self) -> None:
        """開始倒數計時"""
        if not self.timeout_enabled:
            return

        self.remaining_seconds = self.timeout_duration
        self.countdown_timer.start(1000)  # 每秒更新
        self._update_countdown_display()
        debug_log(f"開始倒數計時：{self.timeout_duration} 秒")

    def stop_countdown(self) -> None:
        """停止倒數計時"""
        self.countdown_timer.stop()
        self.countdown_display.setText("--:--")
        debug_log("倒數計時已停止")

    def _update_countdown(self) -> None:
        """更新倒數計時"""
        self.remaining_seconds -= 1
        self._update_countdown_display()

        if self.remaining_seconds <= 0:
            self.countdown_timer.stop()
            self._on_timeout_occurred()
            debug_log("倒數計時結束，觸發超時事件")

    def _update_countdown_display(self) -> None:
        """更新倒數顯示"""
        if self.remaining_seconds <= 0:
            self.countdown_display.setText("00:00")
            self.countdown_display.setStyleSheet("""
                color: #ff4444;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Consolas', 'Monaco', monospace;
                min-width: 50px;
                margin-left: 8px;
            """)
        else:
            minutes = self.remaining_seconds // 60
            seconds = self.remaining_seconds % 60
            time_text = f"{minutes:02d}:{seconds:02d}"
            self.countdown_display.setText(time_text)

            # 根據剩餘時間調整顏色
            if self.remaining_seconds <= 60:  # 最後1分鐘
                color = "#ff4444"  # 紅色
            elif self.remaining_seconds <= 300:  # 最後5分鐘
                color = "#ffaa00"  # 橙色
            else:
                color = "#ffa500"  # 黃色

            self.countdown_display.setStyleSheet(f"""
                color: {color};
                font-size: 14px;
                font-weight: bold;
                font-family: 'Consolas', 'Monaco', monospace;
                min-width: 50px;
                margin-left: 8px;
            """)

    def _update_countdown_visibility(self) -> None:
        """更新倒數計時器可見性"""
        # 倒數計時器只在啟用超時時顯示
        self.countdown_label.setVisible(self.timeout_enabled)
        self.countdown_display.setVisible(self.timeout_enabled)

    def _refresh_ui_texts(self) -> None:
        """刷新界面文字"""
        self.setWindowTitle(t('app.title'))
        self.project_label.setText(f"{t('app.projectDirectory')}: {self.project_dir}")

        # 更新按鈕文字
        self.submit_button.setText(t('buttons.submit'))
        self.cancel_button.setText(t('buttons.cancel'))

        # 更新倒數計時器文字
        if hasattr(self, 'countdown_label'):
            self.countdown_label.setText(t('timeout.remaining'))

        # 更新分頁文字
        self.tab_manager.update_tab_texts()

    def _apply_window_positioning(self) -> None:
        """根據用戶設置應用視窗定位策略"""
        always_center = self.config_manager.get_always_center_window()

        if always_center:
            # 總是中心顯示模式：使用保存的大小（如果有的話），然後置中
            self._restore_window_size_only()
            self._move_to_primary_screen_center()
        else:
            # 智能定位模式：先嘗試恢復上次完整的位置和大小
            if self._restore_last_position():
                # 檢查恢復的位置是否可見
                if not self._is_window_visible():
                    self._move_to_primary_screen_center()
            else:
                # 沒有保存的位置，移到中心
                self._move_to_primary_screen_center()

    def _is_window_visible(self) -> bool:
        """檢查視窗是否在任何螢幕的可見範圍內"""
        from PySide6.QtWidgets import QApplication

        window_rect = self.frameGeometry()

        for screen in QApplication.screens():
            if screen.availableGeometry().intersects(window_rect):
                return True
        return False

    def _move_to_primary_screen_center(self) -> None:
        """將視窗移到主螢幕中心"""
        from PySide6.QtWidgets import QApplication

        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            window_geometry = self.frameGeometry()
            center_point = screen_geometry.center()
            window_geometry.moveCenter(center_point)
            self.move(window_geometry.topLeft())
            debug_log("視窗已移到主螢幕中心")

    def _restore_window_size_only(self) -> bool:
        """只恢復視窗大小（不恢復位置）"""
        try:
            geometry = self.config_manager.get_window_geometry()
            if geometry and 'width' in geometry and 'height' in geometry:
                self.resize(geometry['width'], geometry['height'])
                debug_log(f"已恢復視窗大小: {geometry['width']}x{geometry['height']}")
                return True
        except Exception as e:
            debug_log(f"恢復視窗大小失敗: {e}")
        return False

    def _restore_last_position(self) -> bool:
        """嘗試恢復上次保存的視窗位置和大小"""
        try:
            geometry = self.config_manager.get_window_geometry()
            if geometry and 'x' in geometry and 'y' in geometry and 'width' in geometry and 'height' in geometry:
                self.move(geometry['x'], geometry['y'])
                self.resize(geometry['width'], geometry['height'])
                debug_log(f"Posisi jendela dipulihkan: ({geometry['x']}, {geometry['y']}) ukuran: {geometry['width']}x{geometry['height']}")
                return True
        except Exception as e:
            debug_log(f"恢復視窗位置失敗: {e}")
        return False

    def _save_window_position(self) -> None:
        """保存當前視窗位置和大小"""
        try:
            always_center = self.config_manager.get_always_center_window()

            # 獲取當前幾何信息
            current_geometry = {
                'width': self.width(),
                'height': self.height()
            }

            if not always_center:
                # 智能定位模式：同時保存位置
                current_geometry['x'] = self.x()
                current_geometry['y'] = self.y()
                debug_log(f"Posisi jendela tersimpan: ({current_geometry['x']}, {current_geometry['y']}) ukuran: {current_geometry['width']}x{current_geometry['height']}")
            else:
                # 總是中心顯示模式：只保存大小，不保存位置
                debug_log(f"Ukuran jendela tersimpan: {current_geometry['width']}x{current_geometry['height']} (mode selalu di tengah)")

            # 獲取現有配置，只更新需要的部分
            saved_geometry = self.config_manager.get_window_geometry() or {}
            saved_geometry.update(current_geometry)

            self.config_manager.set_window_geometry(saved_geometry)

        except Exception as e:
            debug_log(f"保存視窗狀態失敗: {e}")

    def resizeEvent(self, event) -> None:
        """窗口大小變化事件"""
        super().resizeEvent(event)
        # 窗口大小變化時始終保存（無論是否設置為中心顯示）
        if hasattr(self, 'config_manager'):
            self._schedule_save_window_position()

    def moveEvent(self, event) -> None:
        """窗口位置變化事件"""
        super().moveEvent(event)
        # 窗口位置變化只在智能定位模式下保存
        if hasattr(self, 'config_manager') and not self.config_manager.get_always_center_window():
            self._schedule_save_window_position()

    def _schedule_save_window_position(self) -> None:
        """調度窗口位置保存（防抖機制）"""
        if hasattr(self, '_save_timer'):
            self._save_timer.start(self._save_delay)

    def _delayed_save_window_position(self) -> None:
        """延遲保存窗口位置（防抖機制的實際執行）"""
        self._save_window_position()

    def _auto_focus_input(self) -> None:
        """自動聚焦到輸入框"""
        try:
            # 確保窗口已經顯示並激活
            self.raise_()
            self.activateWindow()

            # 獲取回饋輸入框（修正邏輯）
            feedback_input = None

            # 檢查是否有tab_manager
            if not hasattr(self, 'tab_manager'):
                debug_log("tab_manager 不存在")
                return

            # 檢查 feedback_tab（無論是合併模式還是分離模式）
            if hasattr(self.tab_manager, 'feedback_tab') and self.tab_manager.feedback_tab:
                if hasattr(self.tab_manager.feedback_tab, 'feedback_input'):
                    feedback_input = self.tab_manager.feedback_tab.feedback_input
                    debug_log("Menemukan input box di feedback_tab")
                else:
                    debug_log("feedback_tab存在但沒有feedback_input屬性")
            else:
                debug_log("沒有找到feedback_tab")

            # 設置焦點到輸入框
            if feedback_input:
                feedback_input.setFocus()
                feedback_input.raise_()  # 確保輸入框可見
                debug_log("Fokus otomatis ke input box berhasil")
            else:
                debug_log("未找到回饋輸入框，無法自動聚焦")
                # 打印調試信息
                if hasattr(self, 'tab_manager'):
                    debug_log(f"tab_manager 屬性: {dir(self.tab_manager)}")

        except Exception as e:
            debug_log(f"自動聚焦失敗: {e}")
            import traceback
            debug_log(f"詳細錯誤: {traceback.format_exc()}")

    def closeEvent(self, event) -> None:
        """窗口關閉事件"""
        # 最終保存視窗狀態（大小始終保存，位置根據設置決定）
        self._save_window_position()

        # 清理分頁管理器
        self.tab_manager.cleanup()
        event.accept()
        debug_log("主窗口已關閉")
