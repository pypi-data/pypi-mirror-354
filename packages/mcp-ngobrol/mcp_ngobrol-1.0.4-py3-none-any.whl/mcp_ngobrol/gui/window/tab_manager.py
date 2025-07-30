#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分頁管理器
==========

負責管理和創建各種分頁組件。
"""

from typing import Dict, Any
from PySide6.QtWidgets import QTabWidget, QSplitter, QWidget, QVBoxLayout, QScrollArea, QSizePolicy
from PySide6.QtCore import Signal, Qt

from ..tabs import FeedbackTab, SummaryTab, CommandTab, SettingsTab, AboutTab
from ..tabs.auto_completion_tab import AutoCompletionTab
from ..widgets import SmartTextEdit, ImageUploadWidget
from ...i18n import t
from ...debug import gui_debug_log as debug_log
from .config_manager import ConfigManager


class TabManager:
    """分頁管理器"""
    
    def __init__(self, tab_widget: QTabWidget, project_dir: str, summary: str, combined_mode: bool, layout_orientation: str = 'vertical'):
        self.tab_widget = tab_widget
        self.project_dir = project_dir
        self.summary = summary
        self.combined_mode = combined_mode
        self.layout_orientation = layout_orientation
        
        # 配置管理器
        self.config_manager = ConfigManager()
        
        # 分頁組件實例
        self.feedback_tab = None
        self.summary_tab = None
        self.command_tab = None
        self.settings_tab = None
        self.about_tab = None
        self.auto_completion_tab = None
        self.combined_feedback_tab = None
    
    def create_tabs(self) -> None:
        """創建所有分頁"""
        # 清除現有分頁
        self.tab_widget.clear()
        
        if self.combined_mode:
            # 合併模式：回饋頁包含AI摘要
            self._create_combined_feedback_tab()
            self.tab_widget.addTab(self.combined_feedback_tab, t('tabs.feedback'))
        else:
            # 分離模式：分別的回饋和摘要頁
            self.feedback_tab = FeedbackTab()
            self.tab_widget.addTab(self.feedback_tab, t('tabs.feedback'))
            
            self.summary_tab = SummaryTab(self.summary)
            self.tab_widget.addTab(self.summary_tab, t('tabs.summary'))
        
        # 命令分頁
        self.command_tab = CommandTab(self.project_dir)
        self.tab_widget.addTab(self.command_tab, t('tabs.command'))
        
        # Auto-completion & Checkpoint 分頁
        self.auto_completion_tab = AutoCompletionTab()
        self.tab_widget.addTab(self.auto_completion_tab, "🔔 Auto & 📋 Checkpoint")

        # 設置分頁
        self.settings_tab = SettingsTab(self.combined_mode, self.config_manager)
        self.settings_tab.set_layout_orientation(self.layout_orientation)
        self.tab_widget.addTab(self.settings_tab, t('tabs.language'))

        # 關於分頁
        self.about_tab = AboutTab()
        self.tab_widget.addTab(self.about_tab, t('tabs.about'))
        
        debug_log(f"Tab berhasil dibuat, mode: {'gabungan' if self.combined_mode else 'terpisah'}, orientasi: {self.layout_orientation}")
    
    def _create_combined_feedback_tab(self) -> None:
        """創建合併模式的回饋分頁（包含AI摘要）"""
        self.combined_feedback_tab = QWidget()
        
        # 主布局
        tab_layout = QVBoxLayout(self.combined_feedback_tab)
        tab_layout.setSpacing(12)
        tab_layout.setContentsMargins(0, 0, 0, 0)  # 設置邊距為0
        
        # 創建分割器包裝容器
        splitter_wrapper = QWidget()
        splitter_wrapper_layout = QVBoxLayout(splitter_wrapper)
        splitter_wrapper_layout.setContentsMargins(16, 16, 16, 0)  # 恢復左右邊距設置
        splitter_wrapper_layout.setSpacing(0)
        
        # 根據布局方向創建分割器
        orientation = Qt.Horizontal if self.layout_orientation == 'horizontal' else Qt.Vertical
        main_splitter = QSplitter(orientation)
        main_splitter.setChildrenCollapsible(False)
        main_splitter.setHandleWidth(6)
        main_splitter.setContentsMargins(0, 0, 0, 0)  # 設置分割器邊距為0
        
        # 設置分割器wrapper樣式，確保分割器延伸到邊緣
        splitter_wrapper.setStyleSheet("""
            QWidget {
                margin: 0px;
                padding: 0px;
            }
        """)
        
        # 根據方向設置不同的分割器樣式
        if self.layout_orientation == 'horizontal':
            # 水平布局（左右）
            main_splitter.setStyleSheet("""
                QSplitter {
                    border: none;
                    background: transparent;
                }
                QSplitter::handle:horizontal {
                    width: 8px;
                    background-color: #3c3c3c;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    margin-top: 16px;
                    margin-bottom: 16px;
                    margin-left: 2px;
                    margin-right: 2px;
                }
                QSplitter::handle:horizontal:hover {
                    background-color: #606060;
                    border-color: #808080;
                }
                QSplitter::handle:horizontal:pressed {
                    background-color: #007acc;
                    border-color: #005a9e;
                }
            """)
        else:
            # 垂直布局（上下）
            main_splitter.setStyleSheet("""
                QSplitter {
                    border: none;
                    background: transparent;
                }
                QSplitter::handle:vertical {
                    height: 8px;
                    background-color: #3c3c3c;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    margin-left: 16px;
                    margin-right: 16px;
                    margin-top: 2px;
                    margin-bottom: 2px;
                }
                QSplitter::handle:vertical:hover {
                    background-color: #606060;
                    border-color: #808080;
                }
                QSplitter::handle:vertical:pressed {
                    background-color: #007acc;
                    border-color: #005a9e;
                }
            """)
        
        # 創建AI摘要組件
        self.summary_tab = SummaryTab(self.summary)
        
        # 創建回饋輸入組件
        self.feedback_tab = FeedbackTab()
        
        if self.layout_orientation == 'horizontal':
            # 水平布局設置 - lebih lebar
            self.summary_tab.setMinimumWidth(200)  # Minimum width yang lebih besar
            self.summary_tab.setMaximumWidth(1000)  # Maximum width yang lebih besar
            self.feedback_tab.setMinimumWidth(300)  # Minimum width yang lebih besar
            self.feedback_tab.setMaximumWidth(1600)  # Maximum width yang lebih besar
            
            # 添加到主分割器
            main_splitter.addWidget(self.summary_tab)
            main_splitter.addWidget(self.feedback_tab)
            
            # 調整分割器比例（水平布局）
            main_splitter.setStretchFactor(0, 1)  # AI摘要區域
            main_splitter.setStretchFactor(1, 2)  # 回饋輸入區域
            
            # 從配置載入分割器位置
            saved_sizes = self.config_manager.get_splitter_sizes('main_splitter_horizontal')
            if saved_sizes and len(saved_sizes) == 2:
                main_splitter.setSizes(saved_sizes)
            else:
                main_splitter.setSizes([500, 900])  # 預設大小yang lebih lebar（水平）
            
            # 連接分割器位置變化信號
            main_splitter.splitterMoved.connect(
                lambda pos, index: self._save_splitter_position(main_splitter, 'main_splitter_horizontal')
            )
            
            # 設置最小高度
            main_splitter.setMinimumHeight(200)  # 降低水平布局最小高度
            main_splitter.setMaximumHeight(2000)
            
        else:
            # 垂直布局設置 - lebih tinggi
            self.summary_tab.setMinimumHeight(100)   # Minimum height yang lebih besar
            self.summary_tab.setMaximumHeight(1200)  # Maximum height yang lebih besar
            self.feedback_tab.setMinimumHeight(150)  # Minimum height yang lebih besar
            self.feedback_tab.setMaximumHeight(2400) # Maximum height yang lebih besar
            
            # 添加到主分割器
            main_splitter.addWidget(self.summary_tab)
            main_splitter.addWidget(self.feedback_tab)
            
            # 調整分割器比例（垂直布局）
            main_splitter.setStretchFactor(0, 1)  # AI摘要區域
            main_splitter.setStretchFactor(1, 2)  # 回饋輸入區域
            
            # 從配置載入分割器位置
            saved_sizes = self.config_manager.get_splitter_sizes('main_splitter_vertical')
            if saved_sizes and len(saved_sizes) == 2:
                main_splitter.setSizes(saved_sizes)
            else:
                main_splitter.setSizes([200, 700])  # 預設大小yang lebih tinggi（垂直）
            
            # 連接分割器位置變化信號
            main_splitter.splitterMoved.connect(
                lambda pos, index: self._save_splitter_position(main_splitter, 'main_splitter_vertical')
            )
            
            # 設置最小高度
            main_splitter.setMinimumHeight(200)  # 降低垂直布局最小高度
            main_splitter.setMaximumHeight(3000)
        
        splitter_wrapper_layout.addWidget(main_splitter)
        
        # 添加底部空間以保持完整的邊距
        bottom_spacer = QWidget()
        bottom_spacer.setFixedHeight(16)
        tab_layout.addWidget(splitter_wrapper, 1)
        tab_layout.addWidget(bottom_spacer)
        
        # 設置合併分頁的大小策略，確保能夠觸發父容器的滾動條
        self.combined_feedback_tab.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        if self.layout_orientation == 'vertical':
            self.combined_feedback_tab.setMinimumHeight(200)  # 降低垂直布局最小高度
        else:
            self.combined_feedback_tab.setMinimumWidth(400)   # 降低水平布局最小寬度
    
    def update_tab_texts(self) -> None:
        """更新分頁標籤文字"""
        if self.combined_mode:
            # 合併模式：回饋、命令、Auto&Checkpoint、設置、關於
            self.tab_widget.setTabText(0, t('tabs.feedback'))
            self.tab_widget.setTabText(1, t('tabs.command'))
            self.tab_widget.setTabText(2, "🔔 Auto & 📋 Checkpoint")
            self.tab_widget.setTabText(3, t('tabs.language'))
            self.tab_widget.setTabText(4, t('tabs.about'))
        else:
            # 分離模式：回饋、摘要、命令、Auto&Checkpoint、設置、關於
            self.tab_widget.setTabText(0, t('tabs.feedback'))
            self.tab_widget.setTabText(1, t('tabs.summary'))
            self.tab_widget.setTabText(2, t('tabs.command'))
            self.tab_widget.setTabText(3, "🔔 Auto & 📋 Checkpoint")
            self.tab_widget.setTabText(4, t('tabs.language'))
            self.tab_widget.setTabText(5, t('tabs.about'))
        
        # 更新各分頁的內部文字
        if self.feedback_tab:
            self.feedback_tab.update_texts()
        if self.summary_tab:
            self.summary_tab.update_texts()
        if self.command_tab:
            self.command_tab.update_texts()
        if self.auto_completion_tab:
            # Auto-completion tab doesn't need text updates (uses static text)
            pass
        if self.settings_tab:
            self.settings_tab.update_texts()
        if self.about_tab:
            self.about_tab.update_texts()
    
    def get_feedback_data(self) -> Dict[str, Any]:
        """獲取回饋數據"""
        result = {
            "interactive_feedback": "",
            "command_logs": "",
            "images": [],
            "settings": {}
        }

        # 獲取回饋文字和圖片
        if self.feedback_tab:
            result["interactive_feedback"] = self.feedback_tab.get_feedback_text()
            result["images"] = self.feedback_tab.get_images_data()

        # 獲取命令日誌
        if self.command_tab:
            result["command_logs"] = self.command_tab.get_command_logs()

        # 獲取圖片設定
        if self.config_manager:
            result["settings"] = {
                "image_size_limit": self.config_manager.get_image_size_limit(),
                "enable_base64_detail": self.config_manager.get_enable_base64_detail()
            }

        return result
    
    def restore_content(self, feedback_text: str, command_logs: str, images_data: list) -> None:
        """恢復內容（用於界面重新創建時）"""
        try:
            if self.feedback_tab and feedback_text:
                if hasattr(self.feedback_tab, 'feedback_input'):
                    self.feedback_tab.feedback_input.setPlainText(feedback_text)
            
            if self.command_tab and command_logs:
                if hasattr(self.command_tab, 'command_output'):
                    self.command_tab.command_output.setPlainText(command_logs)
            
            if self.feedback_tab and images_data:
                if hasattr(self.feedback_tab, 'image_upload'):
                    for img_data in images_data:
                        try:
                            self.feedback_tab.image_upload.add_image_data(img_data)
                        except:
                            pass  # 如果無法恢復圖片，忽略錯誤
                            
            debug_log("Pemulihan konten selesai")
        except Exception as e:
            debug_log(f"恢復內容失敗: {e}")
    
    def connect_signals(self, parent) -> None:
        """連接信號"""
        # 連接設置分頁的信號
        if self.settings_tab:
            # 語言變更信號直接連接到父窗口的刷新方法
            if hasattr(parent, '_refresh_ui_texts'):
                self.settings_tab.language_changed.connect(parent._refresh_ui_texts)
            if hasattr(parent, '_on_layout_change_requested'):
                self.settings_tab.layout_change_requested.connect(parent._on_layout_change_requested)
            if hasattr(parent, '_on_reset_settings_requested'):
                self.settings_tab.reset_requested.connect(parent._on_reset_settings_requested)
            if hasattr(parent, '_on_timeout_settings_changed'):
                self.settings_tab.timeout_settings_changed.connect(parent._on_timeout_settings_changed)
        
        # 圖片貼上信號已在 FeedbackTab 內部直接處理，不需要外部連接
    
    def cleanup(self) -> None:
        """清理資源"""
        if self.command_tab:
            self.command_tab.cleanup()
        
        debug_log("Pembersihan tab manager selesai")
    
    def set_layout_mode(self, combined_mode: bool) -> None:
        """設置佈局模式"""
        self.combined_mode = combined_mode
        if self.settings_tab:
            self.settings_tab.set_layout_mode(combined_mode) 
    
    def set_layout_orientation(self, orientation: str) -> None:
        """設置佈局方向"""
        self.layout_orientation = orientation
        if self.settings_tab:
            self.settings_tab.set_layout_orientation(orientation)

    def _save_splitter_position(self, splitter: QSplitter, config_key: str) -> None:
        """保存分割器位置"""
        sizes = splitter.sizes()
        self.config_manager.set_splitter_sizes(config_key, sizes)
        debug_log(f"分割器位置保存成功，大小: {sizes}") 