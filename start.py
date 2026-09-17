import http.server
import socketserver
import threading
import webbrowser
import os
import sys
import time

PORT = 8080


def get_base_dir():
    """Папка, где искать assets."""
    if getattr(sys, 'frozen', False):
        # Запущено из exe (PyInstaller распаковывает во _MEIPASS)
        return getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()
DIRECTORY = os.path.join(BASE_DIR, "assets", "code")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        pass


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def open_browser():
    time.sleep(1)
    webbrowser.open(f"http://localhost:{PORT}/index.html")


def main():
    if not os.path.isdir(DIRECTORY):
        print(f"Ошибка: не найдена папка {DIRECTORY}")
        input("Enter для выхода...")
        return

    threading.Thread(target=open_browser, daemon=True).start()

    with ReusableTCPServer(("", PORT), Handler) as httpd:
        print("=" * 50)
        print("  Презентация запущена!")
        print(f"  http://localhost:{PORT}/index.html")
        print("  НЕ ЗАКРЫВАЙ ЭТО ОКНО во время показа.")
        print("=" * 50)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
