#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modul Dukungan Internasionalisasi
==================================

Menyediakan fungsionalitas dukungan multi-bahasa terpadu, mendukung bahasa Indonesia,
Tradisional Cina, Inggris, dan bahasa lainnya.
Deteksi bahasa sistem otomatis dan menyediakan fungsionalitas pergantian bahasa.

Arsitektur Baru:
- Menggunakan file terjemahan JSON terpisah
- Mendukung kunci terjemahan bersarang
- Dukungan metadata
- Mudah diperluas untuk bahasa baru

Penulis: Minidoracat
"""

import os
import sys
import locale
import json
from typing import Dict, Any, Optional, Union
from pathlib import Path

from .debug import i18n_debug_log as debug_log


class I18nManager:
    """Manajer Internasionalisasi - Versi Arsitektur Baru"""

    def __init__(self):
        self._current_language = None
        self._translations = {}
        self._supported_languages = ['id', 'en', 'zh-TW', 'zh-CN']  # Bahasa Indonesia di urutan pertama
        self._fallback_language = 'id'  # Default ke Bahasa Indonesia
        self._config_file = self._get_config_file_path()
        self._locales_dir = Path(__file__).parent / "gui" / "locales"
        
        # 載入翻譯
        self._load_all_translations()
        
        # 設定語言
        self._current_language = self._detect_language()
    
    def _get_config_file_path(self) -> Path:
        """Mendapatkan jalur file konfigurasi"""
        config_dir = Path.home() / ".config" / "mcp-ngobrol"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "language.json"
    
    def _load_all_translations(self) -> None:
        """Memuat semua file terjemahan bahasa"""
        self._translations = {}

        for lang_code in self._supported_languages:
            lang_dir = self._locales_dir / lang_code
            translation_file = lang_dir / "translations.json"

            if translation_file.exists():
                try:
                    with open(translation_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self._translations[lang_code] = data
                        debug_log(f"Berhasil memuat bahasa {lang_code}: {data.get('meta', {}).get('displayName', lang_code)}")
                except Exception as e:
                    debug_log(f"Gagal memuat file bahasa {lang_code}: {e}")
                    # Jika gagal memuat, gunakan terjemahan kosong
                    self._translations[lang_code] = {}
            else:
                debug_log(f"File bahasa tidak ditemukan: {translation_file}")
                self._translations[lang_code] = {}
    
    def _detect_language(self) -> str:
        """Deteksi bahasa otomatis dengan prioritas Bahasa Indonesia"""
        # 1. Prioritas menggunakan pengaturan bahasa yang disimpan pengguna
        saved_lang = self._load_saved_language()
        if saved_lang and saved_lang in self._supported_languages:
            debug_log(f"Menggunakan bahasa tersimpan: {saved_lang}")
            return saved_lang

        # 2. Periksa variabel lingkungan MCP_LANGUAGE
        env_lang = os.getenv('MCP_LANGUAGE', '').strip()
        if env_lang and env_lang in self._supported_languages:
            debug_log(f"Menggunakan bahasa dari environment: {env_lang}")
            return env_lang

        # 3. Untuk MCP Ngobrol, default ke Bahasa Indonesia kecuali ada preferensi eksplisit
        # Hanya gunakan deteksi sistem jika ada preferensi eksplisit untuk bahasa lain
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                # Hanya gunakan bahasa sistem jika eksplisit Indonesia atau Chinese
                if system_locale.startswith('id') or system_locale.startswith('in'):
                    debug_log(f"Sistem locale Indonesia terdeteksi: {system_locale}")
                    return 'id'
                elif system_locale.startswith('zh_TW') or system_locale.startswith('zh_Hant'):
                    debug_log(f"Sistem locale Chinese Traditional terdeteksi: {system_locale}")
                    return 'zh-TW'
                elif system_locale.startswith('zh_CN') or system_locale.startswith('zh_Hans'):
                    debug_log(f"Sistem locale Chinese Simplified terdeteksi: {system_locale}")
                    return 'zh-CN'
                # Untuk locale lainnya (termasuk English), gunakan Bahasa Indonesia sebagai default
        except Exception as e:
            debug_log(f"Error deteksi locale: {e}")

        # 4. Default ke Bahasa Indonesia untuk MCP Ngobrol
        debug_log("Menggunakan Bahasa Indonesia sebagai default untuk MCP Ngobrol")
        return self._fallback_language
    
    def _load_saved_language(self) -> Optional[str]:
        """Memuat pengaturan bahasa yang disimpan"""
        try:
            if self._config_file.exists():
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('language')
        except Exception:
            pass
        return None

    def save_language(self, language: str) -> None:
        """Menyimpan pengaturan bahasa"""
        try:
            config = {'language': language}
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get_current_language(self) -> str:
        """Mendapatkan bahasa saat ini"""
        return self._current_language

    def set_language(self, language: str) -> bool:
        """Mengatur bahasa"""
        if language in self._supported_languages:
            self._current_language = language
            self.save_language(language)
            return True
        return False

    def get_supported_languages(self) -> list:
        """Mendapatkan daftar bahasa yang didukung"""
        return self._supported_languages.copy()

    def get_language_info(self, language_code: str) -> Dict[str, Any]:
        """Mendapatkan informasi metadata bahasa"""
        if language_code in self._translations:
            return self._translations[language_code].get('meta', {})
        return {}
    
    def _get_nested_value(self, data: Dict[str, Any], key_path: str) -> Optional[str]:
        """Mendapatkan nilai dari dictionary bersarang, mendukung jalur kunci yang dipisahkan titik"""
        keys = key_path.split('.')
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None

        return current if isinstance(current, str) else None
    
    def t(self, key: str, **kwargs) -> str:
        """
        翻譯函數 - 支援新舊兩種鍵值格式
        
        新格式: 'buttons.submit' -> data['buttons']['submit']
        舊格式: 'btn_submit_feedback' -> 兼容舊的鍵值
        """
        # 獲取當前語言的翻譯
        current_translations = self._translations.get(self._current_language, {})
        
        # 嘗試新格式（巢狀鍵）
        text = self._get_nested_value(current_translations, key)
        
        # 如果沒有找到，嘗試舊格式的兼容映射
        if text is None:
            text = self._get_legacy_translation(current_translations, key)
        
        # 如果還是沒有找到，嘗試使用回退語言
        if text is None:
            fallback_translations = self._translations.get(self._fallback_language, {})
            text = self._get_nested_value(fallback_translations, key)
            if text is None:
                text = self._get_legacy_translation(fallback_translations, key)
        
        # 最後回退到鍵本身
        if text is None:
            text = key
        
        # 處理格式化參數
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                pass
        
        return text
    
    def _get_legacy_translation(self, translations: Dict[str, Any], key: str) -> Optional[str]:
        """獲取舊格式翻譯的兼容方法"""
        # 舊鍵到新鍵的映射
        legacy_mapping = {
            # 應用程式
            'app_title': 'app.title',
            'project_directory': 'app.projectDirectory',
            'language': 'app.language',
            'settings': 'app.settings',
            
            # 分頁
            'feedback_tab': 'tabs.feedback',
            'command_tab': 'tabs.command',
            'images_tab': 'tabs.images',
            
            # 回饋
            'feedback_title': 'feedback.title',
            'feedback_description': 'feedback.description',
            'feedback_placeholder': 'feedback.placeholder',
            
            # 命令
            'command_title': 'command.title',
            'command_description': 'command.description',
            'command_placeholder': 'command.placeholder',
            'command_output': 'command.output',
            
            # 圖片
            'images_title': 'images.title',
            'images_select': 'images.select',
            'images_paste': 'images.paste',
            'images_clear': 'images.clear',
            'images_status': 'images.status',
            'images_status_with_size': 'images.statusWithSize',
            'images_drag_hint': 'images.dragHint',
            'images_delete_confirm': 'images.deleteConfirm',
            'images_delete_title': 'images.deleteTitle',
            'images_size_warning': 'images.sizeWarning',
            'images_format_error': 'images.formatError',
            
            # 按鈕
            'submit': 'buttons.submit',
            'cancel': 'buttons.cancel',
            'close': 'buttons.close',
            'clear': 'buttons.clear',
            'btn_submit_feedback': 'buttons.submitFeedback',
            'btn_cancel': 'buttons.cancel',
            'btn_select_files': 'buttons.selectFiles',
            'btn_paste_clipboard': 'buttons.pasteClipboard',
            'btn_clear_all': 'buttons.clearAll',
            'btn_run_command': 'buttons.runCommand',
            
            # 狀態
            'feedback_submitted': 'status.feedbackSubmitted',
            'feedback_cancelled': 'status.feedbackCancelled',
            'timeout_message': 'status.timeoutMessage',
            'error_occurred': 'status.errorOccurred',
            'loading': 'status.loading',
            'connecting': 'status.connecting',
            'connected': 'status.connected',
            'disconnected': 'status.disconnected',
            'uploading': 'status.uploading',
            'upload_success': 'status.uploadSuccess',
            'upload_failed': 'status.uploadFailed',
            'command_running': 'status.commandRunning',
            'command_finished': 'status.commandFinished',
            'paste_success': 'status.pasteSuccess',
            'paste_failed': 'status.pasteFailed',
            'invalid_file_type': 'status.invalidFileType',
            'file_too_large': 'status.fileTooLarge',
            
            # 其他
            'ai_summary': 'aiSummary',
            'language_selector': 'languageSelector',
            'language_zh_tw': 'languageNames.zhTw',
            'language_en': 'languageNames.en',
            'language_zh_cn': 'languageNames.zhCn',
            
            # 測試
            'test_qt_gui_summary': 'test.qtGuiSummary',
            'test_web_ui_summary': 'test.webUiSummary',
        }
        
        # 檢查是否有對應的新鍵
        new_key = legacy_mapping.get(key)
        if new_key:
            return self._get_nested_value(translations, new_key)
        
        return None
    
    def get_language_display_name(self, language_code: str) -> str:
        """獲取語言的顯示名稱"""
        # 直接從當前語言的翻譯中獲取，避免遞歸
        current_translations = self._translations.get(self._current_language, {})
        
        # Bangun kunci berdasarkan kode bahasa
        lang_key = None
        if language_code == 'id':
            lang_key = 'languageNames.id'
        elif language_code == 'zh-TW':
            lang_key = 'languageNames.zhTw'
        elif language_code == 'zh-CN':
            lang_key = 'languageNames.zhCn'
        elif language_code == 'en':
            lang_key = 'languageNames.en'
        else:
            # Format umum
            lang_key = f"languageNames.{language_code.replace('-', '').lower()}"
        
        # Dapatkan terjemahan langsung, hindari memanggil self.t() yang menyebabkan rekursi
        if lang_key:
            display_name = self._get_nested_value(current_translations, lang_key)
            if display_name:
                return display_name

        # Fallback ke nama tampilan dalam metadata
        meta = self.get_language_info(language_code)
        return meta.get('displayName', language_code)

    def reload_translations(self) -> None:
        """Memuat ulang semua file terjemahan (untuk pengembangan)"""
        self._load_all_translations()

    def add_language(self, language_code: str, translation_file_path: str) -> bool:
        """Menambahkan dukungan bahasa baru secara dinamis"""
        try:
            translation_file = Path(translation_file_path)
            if not translation_file.exists():
                return False

            with open(translation_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._translations[language_code] = data

                if language_code not in self._supported_languages:
                    self._supported_languages.append(language_code)

                debug_log(f"Berhasil menambahkan bahasa {language_code}: {data.get('meta', {}).get('displayName', language_code)}")
                return True
        except Exception as e:
            debug_log(f"Gagal menambahkan bahasa {language_code}: {e}")
            return False


# Instance manajer internasionalisasi global
_i18n_manager = None

def get_i18n_manager() -> I18nManager:
    """Mendapatkan instance manajer internasionalisasi global"""
    global _i18n_manager
    if _i18n_manager is None:
        _i18n_manager = I18nManager()
    return _i18n_manager

def t(key: str, **kwargs) -> str:
    """Fungsi terjemahan yang mudah"""
    return get_i18n_manager().t(key, **kwargs)

def set_language(language: str) -> bool:
    """Mengatur bahasa"""
    return get_i18n_manager().set_language(language)

def get_current_language() -> str:
    """Mendapatkan bahasa saat ini"""
    return get_i18n_manager().get_current_language()

def reload_translations() -> None:
    """Memuat ulang terjemahan (untuk pengembangan)"""
    get_i18n_manager().reload_translations()