#!/usr/bin/env python3
"""
Простой HTTP-сервер для скачивания файла.
При обращении на порт 80 клиент получает указанный файл с заголовком Content-Disposition.
"""

import os
import sys
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler

class DownloadHandler(SimpleHTTPRequestHandler):
    """Обработчик запросов, всегда отдающий один и тот же файл для скачивания."""

    # Имя файла, который будет передан клиенту (устанавливается в main)
    file_to_serve = None

    def do_GET(self):
        """Обрабатываем GET-запрос: отдаём файл на скачивание."""
        if not self.file_to_serve or not os.path.isfile(self.file_to_serve):
            self.send_error(404, "File not found or not configured")
            return

        try:
            # Открываем файл в бинарном режиме
            with open(self.file_to_serve, 'rb') as f:
                content = f.read()

            # Отправляем заголовки
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            # Предлагаем сохранить файл с оригинальным именем
            filename = os.path.basename(self.file_to_serve)
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()

            # Отправляем тело файла
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")

    def log_message(self, format, *args):
        """Необязательно: кастомизируем вывод логов в консоль."""
        sys.stderr.write("%s - - [%s] %s\n" % (
            self.address_string(),
            self.log_date_time_string(),
            format % args
        ))

def main():
    parser = argparse.ArgumentParser(description='Сервер для скачивания файла через HTTP на порту 80')
    parser.add_argument('file', help='Путь к файлу, который будет отдаваться при запросе')
    parser.add_argument('--host', default='0.0.0.0', help='Хост для прослушивания (по умолчанию 0.0.0.0)')
    parser.add_argument('--port', type=int, default=80, help='Порт (по умолчанию 80)')
    args = parser.parse_args()

    # Проверяем, существует ли указанный файл
    if not os.path.isfile(args.file):
        print(f"Ошибка: файл '{args.file}' не найден.", file=sys.stderr)
        sys.exit(1)

    # Передаём имя файла обработчику
    DownloadHandler.file_to_serve = args.file

    # Создаём сервер
    server = HTTPServer((args.host, args.port), DownloadHandler)
    print(f"Сервер запущен на {args.host}:{args.port}")
    print(f"Файл '{args.file}' будет отдаваться на любой GET-запрос.")
    print("Нажмите Ctrl+C для остановки.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
        server.server_close()

if __name__ == '__main__':
    # Для Windows может потребоваться запуск с правами администратора,
    # для Linux/macOS – с sudo (из-за порта 80)
    if os.name == 'nt' and sys.argv[0]:
        # На Windows порт 80 часто занят, предупреждаем
        print("Внимание: на Windows порт 80 может быть занят системой.\n"
              "Попробуйте запустить от имени администратора или используйте другой порт.", file=sys.stderr)
    elif os.name != 'nt' and os.geteuid() != 0:
        print("Внимание: для использования порта 80 на Unix-подобных системах требуются права root.\n"
              "Попробуйте запустить с sudo.", file=sys.stderr)

    main()
