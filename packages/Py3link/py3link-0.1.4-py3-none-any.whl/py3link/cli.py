import sys
import os
from downloader import Downloader

def main():
    if len(sys.argv) < 2:
        print("Использование: python main.py <URL> [путь_сохранения]")
        print("Поддерживаемые платформы: YouTube, VK, TikTok, Instagram и другие")
        sys.exit(1)

    url = sys.argv[1]
    destination = sys.argv[2] if len(sys.argv) > 2 else None
    downloader = Downloader()

    if any(site in url for site in ['youtube.com', 'youtu.be', 'vk.com', 'tiktok.com', 'instagram.com', 'fb.watch']):
        print(f"\nЗагрузка медиа с {url}")
        success, path = downloader.download_media(url, destination)
    else:
        print(f"\nЗагрузка файла с {url}")
        success, path = downloader.download_file_threaded(url, destination)

    if success:
        print(f"\n✅ Успешно загружено: {path}")
        print(f"📦 Размер: {Downloader.format_size(os.path.getsize(path))}")
    else:
        print(f"\n❌ Не удалось загрузить: {url}")

if __name__ == "__main__":
    main()