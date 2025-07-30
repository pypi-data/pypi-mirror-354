import requests
import yt_dlp
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import os

CHUNK_SIZE = 8192

def download_file_threaded(url, destination, num_threads=5):
    try:
        response = requests.head(url, allow_redirects=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))

        if total_size == 0:
            print(f"Не удалось определить размер файла для {url}. Загрузка без прогресс-бара.")
            return download_file(url, destination) # Fallback to single-threaded if size unknown

        # Initialize tqdm outside to be shared
        with tqdm(total=total_size, unit="B", unit_scale=True, desc=f"Загрузка {os.path.basename(destination)}", leave=True) as pbar:
            # Create a partial download function
            def download_range(start, end, part_num):
                headers = {"Range": f"bytes={start}-{end}"}
                part_file_path = f"{destination}.part{part_num}"
                try:
                    part_response = requests.get(url, headers=headers, stream=True)
                    part_response.raise_for_status()
                    with open(part_file_path, "wb") as f:
                        for chunk in part_response.iter_content(chunk_size=CHUNK_SIZE):
                            f.write(chunk)
                            pbar.update(len(chunk)) # Update shared progress bar
                    return True
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка при загрузке части {part_num} из {url}: {e}")
                    return False
                except Exception as e:
                    print(f"Произошла непредвиденная ошибка при загрузке части {part_num}: {e}")
                    return False

            # Divide the file into chunks for multi-threaded download
            chunk_size_per_thread = total_size // num_threads
            ranges = []
            for i in range(num_threads):
                start = i * chunk_size_per_thread
                end = start + chunk_size_per_thread - 1
                if i == num_threads - 1:  # Last chunk takes the rest
                    end = total_size - 1
                ranges.append((start, end, i))

            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(download_range, r[0], r[1], r[2]) for r in ranges]
                for future in futures:
                    if not future.result(): # Check if any part failed
                        print("Загрузка отменена из-за ошибки в одной из частей.")
                        # Clean up partial files if download fails
                        for i in range(num_threads):
                            part_file_path = f"{destination}.part{i}"
                            if os.path.exists(part_file_path):
                                os.remove(part_file_path)
                        return False

        # Reassemble the parts
        with open(destination, "wb") as outfile:
            for i in range(num_threads):
                part_file_path = f"{destination}.part{i}"
                with open(part_file_path, "rb") as infile:
                    outfile.write(infile.read())
                os.remove(part_file_path) # Clean up part files
        return True

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при многопоточной загрузке {url}: {e}")
        return False
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return False

def download_file(url, destination):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))

        with open(destination, "wb") as f:
            with tqdm(total=total_size, unit="B", unit_scale=True, desc=f"Загрузка {os.path.basename(destination)}", leave=True) as pbar:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
                    pbar.update(len(chunk))
        return True
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return False

def download_media_yt_dlp(url, destination):
    class TqdmProgressBar(tqdm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.last_downloaded_bytes = 0

        def hook(self, d):
            if d["status"] == "downloading":
                total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                downloaded_bytes = d.get("downloaded_bytes", 0)
                speed = d.get("speed") # bytes/sec
                eta = d.get("eta") # seconds

                if total_bytes > 0:
                    self.total = total_bytes
                self.update(downloaded_bytes - self.n)

                # Update description with speed and ETA if available
                desc_parts = [f"Загрузка {os.path.basename(destination)}"]
                if speed is not None:
                    desc_parts.append(f"{self.format_sizeof(speed)}/s")
                if eta is not None: # Only show ETA if speed is also available
                    desc_parts.append(f"ETA: {self.format_eta(eta)}")
                self.set_description(" ".join(desc_parts))

            elif d["status"] == "finished":
                self.update(self.total - self.n)
                # Check if 'filename' key exists before accessing it
                filename = d.get("filename", "Неизвестный файл")
                print(f"\nГотово: {filename}")
            elif d["status"] == "error":
                print(f"\nОшибка при загрузке: {d.get("error", "Неизвестная ошибка")}")

        def format_sizeof(self, num, suffix=\'B\'):
            for unit in [\'\',\'Ki\',\'Mi\',\'Gi\',\'Ti\',\'Pi\',\'Ei\',\'Zi\']:
                if abs(num) < 1024.0:
                    return f"{num:3.1f}{unit}{suffix}"
                num /= 1024.0
            return f"{num:.1f}Yi{suffix}"

        def format_eta(self, seconds):
            if seconds is None:
                return "N/A"
            minutes, seconds = divmod(int(seconds), 60)
            hours, minutes = divmod(minutes, 60)
            if hours > 0:
                return f"{hours:d}ч {minutes:02d}м {seconds:02d}с"
            elif minutes > 0:
                return f"{minutes:d}м {seconds:02d}с"
            else:
                return f"{seconds:d}с"


    ydl_opts = {
        \'outtmpl\': destination,
        \'noplaylist\': True,
        \'quiet\': True,
        \'no_warnings\': True,
        \'progress_hooks\': [TqdmProgressBar(unit=\'B\', unit_scale=True, desc=f"Загрузка {os.path.basename(destination)}").hook],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"Ошибка при загрузке медиа с {url} с помощью yt-dlp: {e}")
        return False


