import os
import time
import mimetypes
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from typing import Optional, Tuple
import yt_dlp

CHUNK_SIZE = 8192 * 4  # Увеличенный размер чанка

class Downloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    @staticmethod
    def format_size(bytes_size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"

    @staticmethod
    def format_speed(speed: float) -> str:
        return Downloader.format_size(speed) + "/s"

    @staticmethod
    def format_time(seconds: int) -> str:
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

    def get_filename_from_url(self, url: str, response: requests.Response = None) -> str:
        filename = os.path.basename(urlparse(url).path)
        if not filename or filename == '/':
            if response and 'content-disposition' in response.headers:
                content_disposition = response.headers['content-disposition']
                if 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[1].strip('"\'')
            if not filename and response and 'content-type' in response.headers:
                ext = mimetypes.guess_extension(response.headers['content-type'])
                if ext:
                    filename = f"file{ext}"
        return filename or f"download_{int(time.time())}"

    def download_chunk(self, url: str, start: int, end: int, part_file: str, progress_bar: tqdm) -> bool:
        headers = {'Range': f'bytes={start}-{end}'}
        try:
            with self.session.get(url, headers=headers, stream=True) as response:
                response.raise_for_status()
                with open(part_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                            progress_bar.update(len(chunk))
            return True
        except Exception as e:
            print(f"\nОшибка при загрузке части файла: {e}")
            return False

    def download_file_threaded(self, url: str, destination: Optional[str] = None, num_threads: int = 8) -> Tuple[bool, str]:
        try:
            with self.session.head(url, allow_redirects=True) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                supports_partial = response.headers.get('accept-ranges') == 'bytes'
                if not destination:
                    destination = self.get_filename_from_url(url, response)
                os.makedirs(os.path.dirname(destination) or ".", exist_ok=True)

            if not supports_partial or total_size < 5 * 1024 * 1024:
                return self.download_file(url, destination), destination

            with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Загрузка {os.path.basename(destination)}") as pbar:
                part_size = total_size // num_threads
                futures = []
                temp_files = []

                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    for i in range(num_threads):
                        start = i * part_size
                        end = start + part_size - 1 if i < num_threads - 1 else total_size - 1
                        part_file = f"{destination}.part{i}"
                        temp_files.append(part_file)
                        futures.append(executor.submit(self.download_chunk, url, start, end, part_file, pbar))

                    for future in as_completed(futures):
                        if not future.result():
                            for f in temp_files:
                                if os.path.exists(f):
                                    os.remove(f)
                            return False, destination

                with open(destination, 'wb') as outfile:
                    for part_file in temp_files:
                        with open(part_file, 'rb') as infile:
                            outfile.write(infile.read())
                        os.remove(part_file)

            return True, destination
        except Exception as e:
            print(f"\nОшибка при загрузке файла: {e}")
            return False, destination

    def download_file(self, url: str, destination: Optional[str] = None) -> bool:
        try:
            with self.session.get(url, stream=True) as response:
                response.raise_for_status()
                if not destination:
                    destination = self.get_filename_from_url(url, response)
                total_size = int(response.headers.get('content-length', 0))
                os.makedirs(os.path.dirname(destination) or ".", exist_ok=True)

                with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Загрузка {os.path.basename(destination)}") as pbar:
                    with open(destination, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
            return True
        except Exception as e:
            print(f"\nОшибка при загрузке файла: {e}")
            return False

    def download_media(self, url: str, destination: Optional[str] = None) -> Tuple[bool, str]:
        class YTDLPProgressHook:
            def __init__(self):
                self.pbar = None

            def __call__(self, d):
                if d['status'] == 'downloading':
                    if self.pbar is None:
                        self.pbar = tqdm(
                            total=d.get('total_bytes') or d.get('total_bytes_estimate'),
                            unit='B',
                            unit_scale=True,
                            desc="Загрузка медиа"
                        )
                    self.pbar.n = d.get('downloaded_bytes', 0)
                    self.pbar.set_postfix({
                        'speed': Downloader.format_speed(d.get('speed', 0)),
                        'ETA': Downloader.format_time(d.get('eta', 0))
                    })
                    self.pbar.refresh()
                elif d['status'] == 'finished':
                    if self.pbar:
                        self.pbar.close()
                        self.pbar = None
                elif d['status'] == 'error' and self.pbar:
                    self.pbar.close()
                    self.pbar = None

        opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True,
        }

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)

                title = info.get("title", "Без названия")
                filesize = info.get("filesize") or info.get("filesize_approx") or 0
                ext = info.get("ext", "mp4")
                format_note = info.get("format_note", "")
                resolution = info.get("height", "")
                final_size = self.format_size(filesize)

                print(f"\n📹 Видео: {title}")
                print(f"📦 Формат: {format_note} | {resolution}p | {ext}")
                print(f"💾 Размер: {final_size}")

                choice = input("✅ Начать загрузку? (да/нет): ").strip().lower()
                if choice not in ['да', 'y', 'yes']:
                    print("🚫 Загрузка отменена.")
                    return False, ""

                # Формируем безопасное имя файла
                if destination is None:
                    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '.', '_')).rstrip()
                    destination = os.path.join(os.getcwd(), f"{safe_title}.{ext}")

                opts.update({
                    'outtmpl': destination,
                    'progress_hooks': [YTDLPProgressHook()],
                })

                with yt_dlp.YoutubeDL(opts) as ydl_with_download:
                    ydl_with_download.download([url])

                return True, destination

        except Exception as e:
            print(f"\n❌ Ошибка при загрузке медиа: {e}")
            return False, destination or ""