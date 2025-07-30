import sys
from .downloader import download_file, download_media_yt_dlp, download_file_threaded

def main():
    if len(sys.argv) < 2:
        print("Использование: pylink <URL> [путь_сохранения]")
        sys.exit(1)

    url = sys.argv[1]
    destination = sys.argv[2] if len(sys.argv) > 2 else url.split("/")[-1]

    # Простая проверка для видео-ссылок (можно улучшить позже)
    if "youtube.com" in url or "youtu.be" in url or "vk.com" in url or "tiktok.com" in url:
        print(f"Загрузка медиа с {url} в {destination} с помощью yt-dlp...")
        if download_media_yt_dlp(url, destination):
            print(f"Успешно загружено медиа с {url} в {destination}")
        else:
            print(f"Не удалось загрузить медиа с {url}")
    else:
        print(f"Загрузка файла с {url} в {destination} (многопоточно)... ")
        if download_file_threaded(url, destination):
            print(f"Успешно загружен файл с {url} в {destination}")
        else:
            print(f"Не удалось загрузить файл с {url}")


