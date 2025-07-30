import os
import sys
import requests
import yt_dlp
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import time
import mimetypes
from typing import Optional, Tuple

CHUNK_SIZE = 8192 * 4  # Увеличенный размер чанка для лучшей производительности

class Downloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    @staticmethod
    def format_size(bytes_size: int) -> str:
        """Форматирует размер файла в читаемый вид"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"

    @staticmethod
    def format_speed(speed: float) -> str:
        """Форматирует скорость загрузки"""
        return Downloader.format_size(speed) + "/s"

    @staticmethod
    def format_time(seconds: int) -> str:
        """Форматирует время в ЧЧ:ММ:СС"""
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

    def get_filename_from_url(self, url: str, response: requests.Response = None) -> str:
        """Определяет имя файла из URL или заголовков ответа"""
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
        
        if not filename:
            filename = f"download_{int(time.time())}"
            
        return filename

    def download_chunk(self, url: str, start: int, end: int, part_file: str, progress_bar: tqdm) -> bool:
        """Загружает часть файла"""
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
        """Многопоточная загрузка файла"""
        try:
            # Получаем информацию о файле
            with self.session.head(url, allow_redirects=True) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                supports_partial = response.headers.get('accept-ranges') == 'bytes'
                
                if not destination:
                    destination = self.get_filename_from_url(url, response)
                
                # Создаем папку если нужно
                os.makedirs(os.path.dirname(destination), exist_ok=True)

            # Если файл не поддерживает частичную загрузку или слишком мал
            if not supports_partial or total_size < 1024 * 1024 * 5:  # < 5MB
                return self.download_file(url, destination), destination

            # Настраиваем прогресс-бар
            with tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=f"Загрузка {os.path.basename(destination)}",
                ascii=True,
                dynamic_ncols=True
            ) as pbar:
                # Разделяем файл на части
                part_size = total_size // num_threads
                futures = []
                temp_files = []
                
                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    for i in range(num_threads):
                        start = i * part_size
                        end = start + part_size - 1 if i < num_threads - 1 else total_size - 1
                        part_file = f"{destination}.part{i}"
                        temp_files.append(part_file)
                        
                        futures.append(
                            executor.submit(
                                self.download_chunk,
                                url, start, end, part_file, pbar
                            )
                        )
                    
                    # Проверяем результаты
                    for future in as_completed(futures):
                        if not future.result():
                            # Если хотя бы одна часть не загрузилась, отменяем все
                            for f in temp_files:
                                if os.path.exists(f):
                                    os.remove(f)
                            return False, destination

                # Собираем части в один файл
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
        """Однопоточная загрузка файла"""
        try:
            with self.session.get(url, stream=True) as response:
                response.raise_for_status()
                
                if not destination:
                    destination = self.get_filename_from_url(url, response)
                
                total_size = int(response.headers.get('content-length', 0))
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                
                with tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=f"Загрузка {os.path.basename(destination)}",
                    ascii=True,
                    dynamic_ncols=True
                ) as pbar:
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
        """Загрузка медиа через yt-dlp"""
        class YTDLPProgressHook:
            def __init__(self):
                self.pbar = None
                self.last_update = 0
                
            def __call__(self, d):
                if d['status'] == 'downloading':
                    if self.pbar is None:
                        self.pbar = tqdm(
                            total=d.get('total_bytes') or d.get('total_bytes_estimate'),
                            unit='B',
                            unit_scale=True,
                            unit_divisor=1024,
                            desc="Загрузка медиа",
                            ascii=True,
                            dynamic_ncols=True
                        )
                    
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                    speed = d.get('speed', 0)
                    eta = d.get('eta', 0)
                    
                    self.pbar.total = total
                    self.pbar.n = downloaded
                    self.pbar.set_postfix({
                        'speed': Downloader.format_speed(speed),
                        'ETA': Downloader.format_time(eta)
                    })
                    self.pbar.refresh()
                    
                elif d['status'] == 'finished':
                    if self.pbar:
                        self.pbar.close()
                        self.pbar = None
                    print("\nЗагрузка завершена!")
                    
                elif d['status'] == 'error':
                    if self.pbar:
                        self.pbar.close()
                        self.pbar = None
                    print("\nОшибка загрузки!")

        ydl_opts = {
            'outtmpl': destination or '%(title)s.%(ext)s',
            'progress_hooks': [YTDLPProgressHook()],
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
            'merge_output_format': 'mp4',
            'noplaylist': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if destination is None:
                    destination = ydl.prepare_filename(info)
            return True, destination
        except Exception as e:
            print(f"\nОшибка при загрузке медиа: {e}")
            return False, destination

def main():
    if len(sys.argv) < 2:
        print("Использование: python downloader.py <URL> [путь_сохранения]")
        print("Поддерживаемые платформы: YouTube, VK, TikTok, Instagram и другие")
        sys.exit(1)

    url = sys.argv[1]
    destination = sys.argv[2] if len(sys.argv) > 2 else None
    
    downloader = Downloader()
    
    # Определяем тип загрузки
    if any(domain in url for domain in [
        'youtube.com', 'youtu.be', 
        'vk.com', 'tiktok.com', 
        'instagram.com', 'fb.watch'
    ]):
        print(f"\nЗагрузка медиа с {url}")
        success, output_path = downloader.download_media(url, destination)
    else:
        print(f"\nЗагрузка файла с {url}")
        success, output_path = downloader.download_file_threaded(url, destination)
    
    if success:
        print(f"\nУспешно загружено в: {output_path}")
        print(f"Размер файла: {Downloader.format_size(os.path.getsize(output_path))}")
    else:
        print("\nЗагрузка не удалась!")

if __name__ == "__main__":
    main()