#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Interactive Feedback Enhanced - Entry Point Program Utama
=============================================================

File ini memungkinkan paket dijalankan melalui `python -m mcp_ngobrol`.

Cara Penggunaan:
  python -m mcp_ngobrol        # Memulai server MCP
  python -m mcp_ngobrol test   # Menjalankan testing
"""

import sys
import argparse
import os

def main():
    """Entry point program utama"""
    parser = argparse.ArgumentParser(
        description="MCP Ngobrol - Server MCP Koleksi Umpan Balik Interaktif"
    )

    subparsers = parser.add_subparsers(dest='command', help='Perintah yang tersedia')

    # Perintah server (default)
    server_parser = subparsers.add_parser('server', help='Memulai server MCP (default)')

    # Perintah testing
    test_parser = subparsers.add_parser('test', help='Menjalankan testing')
    test_parser.add_argument('--gui', action='store_true', help='Test Qt GUI (test cepat)')
    test_parser.add_argument('--enhanced', action='store_true', help='Jalankan test MCP enhanced (direkomendasikan)')
    test_parser.add_argument('--scenario', help='Jalankan skenario test tertentu')
    test_parser.add_argument('--tags', help='Jalankan skenario test berdasarkan tag (dipisah koma)')
    test_parser.add_argument('--list-scenarios', action='store_true', help='Daftar semua skenario test yang tersedia')
    test_parser.add_argument('--report-format', choices=['html', 'json', 'markdown'], help='Format laporan')
    test_parser.add_argument('--timeout', type=int, help='Waktu timeout test (detik)')

    # Perintah GUI (default)
    gui_parser = subparsers.add_parser('gui', help='Buka GUI interface (default)')
    gui_parser.add_argument('--debug', action='store_true', help='Aktifkan mode debug')

    # Perintah versi
    version_parser = subparsers.add_parser('version', help='Tampilkan informasi versi')
    
    args = parser.parse_args()
    
    if args.command == 'test':
        run_tests(args)
    elif args.command == 'version':
        show_version()
    elif args.command == 'server':
        run_server()
    elif args.command == 'gui':
        run_gui(args)
    elif args.command is None:
        # Default: buka GUI
        run_gui(argparse.Namespace(debug=False))
    else:
        # Seharusnya tidak sampai di sini
        parser.print_help()
        sys.exit(1)

def run_server():
    """Memulai server MCP"""
    from .server import main as server_main
    return server_main()

def run_gui(args):
    """Menjalankan GUI interface"""
    if args.debug:
        os.environ["MCP_DEBUG"] = "true"

    print("🎨 Membuka MCP Ngobrol GUI...")
    from .test_qt_gui import test_qt_gui
    return test_qt_gui()

def run_tests(args):
    """Menjalankan testing"""
    # Aktifkan mode debug untuk menampilkan proses testing
    os.environ["MCP_DEBUG"] = "true"

    if args.enhanced or args.scenario or args.tags or args.list_scenarios:
        # Gunakan sistem testing enhanced baru
        print("🚀 Menjalankan sistem testing MCP enhanced...")
        import asyncio
        from .test_mcp_enhanced import MCPTestRunner, TestConfig

        # Buat konfigurasi
        config = TestConfig.from_env()
        if args.timeout:
            config.test_timeout = args.timeout
        if args.report_format:
            config.report_format = args.report_format

        runner = MCPTestRunner(config)

        async def run_enhanced_tests():
            try:
                if args.list_scenarios:
                    # Daftar skenario testing
                    tags = args.tags.split(',') if args.tags else None
                    runner.list_scenarios(tags)
                    return True

                success = False

                if args.scenario:
                    # Jalankan skenario tertentu
                    success = await runner.run_single_scenario(args.scenario)
                elif args.tags:
                    # Jalankan berdasarkan tag
                    tags = [tag.strip() for tag in args.tags.split(',')]
                    success = await runner.run_scenarios_by_tags(tags)
                else:
                    # Jalankan semua skenario
                    success = await runner.run_all_scenarios()

                return success

            except Exception as e:
                print(f"❌ Eksekusi testing enhanced gagal: {e}")
                return False

        success = asyncio.run(run_enhanced_tests())
        if not success:
            sys.exit(1)

    elif args.gui:
        print("🧪 Menjalankan testing Qt GUI...")
        from .test_qt_gui import test_qt_gui
        if not test_qt_gui():
            sys.exit(1)
    else:
        # Default menjalankan testing cepat sistem enhanced
        print("🧪 Menjalankan suite testing cepat (menggunakan sistem testing enhanced)...")
        print("💡 Tips: Gunakan parameter --enhanced untuk menjalankan testing lengkap")

        import asyncio
        from .test_mcp_enhanced import MCPTestRunner, TestConfig

        config = TestConfig.from_env()
        config.test_timeout = 60  # Testing cepat menggunakan timeout lebih pendek

        runner = MCPTestRunner(config)

        async def run_quick_tests():
            try:
                # Jalankan tag testing cepat
                success = await runner.run_scenarios_by_tags(["quick"])
                return success
            except Exception as e:
                print(f"❌ Eksekusi testing cepat gagal: {e}")
                return False

        success = asyncio.run(run_quick_tests())
        if not success:
            sys.exit(1)

        print("🎉 Testing cepat berhasil!")
        print("💡 Gunakan 'test --enhanced' untuk menjalankan suite testing lengkap")

def show_version():
    """Tampilkan informasi versi"""
    from . import __version__, __author__
    print(f"MCP Ngobrol v{__version__}")
    print(f"Penulis: {__author__}")
    print("GitHub: https://github.com/mbprcc/mcp-ngobrol")

if __name__ == "__main__":
    main() 