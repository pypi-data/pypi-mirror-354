#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program Utama Server MCP
========================

Program server inti MCP Ngobrol, menyediakan fungsionalitas umpan balik interaktif pengguna.
Menggunakan Qt GUI interface yang powerful dan user-friendly.

Fungsi Utama:
- Qt GUI interface yang responsif
- Pemrosesan gambar dan integrasi MCP
- Standardisasi hasil umpan balik
- Memory management dan checkpoint system

Penulis: Fábio Ferreira (penulis asli)
Enhanced by: MBPRCC (GUI-focused, Indonesian-first experience)
"""

import os
import sys
import json
import tempfile
import asyncio
import base64
import time
from typing import Annotated, List, Union, Any
import io

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.types import Image as MCPImage
from mcp.types import TextContent
from pydantic import Field

# Impor dukungan multi-bahasa
from .i18n import get_i18n_manager

# Impor fungsi debugging terpadu
from .debug import server_debug_log as debug_log

# Impor framework penanganan error
from .utils.error_handler import ErrorHandler, ErrorType

# Impor manajer sumber daya
from .utils.resource_manager import get_resource_manager, create_temp_file

# Impor sistem auto-completion dan checkpoint
from .utils.auto_completion import get_auto_completion_system, register_auto_completion_callback, check_auto_completion
from .utils.checkpoint_manager import get_checkpoint_integration

# Impor environment detection dan auto-setup
from .mcp_environment import get_environment_manager
from .auto_mcp_setup import MCPAutoSetup
from .models.completion_trigger import TriggerType
from .models.checkpoint import CheckpointType

# Impor memory system
from .memory import (
    get_session_memory,
    ContextProcessor,
    get_user_preferences,
    enhance_response_with_context
)

# ===== Inisialisasi Encoding =====
def init_encoding():
    """Inisialisasi pengaturan encoding, memastikan penanganan karakter Indonesia yang benar"""
    try:
        # Penanganan khusus Windows
        if sys.platform == 'win32':
            import msvcrt
            # Set ke mode binary
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

            # Bungkus ulang sebagai stream teks UTF-8, dan nonaktifkan buffering
            sys.stdin = io.TextIOWrapper(
                sys.stdin.detach(),
                encoding='utf-8',
                errors='replace',
                newline=None
            )
            sys.stdout = io.TextIOWrapper(
                sys.stdout.detach(),
                encoding='utf-8',
                errors='replace',
                newline='',
                write_through=True  # Kunci: nonaktifkan write buffering
            )
        else:
            # Pengaturan standar untuk sistem non-Windows
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            if hasattr(sys.stdin, 'reconfigure'):
                sys.stdin.reconfigure(encoding='utf-8', errors='replace')

        # Set encoding stderr (untuk pesan debug)
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')

        return True
    except Exception as e:
        # Jika pengaturan encoding gagal, coba pengaturan dasar
        try:
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            if hasattr(sys.stdin, 'reconfigure'):
                sys.stdin.reconfigure(encoding='utf-8', errors='replace')
            if hasattr(sys.stderr, 'reconfigure'):
                sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except:
            pass
        return False

# Inisialisasi encoding (dijalankan saat import)
_encoding_initialized = init_encoding()

# ===== Definisi Konstanta =====
SERVER_NAME = "MCP Koleksi Umpan Balik Interaktif"
SSH_ENV_VARS = ['SSH_CONNECTION', 'SSH_CLIENT', 'SSH_TTY']
REMOTE_ENV_VARS = ['REMOTE_CONTAINERS', 'CODESPACES']

# Inisialisasi server MCP
from . import __version__

# Pastikan log_level diset ke format uppercase yang benar
fastmcp_settings = {}

# Periksa variabel lingkungan dan set log_level yang benar
env_log_level = os.getenv("FASTMCP_LOG_LEVEL", "").upper()
if env_log_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
    fastmcp_settings["log_level"] = env_log_level
else:
    # Default menggunakan level INFO
    fastmcp_settings["log_level"] = "INFO"

mcp = FastMCP(SERVER_NAME, version=__version__, **fastmcp_settings)

# Inisialisasi sistem auto-completion dan checkpoint
auto_completion_system = get_auto_completion_system()
checkpoint_integration = get_checkpoint_integration()

# Inisialisasi memory system
session_memory = get_session_memory()
context_processor = ContextProcessor()
user_preferences = get_user_preferences()


# ===== Auto-completion Callback =====
async def auto_feedback_callback(triggers, text, context):
    """
    Callback yang otomatis dipanggil saat trigger auto-completion terdeteksi
    """
    try:
        debug_log(f"Auto-completion triggered: {[t.trigger_id for t in triggers]}")

        # Buat checkpoint sebelum feedback
        checkpoint_id = checkpoint_integration.create_task_checkpoint(
            task_name="Auto Feedback Trigger",
            is_start=False
        )

        # Ambil project directory dari context atau gunakan current directory
        project_dir = context.get("project_directory", os.getcwd())

        # Generate summary berdasarkan trigger
        summary_parts = []
        for trigger in triggers:
            if trigger.trigger_type == TriggerType.TASK_COMPLETION:
                summary_parts.append("✅ Task completion detected")
            elif trigger.trigger_type == TriggerType.CHAT_ENDING:
                summary_parts.append("💬 Chat ending detected")
            else:
                summary_parts.append(f"🔔 {trigger.description}")

        summary = "Auto-completion triggered:\n" + "\n".join(summary_parts)
        summary += f"\n\nOriginal text: {text[:200]}..."

        if checkpoint_id:
            summary += f"\n\n📋 Checkpoint created: {checkpoint_id}"

        # Panggil interactive_feedback
        result = await interactive_feedback(
            project_directory=project_dir,
            summary=summary,
            timeout=300  # 5 menit timeout untuk auto-completion
        )

        debug_log("Auto-completion feedback completed")
        return result

    except Exception as e:
        debug_log(f"Error in auto-completion callback: {e}")
        return None


# Register callback untuk auto-completion
register_auto_completion_callback("auto_feedback", auto_feedback_callback)


# ===== Fungsi Utilitas =====
def is_wsl_environment() -> bool:
    """
    Deteksi apakah berjalan di lingkungan WSL (Windows Subsystem for Linux)

    Returns:
        bool: True menunjukkan lingkungan WSL, False menunjukkan lingkungan lain
    """
    try:
        # Periksa apakah file /proc/version mengandung identifikasi WSL
        if os.path.exists('/proc/version'):
            with open('/proc/version', 'r') as f:
                version_info = f.read().lower()
                if 'microsoft' in version_info or 'wsl' in version_info:
                    debug_log("Terdeteksi lingkungan WSL (melalui /proc/version)")
                    return True

        # Periksa variabel lingkungan terkait WSL
        wsl_env_vars = ['WSL_DISTRO_NAME', 'WSL_INTEROP', 'WSLENV']
        for env_var in wsl_env_vars:
            if os.getenv(env_var):
                debug_log(f"Terdeteksi variabel lingkungan WSL: {env_var}")
                return True

        # Periksa apakah ada path khusus WSL
        wsl_paths = ['/mnt/c', '/mnt/d', '/proc/sys/fs/binfmt_misc/WSLInterop']
        for path in wsl_paths:
            if os.path.exists(path):
                debug_log(f"Terdeteksi path khusus WSL: {path}")
                return True

    except Exception as e:
        debug_log(f"Terjadi kesalahan dalam proses deteksi WSL: {e}")

    return False


def is_remote_environment() -> bool:
    """
    Deteksi apakah berjalan di lingkungan remote

    Returns:
        bool: True menunjukkan lingkungan remote, False menunjukkan lingkungan lokal
    """
    # WSL tidak boleh dianggap sebagai lingkungan remote, karena dapat mengakses browser Windows
    if is_wsl_environment():
        debug_log("Lingkungan WSL tidak dianggap sebagai lingkungan remote")
        return False

    # Periksa indikator koneksi SSH
    for env_var in SSH_ENV_VARS:
        if os.getenv(env_var):
            debug_log(f"Terdeteksi variabel lingkungan SSH: {env_var}")
            return True

    # Periksa lingkungan pengembangan remote
    for env_var in REMOTE_ENV_VARS:
        if os.getenv(env_var):
            debug_log(f"Terdeteksi lingkungan pengembangan remote: {env_var}")
            return True

    # Periksa container Docker
    if os.path.exists('/.dockerenv'):
        debug_log("Terdeteksi lingkungan container Docker")
        return True

    # Pemeriksaan remote desktop Windows
    if sys.platform == 'win32':
        session_name = os.getenv('SESSIONNAME', '')
        if session_name and 'RDP' in session_name:
            debug_log(f"Terdeteksi remote desktop Windows: {session_name}")
            return True

    # Pemeriksaan lingkungan Linux tanpa display (tapi kecualikan WSL)
    if sys.platform.startswith('linux') and not os.getenv('DISPLAY') and not is_wsl_environment():
        debug_log("Terdeteksi lingkungan Linux tanpa display")
        return True

    return False


def can_use_gui() -> bool:
    """
    Deteksi apakah dapat menggunakan antarmuka grafis Qt GUI

    Returns:
        bool: True menunjukkan dapat menggunakan GUI, False jika ada masalah
    """
    try:
        from PySide6.QtWidgets import QApplication
        debug_log("Berhasil memuat PySide6, dapat menggunakan GUI")
        return True
    except ImportError:
        debug_log("Tidak dapat memuat PySide6, GUI tidak tersedia")
        return False
    except Exception as e:
        debug_log(f"Inisialisasi GUI gagal: {e}")
        return False


def save_feedback_to_file(feedback_data: dict, file_path: str = None) -> str:
    """
    Menyimpan data umpan balik ke file JSON

    Args:
        feedback_data: Dictionary data umpan balik
        file_path: Jalur penyimpanan, jika None akan otomatis generate file sementara

    Returns:
        str: Jalur file yang disimpan
    """
    if file_path is None:
        # Gunakan manajer sumber daya untuk membuat file sementara
        file_path = create_temp_file(suffix='.json', prefix='feedback_')

    # Pastikan direktori ada
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # Salin data untuk menghindari modifikasi data asli
    json_data = feedback_data.copy()

    # Proses data gambar: konversi bytes ke string base64 untuk serialisasi JSON
    if "images" in json_data and isinstance(json_data["images"], list):
        processed_images = []
        for img in json_data["images"]:
            if isinstance(img, dict) and "data" in img:
                processed_img = img.copy()
                # Jika data adalah bytes, konversi ke string base64
                if isinstance(img["data"], bytes):
                    processed_img["data"] = base64.b64encode(img["data"]).decode('utf-8')
                    processed_img["data_type"] = "base64"
                processed_images.append(processed_img)
            else:
                processed_images.append(img)
        json_data["images"] = processed_images

    # Simpan data
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    debug_log(f"Data umpan balik telah disimpan ke: {file_path}")
    return file_path


def create_feedback_text(feedback_data: dict) -> str:
    """
    Membuat teks umpan balik yang diformat

    Args:
        feedback_data: Dictionary data umpan balik

    Returns:
        str: Teks umpan balik yang diformat
    """
    text_parts = []

    # Konten umpan balik dasar
    if feedback_data.get("interactive_feedback"):
        text_parts.append(f"=== Umpan Balik Pengguna ===\n{feedback_data['interactive_feedback']}")

    # Log eksekusi perintah
    if feedback_data.get("command_logs"):
        text_parts.append(f"=== Log Eksekusi Perintah ===\n{feedback_data['command_logs']}")

    # Ringkasan lampiran gambar
    if feedback_data.get("images"):
        images = feedback_data["images"]
        text_parts.append(f"=== Ringkasan Lampiran Gambar ===\nPengguna menyediakan {len(images)} gambar:")
        
        for i, img in enumerate(images, 1):
            size = img.get("size", 0)
            name = img.get("name", "unknown")
            
            # Tampilan unit cerdas
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_kb = size / 1024
                size_str = f"{size_kb:.1f} KB"
            else:
                size_mb = size / (1024 * 1024)
                size_str = f"{size_mb:.1f} MB"

            img_info = f"  {i}. {name} ({size_str})"

            # Untuk meningkatkan kompatibilitas, tambahkan informasi pratinjau base64
            if img.get("data"):
                try:
                    if isinstance(img["data"], bytes):
                        img_base64 = base64.b64encode(img["data"]).decode('utf-8')
                    elif isinstance(img["data"], str):
                        img_base64 = img["data"]
                    else:
                        img_base64 = None

                    if img_base64:
                        # Hanya tampilkan pratinjau 50 karakter pertama
                        preview = img_base64[:50] + "..." if len(img_base64) > 50 else img_base64
                        img_info += f"\n     Pratinjau Base64: {preview}"
                        img_info += f"\n     Panjang Base64 lengkap: {len(img_base64)} karakter"

                        # Jika asisten AI tidak mendukung gambar MCP, dapat menyediakan base64 lengkap
                        debug_log(f"Gambar {i} Base64 siap, panjang: {len(img_base64)}")

                        # Periksa apakah mode detail Base64 diaktifkan (dari pengaturan UI)
                        include_full_base64 = feedback_data.get("settings", {}).get("enable_base64_detail", False)

                        if include_full_base64:
                            # Inferensi tipe MIME berdasarkan nama file
                            file_name = img.get("name", "image.png")
                            if file_name.lower().endswith(('.jpg', '.jpeg')):
                                mime_type = 'image/jpeg'
                            elif file_name.lower().endswith('.gif'):
                                mime_type = 'image/gif'
                            elif file_name.lower().endswith('.webp'):
                                mime_type = 'image/webp'
                            else:
                                mime_type = 'image/png'

                            img_info += f"\n     Base64 Lengkap: data:{mime_type};base64,{img_base64}"

                except Exception as e:
                    debug_log(f"Pemrosesan Base64 gambar {i} gagal: {e}")

            text_parts.append(img_info)

        # Tambahkan penjelasan kompatibilitas
        text_parts.append("\n💡 Catatan: Jika asisten AI tidak dapat menampilkan gambar, data gambar telah disertakan dalam informasi Base64 di atas.")

    return "\n\n".join(text_parts) if text_parts else "Pengguna tidak memberikan konten umpan balik apa pun."


def process_images(images_data: List[dict]) -> List[MCPImage]:
    """
    Memproses data gambar, mengkonversi ke objek gambar MCP

    Args:
        images_data: Daftar data gambar

    Returns:
        List[MCPImage]: Daftar objek gambar MCP
    """
    mcp_images = []

    for i, img in enumerate(images_data, 1):
        try:
            if not img.get("data"):
                debug_log(f"Gambar {i} tidak memiliki data, dilewati")
                continue

            # Periksa tipe data dan proses sesuai
            if isinstance(img["data"], bytes):
                # Jika data bytes asli, gunakan langsung
                image_bytes = img["data"]
                debug_log(f"Gambar {i} menggunakan data bytes asli, ukuran: {len(image_bytes)} bytes")
            elif isinstance(img["data"], str):
                # Jika string base64, lakukan decode
                image_bytes = base64.b64decode(img["data"])
                debug_log(f"Gambar {i} didecode dari base64, ukuran: {len(image_bytes)} bytes")
            else:
                debug_log(f"Gambar {i} tipe data tidak didukung: {type(img['data'])}")
                continue

            if len(image_bytes) == 0:
                debug_log(f"Gambar {i} data kosong, dilewati")
                continue

            # Inferensi format berdasarkan nama file
            file_name = img.get("name", "image.png")
            if file_name.lower().endswith(('.jpg', '.jpeg')):
                image_format = 'jpeg'
            elif file_name.lower().endswith('.gif'):
                image_format = 'gif'
            else:
                image_format = 'png'  # Default menggunakan PNG

            # Buat objek MCPImage
            mcp_image = MCPImage(data=image_bytes, format=image_format)
            mcp_images.append(mcp_image)

            debug_log(f"Gambar {i} ({file_name}) berhasil diproses, format: {image_format}")

        except Exception as e:
            # Gunakan penanganan error terpadu (tidak mempengaruhi JSON RPC)
            error_id = ErrorHandler.log_error_with_context(
                e,
                context={"operation": "Pemrosesan gambar", "image_index": i},
                error_type=ErrorType.FILE_IO
            )
            debug_log(f"Gambar {i} gagal diproses [Error ID: {error_id}]: {e}")

    debug_log(f"Total memproses {len(mcp_images)} gambar")
    return mcp_images


async def launch_gui_with_timeout(project_dir: str, summary: str, timeout: int) -> dict:
    """
    Meluncurkan mode GUI dan menangani timeout
    """
    debug_log(f"Meluncurkan mode GUI (timeout: {timeout} detik)")

    try:
        from .gui import feedback_ui_with_timeout

        # Panggil langsung fungsi GUI dengan timeout
        result = feedback_ui_with_timeout(project_dir, summary, timeout)

        if result:
            return {
                "logs": f"Pengumpulan umpan balik mode GUI selesai",
                "interactive_feedback": result.get("interactive_feedback", ""),
                "images": result.get("images", [])
            }
        else:
            return {
                "logs": "Pengguna membatalkan pengumpulan umpan balik",
                "interactive_feedback": "",
                "images": []
            }

    except TimeoutError as e:
        # Exception timeout - ini adalah perilaku yang diharapkan
        raise e
    except Exception as e:
        debug_log(f"Peluncuran GUI gagal: {e}")
        raise Exception(f"Peluncuran GUI gagal: {e}")


# ===== Definisi Tool MCP =====
@mcp.tool()
async def interactive_feedback(
    project_directory: Annotated[str, Field(description="Jalur direktori proyek")] = ".",
    summary: Annotated[str, Field(description="Ringkasan pekerjaan AI yang telah selesai")] = "Saya telah menyelesaikan tugas yang Anda minta.",
    conversation_history: Annotated[str, Field(description="JSON conversation history untuk context awareness")] = "[]",
    user_preferences: Annotated[str, Field(description="JSON user preferences untuk response adaptation")] = "{}",
    session_id: Annotated[str, Field(description="Session identifier untuk memory tracking")] = "default",
    timeout: Annotated[int, Field(description="Waktu timeout menunggu umpan balik pengguna (detik)")] = 600
) -> List:
    """
    Mengumpulkan umpan balik interaktif pengguna, mendukung teks dan gambar

    Tool ini menggunakan Qt GUI interface yang powerful dan user-friendly.

    Pengguna dapat:
    1. Menjalankan perintah untuk memverifikasi hasil
    2. Memberikan umpan balik teks
    3. Mengunggah gambar sebagai umpan balik
    4. Melihat ringkasan pekerjaan AI
    5. Menggunakan fitur-fitur enhanced seperti Memory Bank dan Checkpoint

    Mode debug:
    - Set variabel lingkungan MCP_DEBUG=true untuk mengaktifkan output debug detail
    - Lingkungan produksi disarankan menonaktifkan mode debug untuk menghindari gangguan output

    Args:
        project_directory: Jalur direktori proyek
        summary: Ringkasan pekerjaan AI yang telah selesai
        timeout: Waktu timeout menunggu umpan balik pengguna (detik), default 600 detik (10 menit)

    Returns:
        List: Daftar yang berisi objek TextContent dan MCPImage
    """
    # ===== Parameter Validation dan Normalisasi =====
    try:
        # Normalize conversation_history parameter
        if isinstance(conversation_history, (list, dict)):
            conversation_history = json.dumps(conversation_history, ensure_ascii=False)
        elif not isinstance(conversation_history, str):
            conversation_history = "[]"

        # Validate JSON format
        try:
            json.loads(conversation_history)
        except (json.JSONDecodeError, TypeError):
            debug_log(f"Invalid conversation_history JSON, using default: {conversation_history}")
            conversation_history = "[]"

        # Normalize user_preferences parameter
        if isinstance(user_preferences, (list, dict)):
            user_preferences = json.dumps(user_preferences, ensure_ascii=False)
        elif not isinstance(user_preferences, str):
            user_preferences = "{}"

        # Validate JSON format
        try:
            json.loads(user_preferences)
        except (json.JSONDecodeError, TypeError):
            debug_log(f"Invalid user_preferences JSON, using default: {user_preferences}")
            user_preferences = "{}"

        debug_log(f"Parameter validation completed - conversation_history: {len(conversation_history)} chars, user_preferences: {len(user_preferences)} chars")

    except Exception as param_error:
        debug_log(f"Parameter validation error: {param_error}")
        # Use safe defaults
        conversation_history = "[]"
        user_preferences = "{}"

    # Deteksi GUI availability
    can_gui = can_use_gui()

    debug_log(f"GUI tersedia: {can_gui}")
    debug_log("Menggunakan Qt GUI interface")

    try:
        # Pastikan direktori proyek ada
        if not os.path.exists(project_directory):
            project_directory = os.getcwd()
        project_directory = os.path.abspath(project_directory)

        # Process conversation context untuk enhance summary
        context = context_processor.process_conversation_history(conversation_history, session_id)
        enhanced_summary = context_processor.enhance_summary_with_context(summary, context)

        # Check auto-completion trigger pada enhanced summary
        check_auto_completion(enhanced_summary, {
            "project_directory": project_directory,
            "source": "interactive_feedback_summary",
            "session_id": session_id
        })

        # Gunakan Qt GUI interface
        if can_gui:
            result = await launch_gui_with_timeout(project_directory, summary, timeout)
        else:
            # Fallback jika GUI tidak tersedia
            result = {
                "command_logs": "",
                "interactive_feedback": "GUI tidak tersedia. Silakan install PySide6 atau gunakan environment yang mendukung GUI.",
                "images": []
            }

        # Tangani situasi pembatalan
        if not result:
            return [TextContent(type="text", text="Pengguna membatalkan umpan balik.")]

        # Simpan hasil detail
        save_feedback_to_file(result)

        # Buat daftar item umpan balik
        feedback_items = []

        # Tambahkan umpan balik teks
        if result.get("interactive_feedback") or result.get("command_logs") or result.get("images"):
            feedback_text = create_feedback_text(result)
            feedback_items.append(TextContent(type="text", text=feedback_text))
            debug_log("Umpan balik teks telah ditambahkan")

        # Tambahkan umpan balik gambar
        if result.get("images"):
            mcp_images = process_images(result["images"])
            feedback_items.extend(mcp_images)
            debug_log(f"Telah menambahkan {len(mcp_images)} gambar")

        # Pastikan setidaknya ada satu item umpan balik
        if not feedback_items:
            feedback_items.append(TextContent(type="text", text="Pengguna tidak memberikan konten umpan balik apa pun."))

        debug_log(f"Pengumpulan umpan balik selesai, total {len(feedback_items)} item")

        # Extract feedback text untuk memory dan auto-completion
        feedback_text = ""
        if feedback_items and len(feedback_items) > 0:
            for item in feedback_items:
                if hasattr(item, 'text'):
                    feedback_text += item.text + " "

        # Save exchange ke session memory
        try:
            # Extract topic dari enhanced summary
            topic = session_memory.extract_topics_from_text(enhanced_summary)
            primary_topic = topic[0] if topic else None

            # Save conversation exchange
            session_memory.add_exchange(
                user_input=feedback_text.strip() if feedback_text.strip() else "User provided feedback",
                agent_response=enhanced_summary,
                session_id=session_id,
                topic=primary_topic,
                intent="feedback"
            )

            # Learn dari user feedback jika ada
            if feedback_text.strip():
                user_preferences.learn_from_interaction({
                    "user_input": feedback_text,
                    "user_correction": "",  # No correction in this context
                    "response_length": len(enhanced_summary)
                })

            debug_log(f"Saved exchange to memory for session {session_id}")

        except Exception as memory_error:
            debug_log(f"Error saving to memory: {memory_error}")
            # Continue without failing - memory is optional

        # Check auto-completion trigger pada feedback text
        if feedback_text.strip():
            check_auto_completion(feedback_text, {
                "project_directory": project_directory,
                "source": "interactive_feedback_result",
                "session_id": session_id
            })

        return feedback_items

    except Exception as e:
        # Gunakan penanganan error terpadu, tapi tidak mempengaruhi respons JSON RPC
        error_id = ErrorHandler.log_error_with_context(
            e,
            context={"operation": "Pengumpulan umpan balik", "project_dir": project_directory},
            error_type=ErrorType.SYSTEM
        )

        # Generate pesan error yang ramah pengguna
        user_error_msg = ErrorHandler.format_user_error(e, include_technical=False)
        debug_log(f"Error pengumpulan umpan balik [Error ID: {error_id}]: {str(e)}")

        return [TextContent(type="text", text=user_error_msg)]


@mcp.tool()
async def feedback_simple(
    summary: Annotated[str, Field(description="Ringkasan pekerjaan AI yang telah selesai")] = "Task completed",
    session_id: Annotated[str, Field(description="Session identifier")] = "default",
    timeout: Annotated[int, Field(description="Timeout dalam detik")] = 60
) -> List:
    """
    Simplified feedback tool yang mudah digunakan tanpa parameter bermasalah

    Args:
        summary: Ringkasan pekerjaan AI
        session_id: Session identifier
        timeout: Timeout dalam detik

    Returns:
        List: Feedback items
    """
    return await interactive_feedback(
        project_directory=".",
        summary=summary,
        conversation_history="[]",
        user_preferences="{}",
        session_id=session_id,
        timeout=timeout
    )





@mcp.tool()
def get_system_info() -> str:
    """
    Mendapatkan informasi lingkungan sistem

    Returns:
        str: Informasi sistem dalam format JSON
    """
    is_remote = is_remote_environment()
    is_wsl = is_wsl_environment()
    can_gui = can_use_gui()

    system_info = {
        "Platform": sys.platform,
        "Versi Python": sys.version.split()[0],
        "Lingkungan WSL": is_wsl,
        "Lingkungan Remote": is_remote,
        "GUI Tersedia": can_gui,
        "Antarmuka": "Qt GUI",
        "Variabel Lingkungan": {
            "SSH_CONNECTION": os.getenv("SSH_CONNECTION"),
            "SSH_CLIENT": os.getenv("SSH_CLIENT"),
            "DISPLAY": os.getenv("DISPLAY"),
            "VSCODE_INJECTION": os.getenv("VSCODE_INJECTION"),
            "SESSIONNAME": os.getenv("SESSIONNAME"),
            "WSL_DISTRO_NAME": os.getenv("WSL_DISTRO_NAME"),
            "WSL_INTEROP": os.getenv("WSL_INTEROP"),
            "WSLENV": os.getenv("WSLENV"),
        }
    }

    return json.dumps(system_info, ensure_ascii=False, indent=2)


@mcp.tool()
def get_mcp_environment_info() -> str:
    """
    Mendapatkan informasi lengkap tentang environment MCP

    Returns:
        str: Informasi environment MCP dalam format JSON
    """
    try:
        env_manager = get_environment_manager()
        env_info = env_manager.get_environment_info()

        return json.dumps(env_info, ensure_ascii=False, indent=2)
    except Exception as e:
        error_info = {
            "error": str(e),
            "message": "Failed to get MCP environment info",
            "fallback_info": {
                "platform": sys.platform,
                "python_version": sys.version.split()[0],
                "working_directory": os.getcwd()
            }
        }
        return json.dumps(error_info, ensure_ascii=False, indent=2)


@mcp.tool()
def setup_mcp_configuration(force: Annotated[bool, Field(description="Force overwrite existing configuration")] = False) -> str:
    """
    Setup konfigurasi MCP otomatis untuk environment saat ini

    Args:
        force: Force overwrite existing configuration

    Returns:
        str: Hasil setup dalam format JSON
    """
    try:
        setup = MCPAutoSetup()
        success = setup.setup_mcp_config(force=force)

        result = {
            "success": success,
            "environment": setup.detect_environment(),
            "message": "MCP configuration setup completed" if success else "MCP configuration setup failed",
            "next_steps": [
                "Restart your AI assistant",
                "Test with interactive_feedback tool",
                "Use get_mcp_environment_info for verification"
            ] if success else [
                "Check setup instructions",
                "Manually configure MCP server",
                "Verify environment compatibility"
            ]
        }

        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to setup MCP configuration",
            "suggestion": "Use manual setup instructions"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def enable_auto_completion() -> str:
    """
    Mengaktifkan sistem auto-completion

    Sistem auto-completion akan otomatis memanggil interactive_feedback
    saat mendeteksi pola seperti "task completed", "would you like me to keep going?", dll.

    Returns:
        str: Status aktivasi
    """
    try:
        auto_completion_system.enable()
        stats = auto_completion_system.get_statistics()

        result = {
            "status": "enabled",
            "message": "Auto-completion system telah diaktifkan",
            "statistics": stats
        }

        debug_log("Auto-completion enabled via tool")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Gagal mengaktifkan auto-completion: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def disable_auto_completion() -> str:
    """
    Menonaktifkan sistem auto-completion

    Returns:
        str: Status deaktivasi
    """
    try:
        auto_completion_system.disable()

        result = {
            "status": "disabled",
            "message": "Auto-completion system telah dinonaktifkan"
        }

        debug_log("Auto-completion disabled via tool")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Gagal menonaktifkan auto-completion: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def check_completion_trigger(
    text: Annotated[str, Field(description="Text yang akan diperiksa untuk trigger")]
) -> str:
    """
    Memeriksa apakah text memicu auto-completion trigger

    Args:
        text: Text yang akan diperiksa

    Returns:
        str: Hasil pemeriksaan trigger
    """
    try:
        # Check trigger tanpa execute callback
        triggered = auto_completion_system.trigger_manager.check_triggers(text)

        result = {
            "text": text,
            "triggered": len(triggered) > 0,
            "trigger_count": len(triggered),
            "triggers": [
                {
                    "id": t.trigger_id,
                    "type": t.trigger_type.value,
                    "description": t.description,
                    "pattern": t.pattern
                }
                for t in triggered
            ]
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Error checking trigger: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def create_checkpoint(
    name: Annotated[str, Field(description="Nama checkpoint")] = "",
    description: Annotated[str, Field(description="Deskripsi checkpoint")] = "",
    project_directory: Annotated[str, Field(description="Direktori proyek")] = ".",
    tags: Annotated[str, Field(description="Tags dipisahkan koma")] = ""
) -> str:
    """
    Membuat checkpoint manual

    Args:
        name: Nama checkpoint
        description: Deskripsi checkpoint
        project_directory: Direktori proyek
        tags: Tags dipisahkan koma

    Returns:
        str: Informasi checkpoint yang dibuat
    """
    try:
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []

        # Pastikan direktori proyek ada
        if not os.path.exists(project_directory):
            project_directory = os.getcwd()
        project_directory = os.path.abspath(project_directory)

        # Buat checkpoint
        checkpoint_id = checkpoint_integration.create_checkpoint(
            name=name or f"Manual Checkpoint {time.strftime('%Y-%m-%d %H:%M:%S')}",
            description=description,
            checkpoint_type=CheckpointType.MANUAL,
            project_directory=project_directory,
            tags=tag_list
        )

        # Get checkpoint info
        checkpoint_info = checkpoint_integration.checkpoint_manager.get_checkpoint_info(checkpoint_id)

        result = {
            "status": "created",
            "checkpoint_id": checkpoint_id,
            "checkpoint_info": checkpoint_info,
            "message": f"Checkpoint berhasil dibuat: {checkpoint_info['name']}"
        }

        debug_log(f"Manual checkpoint created: {checkpoint_id}")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Gagal membuat checkpoint: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def list_checkpoints(
    project_directory: Annotated[str, Field(description="Filter berdasarkan direktori proyek")] = "",
    checkpoint_type: Annotated[str, Field(description="Filter berdasarkan tipe (manual, auto, task_start, task_end, error, milestone)")] = "",
    limit: Annotated[int, Field(description="Jumlah maksimal checkpoint yang ditampilkan")] = 20
) -> str:
    """
    Mendapatkan daftar checkpoint

    Args:
        project_directory: Filter berdasarkan direktori proyek
        checkpoint_type: Filter berdasarkan tipe checkpoint
        limit: Jumlah maksimal checkpoint

    Returns:
        str: Daftar checkpoint
    """
    try:
        # Parse checkpoint type
        filter_type = None
        if checkpoint_type:
            try:
                filter_type = CheckpointType(checkpoint_type.lower())
            except ValueError:
                pass

        # Get checkpoints
        checkpoints = checkpoint_integration.checkpoint_manager.list_checkpoints(
            checkpoint_type=filter_type,
            project_directory=project_directory if project_directory else None
        )

        # Limit results
        checkpoints = checkpoints[:limit]

        # Format results
        checkpoint_list = []
        for checkpoint in checkpoints:
            info = checkpoint_integration.checkpoint_manager.get_checkpoint_info(checkpoint.checkpoint_id)
            checkpoint_list.append(info)

        result = {
            "total_found": len(checkpoint_list),
            "checkpoints": checkpoint_list,
            "filters": {
                "project_directory": project_directory,
                "checkpoint_type": checkpoint_type,
                "limit": limit
            }
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Error listing checkpoints: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def restore_checkpoint(
    checkpoint_id: Annotated[str, Field(description="ID checkpoint yang akan di-restore")]
) -> str:
    """
    Restore dari checkpoint

    Args:
        checkpoint_id: ID checkpoint

    Returns:
        str: Status restore
    """
    try:
        success = checkpoint_integration.restore_checkpoint(checkpoint_id)

        if success:
            checkpoint_info = checkpoint_integration.checkpoint_manager.get_checkpoint_info(checkpoint_id)
            result = {
                "status": "restored",
                "checkpoint_id": checkpoint_id,
                "checkpoint_info": checkpoint_info,
                "message": f"Checkpoint berhasil di-restore: {checkpoint_info['name'] if checkpoint_info else checkpoint_id}"
            }
        else:
            result = {
                "status": "failed",
                "checkpoint_id": checkpoint_id,
                "message": "Gagal restore checkpoint. Checkpoint mungkin tidak ditemukan atau rusak."
            }

        debug_log(f"Checkpoint restore {'successful' if success else 'failed'}: {checkpoint_id}")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Error restoring checkpoint: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def get_auto_completion_status() -> str:
    """
    Mendapatkan status dan statistik auto-completion system

    Returns:
        str: Status dan statistik auto-completion
    """
    try:
        stats = auto_completion_system.get_statistics()
        checkpoint_stats = checkpoint_integration.get_checkpoint_statistics()

        result = {
            "auto_completion": stats,
            "checkpoint": checkpoint_stats,
            "integration_status": {
                "auto_completion_enabled": stats["enabled"],
                "checkpoint_auto_enabled": checkpoint_stats["auto_checkpoint_enabled"],
                "registered_callbacks": len(auto_completion_system.callbacks),
                "checkpoint_callbacks": len(checkpoint_integration.checkpoint_callbacks)
            }
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Error getting status: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def enable_auto_completion() -> str:
    """
    Mengaktifkan sistem auto-completion

    Sistem auto-completion akan otomatis memanggil interactive_feedback
    saat mendeteksi pola seperti "task completed", "would you like me to keep going?", dll.

    Returns:
        str: Status aktivasi
    """
    try:
        auto_completion_system.enable()
        stats = auto_completion_system.get_statistics()

        result = {
            "status": "enabled",
            "message": "Auto-completion system telah diaktifkan",
            "statistics": stats
        }

        debug_log("Auto-completion enabled via tool")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Gagal mengaktifkan auto-completion: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def disable_auto_completion() -> str:
    """
    Menonaktifkan sistem auto-completion

    Returns:
        str: Status deaktivasi
    """
    try:
        auto_completion_system.disable()

        result = {
            "status": "disabled",
            "message": "Auto-completion system telah dinonaktifkan"
        }

        debug_log("Auto-completion disabled via tool")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Gagal menonaktifkan auto-completion: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def check_completion_trigger(
    text: Annotated[str, Field(description="Text yang akan diperiksa untuk trigger")]
) -> str:
    """
    Memeriksa apakah text memicu auto-completion trigger

    Args:
        text: Text yang akan diperiksa

    Returns:
        str: Hasil pemeriksaan trigger
    """
    try:
        # Check trigger tanpa execute callback
        triggered = auto_completion_system.trigger_manager.check_triggers(text)

        result = {
            "text": text,
            "triggered": len(triggered) > 0,
            "trigger_count": len(triggered),
            "triggers": [
                {
                    "id": t.trigger_id,
                    "type": t.trigger_type.value,
                    "description": t.description,
                    "pattern": t.pattern
                }
                for t in triggered
            ]
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Error checking trigger: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


# ===== Memory & Context Tools =====

@mcp.tool()
def analyze_conversation_context(
    conversation_history: Annotated[str, Field(description="JSON conversation history untuk analisis")] = "[]",
    session_id: Annotated[str, Field(description="Session identifier")] = "default"
) -> str:
    """
    Analyze conversation context dan return insights

    Args:
        conversation_history: JSON array of conversation exchanges
        session_id: Session identifier

    Returns:
        str: JSON analysis results
    """
    try:
        # Process conversation context
        context = context_processor.process_conversation_history(conversation_history, session_id)

        # Analyze patterns
        patterns = context_processor.analyze_conversation_patterns(session_id)

        # Get contextual hints
        hints = context_processor.get_contextual_response_hints("", session_id)

        result = {
            "session_id": session_id,
            "context_summary": context.context_summary,
            "relevance_score": context.relevance_score,
            "current_topics": context.current_topics,
            "recent_exchanges_count": len(context.recent_exchanges),
            "suggestions": context.suggestions,
            "patterns": patterns,
            "response_hints": hints,
            "analysis_timestamp": time.time()
        }

        debug_log(f"Analyzed conversation context for session {session_id}")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Error analyzing conversation context: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def enhance_response_with_memory(
    base_response: Annotated[str, Field(description="Base response yang akan di-enhance")],
    conversation_history: Annotated[str, Field(description="JSON conversation history")] = "[]",
    user_preferences: Annotated[str, Field(description="JSON user preferences")] = "{}",
    session_id: Annotated[str, Field(description="Session identifier")] = "default"
) -> str:
    """
    Enhance response dengan conversation context dan user preferences

    Args:
        base_response: Original response
        conversation_history: JSON conversation history
        user_preferences: JSON user preferences
        session_id: Session identifier

    Returns:
        str: Enhanced response
    """
    try:
        # Use response enhancer
        from .memory.response_enhancer import enhance_response_with_context
        enhanced = enhance_response_with_context(
            base_response, conversation_history, user_preferences, session_id
        )

        debug_log(f"Enhanced response for session {session_id}")
        return enhanced

    except Exception as e:
        debug_log(f"Error enhancing response: {e}")
        return base_response  # Fallback to original response


@mcp.tool()
def learn_from_user_feedback(
    original_response: Annotated[str, Field(description="Original response")],
    user_feedback: Annotated[str, Field(description="User feedback atau correction")],
    session_id: Annotated[str, Field(description="Session identifier")] = "default"
) -> str:
    """
    Learn dari user feedback untuk improve future responses

    Args:
        original_response: Response yang diberikan sebelumnya
        user_feedback: Feedback atau correction dari user
        session_id: Session identifier

    Returns:
        str: Learning results
    """
    try:
        # Learn dari feedback
        user_preferences.learn_from_interaction({
            "user_input": user_feedback,
            "user_correction": user_feedback,
            "response_length": len(original_response)
        })

        # Update session patterns
        session_memory.update_user_patterns(session_id, {
            "last_feedback": user_feedback,
            "feedback_timestamp": time.time()
        })

        # Analyze what was learned
        patterns = context_processor.analyze_conversation_patterns(session_id)

        result = {
            "status": "learned",
            "message": "Feedback processed and preferences updated",
            "learned_patterns": patterns.get("patterns", {}),
            "insights": patterns.get("insights", []),
            "session_id": session_id,
            "timestamp": time.time()
        }

        debug_log(f"Learned from user feedback for session {session_id}")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Error learning from feedback: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@mcp.tool()
def get_session_memory_stats(
    session_id: Annotated[str, Field(description="Session identifier")] = "default"
) -> str:
    """
    Get statistics tentang session memory

    Args:
        session_id: Session identifier

    Returns:
        str: JSON memory statistics
    """
    try:
        # Get session stats
        session_stats = session_memory.get_session_stats()

        # Get specific session context
        session_context = session_memory.get_conversation_context(session_id)

        # Get user preferences summary
        prefs_summary = user_preferences.get_preferences_summary()

        result = {
            "session_id": session_id,
            "session_stats": session_stats,
            "current_session_context": session_context,
            "user_preferences_summary": prefs_summary,
            "memory_health": {
                "total_sessions": session_stats["total_sessions"],
                "total_exchanges": session_stats["total_exchanges"],
                "current_session_active": session_id in session_stats["sessions"],
                "memory_usage": "healthy" if session_stats["total_sessions"] < 10 else "high"
            }
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Error getting memory stats: {str(e)}"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


# ===== Entry Point Program Utama =====
def main():
    """Entry point utama untuk eksekusi paket"""
    # Periksa apakah mode debug diaktifkan
    debug_enabled = os.getenv("MCP_DEBUG", "").lower() in ("true", "1", "yes", "on")

    if debug_enabled:
        debug_log("🚀 Memulai server MCP Koleksi Umpan Balik Interaktif")
        debug_log(f"   Nama server: {SERVER_NAME}")
        debug_log(f"   Versi: {__version__}")
        debug_log(f"   Platform: {sys.platform}")
        debug_log(f"   Inisialisasi encoding: {'Berhasil' if _encoding_initialized else 'Gagal'}")
        debug_log(f"   Lingkungan remote: {is_remote_environment()}")
        debug_log(f"   GUI tersedia: {can_use_gui()}")
        debug_log(f"   Antarmuka: Qt GUI")
        debug_log("   Menunggu panggilan dari asisten AI...")
        debug_log("Bersiap memulai server MCP...")
        debug_log("Memanggil mcp.run()...")

    try:
        # Menggunakan API FastMCP yang benar
        mcp.run()
    except KeyboardInterrupt:
        if debug_enabled:
            debug_log("Menerima sinyal interupsi, keluar normal")
        sys.exit(0)
    except Exception as e:
        if debug_enabled:
            debug_log(f"Startup server MCP gagal: {e}")
            import traceback
            debug_log(f"Error detail: {traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
