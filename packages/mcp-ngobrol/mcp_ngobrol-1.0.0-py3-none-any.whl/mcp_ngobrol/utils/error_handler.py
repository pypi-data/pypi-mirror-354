"""
Framework Penanganan Error Terpadu
===================================

Menyediakan mekanisme penanganan error terpadu, termasuk:
- Klasifikasi tipe error
- Pesan error yang ramah pengguna
- Pencatatan konteks error
- Saran solusi
- Dukungan internasionalisasi

Catatan: Modul ini tidak akan mempengaruhi komunikasi JSON RPC, semua penanganan error dilakukan di lapisan aplikasi.
"""

import os
import sys
import traceback
import time
from enum import Enum
from typing import Dict, Any, Optional, List, Tuple
from ..debug import debug_log


class ErrorType(Enum):
    """Enumerasi tipe error"""
    NETWORK = "network"           # Error terkait jaringan
    FILE_IO = "file_io"          # Error I/O file
    PROCESS = "process"          # Error terkait proses
    TIMEOUT = "timeout"          # Error timeout
    USER_CANCEL = "user_cancel"  # Pengguna membatalkan operasi
    SYSTEM = "system"            # Error sistem
    PERMISSION = "permission"    # Error izin
    VALIDATION = "validation"    # Error validasi data
    DEPENDENCY = "dependency"    # Error dependensi
    CONFIGURATION = "config"     # Error konfigurasi


class ErrorSeverity(Enum):
    """Tingkat keparahan error"""
    LOW = "low"           # Rendah: tidak mempengaruhi fungsi inti
    MEDIUM = "medium"     # Sedang: mempengaruhi sebagian fungsi
    HIGH = "high"         # Tinggi: mempengaruhi fungsi inti
    CRITICAL = "critical" # Kritis: sistem tidak dapat berjalan normal


class ErrorHandler:
    """Penanganan error terpadu"""

    # Mapping tipe error ke informasi yang ramah pengguna
    _ERROR_MESSAGES = {
        ErrorType.NETWORK: {
            "id": "Masalah koneksi jaringan",
            "zh-TW": "網絡連接出現問題",
            "zh-CN": "网络连接出现问题",
            "en": "Network connection issue"
        },
        ErrorType.FILE_IO: {
            "id": "Masalah baca/tulis file",
            "zh-TW": "文件讀寫出現問題",
            "zh-CN": "文件读写出现问题",
            "en": "File read/write issue"
        },
        ErrorType.PROCESS: {
            "id": "Masalah eksekusi proses",
            "zh-TW": "進程執行出現問題",
            "zh-CN": "进程执行出现问题",
            "en": "Process execution issue"
        },
        ErrorType.TIMEOUT: {
            "id": "Timeout operasi",
            "zh-TW": "操作超時",
            "zh-CN": "操作超时",
            "en": "Operation timeout"
        },
        ErrorType.USER_CANCEL: {
            "id": "Pengguna membatalkan operasi",
            "zh-TW": "用戶取消了操作",
            "zh-CN": "用户取消了操作",
            "en": "User cancelled the operation"
        },
        ErrorType.SYSTEM: {
            "id": "Masalah sistem",
            "zh-TW": "系統出現問題",
            "zh-CN": "系统出现问题",
            "en": "System issue"
        },
        ErrorType.PERMISSION: {
            "id": "Izin tidak mencukupi",
            "zh-TW": "權限不足",
            "zh-CN": "权限不足",
            "en": "Insufficient permissions"
        },
        ErrorType.VALIDATION: {
            "id": "Validasi data gagal",
            "zh-TW": "數據驗證失敗",
            "zh-CN": "数据验证失败",
            "en": "Data validation failed"
        },
        ErrorType.DEPENDENCY: {
            "id": "Masalah komponen dependensi",
            "zh-TW": "依賴組件出現問題",
            "zh-CN": "依赖组件出现问题",
            "en": "Dependency issue"
        },
        ErrorType.CONFIGURATION: {
            "id": "Masalah konfigurasi",
            "zh-TW": "配置出現問題",
            "zh-CN": "配置出现问题",
            "en": "Configuration issue"
        }
    }
    
    # Saran solusi error
    _ERROR_SOLUTIONS = {
        ErrorType.NETWORK: {
            "id": [
                "Periksa koneksi jaringan",
                "Verifikasi pengaturan firewall",
                "Coba restart aplikasi"
            ],
            "zh-TW": [
                "檢查網絡連接是否正常",
                "確認防火牆設置",
                "嘗試重新啟動應用程序"
            ],
            "zh-CN": [
                "检查网络连接是否正常",
                "确认防火墙设置",
                "尝试重新启动应用程序"
            ],
            "en": [
                "Check network connection",
                "Verify firewall settings",
                "Try restarting the application"
            ]
        },
        ErrorType.FILE_IO: {
            "id": [
                "Periksa apakah file ada",
                "Verifikasi izin file",
                "Periksa ruang disk yang tersedia"
            ],
            "zh-TW": [
                "檢查文件是否存在",
                "確認文件權限",
                "檢查磁盤空間是否足夠"
            ],
            "zh-CN": [
                "检查文件是否存在",
                "确认文件权限",
                "检查磁盘空间是否足够"
            ],
            "en": [
                "Check if file exists",
                "Verify file permissions",
                "Check available disk space"
            ]
        },
        ErrorType.PROCESS: {
            "id": [
                "Periksa apakah proses berjalan",
                "Verifikasi sumber daya sistem",
                "Coba restart layanan terkait"
            ],
            "zh-TW": [
                "檢查進程是否正在運行",
                "確認系統資源是否足夠",
                "嘗試重新啟動相關服務"
            ],
            "zh-CN": [
                "检查进程是否正在运行",
                "确认系统资源是否足够",
                "尝试重新启动相关服务"
            ],
            "en": [
                "Check if process is running",
                "Verify system resources",
                "Try restarting related services"
            ]
        },
        ErrorType.TIMEOUT: {
            "id": [
                "Tingkatkan pengaturan timeout",
                "Periksa latensi jaringan",
                "Coba ulangi operasi nanti"
            ],
            "zh-TW": [
                "增加超時時間設置",
                "檢查網絡延遲",
                "稍後重試操作"
            ],
            "zh-CN": [
                "增加超时时间设置",
                "检查网络延迟",
                "稍后重试操作"
            ],
            "en": [
                "Increase timeout settings",
                "Check network latency",
                "Retry the operation later"
            ]
        },
        ErrorType.PERMISSION: {
            "id": [
                "Jalankan sebagai administrator",
                "Periksa izin file/direktori",
                "Hubungi administrator sistem"
            ],
            "zh-TW": [
                "以管理員身份運行",
                "檢查文件/目錄權限",
                "聯繫系統管理員"
            ],
            "zh-CN": [
                "以管理员身份运行",
                "检查文件/目录权限",
                "联系系统管理员"
            ],
            "en": [
                "Run as administrator",
                "Check file/directory permissions",
                "Contact system administrator"
            ]
        }
    }
    
    @staticmethod
    def get_current_language() -> str:
        """Mendapatkan pengaturan bahasa saat ini"""
        try:
            # Coba dapatkan bahasa saat ini dari modul i18n
            from ..i18n import get_i18n_manager
            return get_i18n_manager().get_current_language()
        except Exception:
            # Fallback ke variabel lingkungan atau bahasa default
            return os.getenv("MCP_LANGUAGE", "id")

    @staticmethod
    def get_i18n_error_message(error_type: ErrorType) -> str:
        """Mendapatkan pesan error dari sistem internasionalisasi"""
        try:
            from ..i18n import get_i18n_manager
            i18n = get_i18n_manager()
            key = f"errors.types.{error_type.value}"
            message = i18n.t(key)
            # Jika yang dikembalikan adalah kunci itu sendiri, berarti tidak ditemukan terjemahan, gunakan fallback
            if message == key:
                raise Exception("Translation not found")
            return message
        except Exception:
            # Fallback ke mapping built-in
            language = ErrorHandler.get_current_language()
            error_messages = ErrorHandler._ERROR_MESSAGES.get(error_type, {})
            return error_messages.get(language, error_messages.get("id", "Terjadi error yang tidak diketahui"))

    @staticmethod
    def get_i18n_error_solutions(error_type: ErrorType) -> List[str]:
        """從國際化系統獲取錯誤解決方案"""
        try:
            from ..i18n import get_i18n_manager
            i18n = get_i18n_manager()
            key = f"errors.solutions.{error_type.value}"
            solutions = i18n.t(key)
            if isinstance(solutions, list) and len(solutions) > 0:
                return solutions
            # 如果沒有找到或為空，使用回退
            raise Exception("Solutions not found")
        except Exception:
            # 回退到內建映射
            language = ErrorHandler.get_current_language()
            solutions = ErrorHandler._ERROR_SOLUTIONS.get(error_type, {})
            return solutions.get(language, solutions.get("zh-TW", []))
    
    @staticmethod
    def classify_error(error: Exception) -> ErrorType:
        """
        根據異常類型自動分類錯誤
        
        Args:
            error: Python 異常對象
            
        Returns:
            ErrorType: 錯誤類型
        """
        error_name = type(error).__name__
        error_message = str(error).lower()
        
        # 超時錯誤（優先檢查，避免被網絡錯誤覆蓋）
        if 'timeout' in error_name.lower() or 'timeout' in error_message:
            return ErrorType.TIMEOUT

        # 權限錯誤（優先檢查，避免被文件錯誤覆蓋）
        if 'permission' in error_name.lower():
            return ErrorType.PERMISSION
        if any(keyword in error_message for keyword in ['permission denied', 'access denied', 'forbidden']):
            return ErrorType.PERMISSION

        # 網絡相關錯誤
        if any(keyword in error_name.lower() for keyword in ['connection', 'network', 'socket']):
            return ErrorType.NETWORK
        if any(keyword in error_message for keyword in ['connection', 'network', 'socket']):
            return ErrorType.NETWORK

        # 文件 I/O 錯誤
        if any(keyword in error_name.lower() for keyword in ['file', 'ioerror']):  # 使用更精確的匹配
            return ErrorType.FILE_IO
        if any(keyword in error_message for keyword in ['file', 'directory', 'no such file']):
            return ErrorType.FILE_IO

        # 進程相關錯誤
        if any(keyword in error_name.lower() for keyword in ['process', 'subprocess']):
            return ErrorType.PROCESS
        if any(keyword in error_message for keyword in ['process', 'command', 'executable']):
            return ErrorType.PROCESS
            
        # 驗證錯誤
        if any(keyword in error_name.lower() for keyword in ['validation', 'value', 'type']):
            return ErrorType.VALIDATION
            
        # 配置錯誤
        if any(keyword in error_message for keyword in ['config', 'setting', 'environment']):
            return ErrorType.CONFIGURATION
            
        # 默認為系統錯誤
        return ErrorType.SYSTEM
    
    @staticmethod
    def format_user_error(
        error: Exception, 
        error_type: Optional[ErrorType] = None,
        context: Optional[Dict[str, Any]] = None,
        include_technical: bool = False
    ) -> str:
        """
        將技術錯誤轉換為用戶友好的錯誤信息
        
        Args:
            error: Python 異常對象
            error_type: 錯誤類型（可選，會自動分類）
            context: 錯誤上下文信息
            include_technical: 是否包含技術細節
            
        Returns:
            str: 用戶友好的錯誤信息
        """
        # 自動分類錯誤類型
        if error_type is None:
            error_type = ErrorHandler.classify_error(error)
        
        # 獲取當前語言
        language = ErrorHandler.get_current_language()
        
        # 獲取用戶友好的錯誤信息（優先使用國際化系統）
        user_message = ErrorHandler.get_i18n_error_message(error_type)
        
        # 構建完整的錯誤信息
        parts = [f"❌ {user_message}"]
        
        # 添加上下文信息
        if context:
            if context.get("operation"):
                if language == "en":
                    parts.append(f"Operation: {context['operation']}")
                else:
                    parts.append(f"操作：{context['operation']}")
            
            if context.get("file_path"):
                if language == "en":
                    parts.append(f"File: {context['file_path']}")
                else:
                    parts.append(f"文件：{context['file_path']}")
        
        # 添加技術細節（如果需要）
        if include_technical:
            if language == "en":
                parts.append(f"Technical details: {type(error).__name__}: {str(error)}")
            else:
                parts.append(f"技術細節：{type(error).__name__}: {str(error)}")
        
        return "\n".join(parts)
    
    @staticmethod
    def get_error_solutions(error_type: ErrorType) -> List[str]:
        """
        獲取錯誤解決建議

        Args:
            error_type: 錯誤類型

        Returns:
            List[str]: 解決建議列表
        """
        return ErrorHandler.get_i18n_error_solutions(error_type)
    
    @staticmethod
    def log_error_with_context(
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        error_type: Optional[ErrorType] = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM
    ) -> str:
        """
        記錄帶上下文的錯誤信息（不影響 JSON RPC）
        
        Args:
            error: Python 異常對象
            context: 錯誤上下文信息
            error_type: 錯誤類型
            severity: 錯誤嚴重程度
            
        Returns:
            str: 錯誤 ID，用於追蹤
        """
        # 生成錯誤 ID
        error_id = f"ERR_{int(time.time())}_{id(error) % 10000}"
        
        # 自動分類錯誤
        if error_type is None:
            error_type = ErrorHandler.classify_error(error)
        
        # 構建錯誤記錄
        error_record = {
            "error_id": error_id,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error_type": error_type.value,
            "severity": severity.value,
            "exception_type": type(error).__name__,
            "exception_message": str(error),
            "context": context or {},
            "traceback": traceback.format_exc() if severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL] else None
        }
        
        # 記錄到調試日誌（不影響 JSON RPC）
        debug_log(f"錯誤記錄 [{error_id}]: {error_type.value} - {str(error)}")
        
        if context:
            debug_log(f"錯誤上下文 [{error_id}]: {context}")
        
        # 對於嚴重錯誤，記錄完整堆棧跟蹤
        if severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            debug_log(f"錯誤堆棧 [{error_id}]:\n{traceback.format_exc()}")
        
        return error_id
    
    @staticmethod
    def create_error_response(
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        error_type: Optional[ErrorType] = None,
        include_solutions: bool = True,
        for_user: bool = True
    ) -> Dict[str, Any]:
        """
        創建標準化的錯誤響應
        
        Args:
            error: Python 異常對象
            context: 錯誤上下文
            error_type: 錯誤類型
            include_solutions: 是否包含解決建議
            for_user: 是否為用戶界面使用
            
        Returns:
            Dict[str, Any]: 標準化錯誤響應
        """
        # 自動分類錯誤
        if error_type is None:
            error_type = ErrorHandler.classify_error(error)
        
        # 記錄錯誤
        error_id = ErrorHandler.log_error_with_context(error, context, error_type)
        
        # 構建響應
        response = {
            "success": False,
            "error_id": error_id,
            "error_type": error_type.value,
            "message": ErrorHandler.format_user_error(error, error_type, context, include_technical=not for_user)
        }
        
        # 添加解決建議
        if include_solutions:
            solutions = ErrorHandler.get_error_solutions(error_type)
            response["solutions"] = solutions  # 即使為空列表也添加
        
        # 添加上下文（僅用於調試）
        if context and not for_user:
            response["context"] = context
        
        return response
