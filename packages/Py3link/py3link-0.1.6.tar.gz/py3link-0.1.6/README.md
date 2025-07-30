
# Py3Link

PyLink is a powerful and beautiful Python library for downloading files and videos from various sources, with multi-threading support and elegant progress bars.



## Установка

```bash
pip install pylink
```

## Использование

### Загрузка файлов

Для загрузки файлов используйте команду `pylink` с URL-адресом файла. Вы можете указать необязательный путь для сохранения файла.

```bash
pylink https://example.com/some_file.zip
pylink https://example.com/another_file.pdf my_document.pdf
```

### Загрузка видео с YouTube, VK, TikTok и других платформ

PyLink автоматически определяет, является ли ссылка видео с поддерживаемой платформы (YouTube, VK, TikTok и т.д.) и использует `yt-dlp` для загрузки.

```bash
pylink https://www.youtube.com/watch?v=dQw4w9WgXcQ
pylink https://vk.com/video-12345678_456239017
pylink https://www.tiktok.com/@username/video/1234567890123456789
```

### Прогресс-бары

Во время загрузки PyLink отображает красивый прогресс-бар, показывающий текущий объем загруженных данных, общий размер файла, скорость загрузки и предполагаемое время завершения.

## Разработка

### Структура проекта

```
pylink/
├── pylink/
│   ├── __init__.py
│   ├── cli.py
│   └── downloader.py
├── docs/
│   └── usage.md
├── setup.py
└── README.md
```

### Модули

-   `cli.py`: Точка входа для командной строки, обрабатывает аргументы и вызывает функции загрузки.
-   `downloader.py`: Содержит логику загрузки файлов (прямые ссылки) и медиа (с использованием `yt-dlp`), а также управление прогресс-барами и многопоточностью.

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности смотрите в файле `LICENSE` (будет добавлен).


