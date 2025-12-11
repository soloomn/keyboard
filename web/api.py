"""
Модуль API для сервиса анализа клавиатурных раскладок.

Содержит эндпоинты FastAPI для управления процессом анализа,
загрузки файлов, отслеживания статуса задач и отображения
веб-страниц с результатами анализа.

Основные возможности:
- Загрузка и обработка файлов для анализа
- Управление фоновыми задачами анализа
- Отслеживание статуса выполнения задач
- Отображение веб-интерфейса (HTML, CSS, JavaScript)
- Хранение и получение данных через Redis

Используемые библиотеки:
- FastAPI для создания REST API
- Redis для хранения данных и состояния
- uuid для генерации уникальных идентификаторов задач

ВХОД:
    API принимает HTTP-запросы через различные эндпоинты:
    - GET-запросы для получения страниц и ресурсов
    - POST-запросы для загрузки файлов и данных

ВЫХОД:
    API возвращает различные HTTP-ответы:
    - HTML-страницы для веб-интерфейса
    - JSON-ответы с данными и статусами
    - Статические файлы (CSS, JavaScript)
"""

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import os
import uuid

from models import RedisStorage

app = FastAPI(title="Keyboard Analyzer API")

# Настройка путей к статическим файлам
STATIC_DIR = os.getenv("STATIC_DIR")
CSS_DIR = os.getenv("CSS_DIR")
JS_DIR = os.getenv("JS_DIR")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(CSS_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Инициализация хранилища Redis
storage = RedisStorage()

# Ключи в Redis (определены через переменные окружения)
CONTROL_KEY = os.getenv("CONTROL_KEY")
DATA_KEY = os.getenv("DATA_KEY")
FILENAMES_KEY = os.getenv("FILENAMES_KEY")


def _job_status_key(job_id: str) -> str:
    """
    Генерирует ключ Redis для хранения статуса задачи.

    ВХОД:
        job_id (str): Уникальный идентификатор задачи

    ВЫХОД:
        str: Строка ключа Redis в формате "job:{job_id}:status"
    """
    return f"job:{job_id}:status"


@app.get("/")
async def root():
    """
    Главная страница веб-интерфейса.

    ВХОД:
        None (GET-запрос без параметров)

    ВЫХОД:
        FileResponse: HTML-файл главной страницы
    """
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/index.html")
async def root():
    """
    Альтернативный маршрут к главной странице.

    ВХОД:
        None (GET-запрос без параметров)

    ВЫХОД:
        FileResponse: HTML-файл главной страницы
    """
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/css/main.css")
async def root_sheets():
    """
    Основные стили CSS для главной страницы.

    ВХОД:
        None (GET-запрос без параметров)

    ВЫХОД:
        FileResponse: CSS-файл стилей
    """
    return FileResponse(os.path.join(CSS_DIR, "main.css"))


@app.get("/js/main.js")
async def root_scripts():
    """
    Основные JavaScript скрипты для главной страницы.

    ВХОД:
        None (GET-запрос без параметров)

    ВЫХОД:
        FileResponse: JavaScript файл
    """
    return FileResponse(os.path.join(JS_DIR, "main.js"))


@app.get("/analysis.html")
async def analysis():
    """
    Страница анализа клавиатурных раскладок.

    ВХОД:
        None (GET-запрос без параметров)

    ВЫХОД:
        FileResponse: HTML-файл страницы анализа
    """
    return FileResponse(os.path.join(STATIC_DIR, "analysis.html"))


@app.get("/css/analysis.css")
async def analysis_sheets():
    """
    Стили CSS для страницы анализа.

    ВХОД:
        None (GET-запрос без параметров)

    ВЫХОД:
        FileResponse: CSS-файл стилей для анализа
    """
    return FileResponse(os.path.join(CSS_DIR, "analysis.css"))


@app.get("/js/analysis.js")
async def analysis_scripts():
    """
    JavaScript скрипты для страницы анализа.

    ВХОД:
        None (GET-запрос без параметров)

    ВЫХОД:
        FileResponse: JavaScript файл для анализа
    """
    return FileResponse(os.path.join(JS_DIR, "analysis.js"))


@app.get("/statistics.html")
async def statistics():
    """
    Страница статистики и визуализации результатов.

    ВХОД:
        None (GET-запрос без параметров)

    ВЫХОД:
        FileResponse: HTML-файл страницы статистики
    """
    return FileResponse(os.path.join(STATIC_DIR, "statistics.html"))


@app.get("/css/statistics.css")
async def statistics_sheets():
    """
    Стили CSS для страницы статистики.

    ВХОД:
        None (GET-запрос без параметров)

    ВЫХОД:
        FileResponse: CSS-файл стилей для статистики
    """
    return FileResponse(os.path.join(CSS_DIR, "statistics.css"))


@app.get("/js/statistics.js")
async def statistics_scripts():
    """
    JavaScript скрипты для страницы статистики.

    ВХОД:
        None (GET-запрос без параметров)

    ВЫХОД:
        FileResponse: JavaScript файл для статистики
    """
    return FileResponse(os.path.join(JS_DIR, "statistics.js"))


@app.post("/analyze")
async def start_analysis(background_tasks: BackgroundTasks,
        files: List[UploadFile] = File(...),):
    """
    Запускает процесс анализа загруженных файлов.

    ВХОД:
        background_tasks (BackgroundTasks): Объект для управления фоновыми задачами
        files (List[UploadFile]): Список загружаемых файлов для анализа

    ВЫХОД:
        JSONResponse: Содержит job_id и начальный статус задачи

    Действия функции:
        - Генерирует уникальный идентификатор задачи
        - Сохраняет загруженные файлы во временную директорию
        - Сохраняет пути к файлам в Redis
        - Устанавливает статус задачи как "queued"
        - Активирует флаг для запуска анализатора
    """
    if not files:
        return JSONResponse({"error": "no files uploaded"}, status_code=400)

    job_id = str(uuid.uuid4())

    # Сохраняем файлы во временную директорию
    tmp_dir = "/app/uploads"
    os.makedirs(tmp_dir, exist_ok=True)

    filenames = []
    for uf in files:
        path = os.path.join(tmp_dir, uf.filename)
        with open(path, "wb") as f:
            f.write(uf.file.read())
        filenames.append(path)

    # Записываем пути файлов в Redis для analyzer
    storage.save(FILENAMES_KEY, filenames)

    # записываем job_id в Redis
    storage.save("control:current_job_id", job_id)

    # Ставим статус "queued"
    storage.save(f"job:{job_id}:status", "queued")

    # Даём разрешение analyzer'у на запуск
    storage.save(CONTROL_KEY, "ready")

    return {"job_id": job_id, "status": "queued"}


@app.post("/metrics")
async def metrics(request: Request,
                  background_tasks: BackgroundTasks):
    """
    Принимает метрики анализа для сохранения в хранилище.

    ВХОД:
        request (Request): HTTP-запрос с данными метрик
        background_tasks (BackgroundTasks): Объект для управления фоновыми задачами

    ВЫХОД:
        JSONResponse: Подтверждение получения данных или ошибку

    Действия функции:
        - Читает сырые данные из запроса
        - Декодирует данные в UTF-8
        - Сохраняет данные в Redis
    """
    raw = await request.body()
    data = raw.decode("utf-8") if raw is not None else ""
    if not data.strip():
        return JSONResponse({"error": "no data uploaded"}, status_code=400)

    storage.save(DATA_KEY, data)
    return JSONResponse({"data": data}, status_code=200)


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """
    Возвращает текущий статус задачи анализа.

    ВХОД:
        job_id (str): Уникальный идентификатор задачи

    ВЫХОД:
        JSONResponse: Содержит job_id и текущий статус задачи

    Возможные статусы:
        - "queued": задача в очереди
        - "running": задача выполняется
        - "finished": задача завершена
        - "error:...": ошибка выполнения с описанием
    """
    status = storage.load(_job_status_key(job_id))
    if status is None:
        # Если статус не найден, проверяем общий флаг
        control = storage.load(CONTROL_KEY)
        if control == "ready":
            status = "queued"
        else:
            return JSONResponse({"error": "job not found"}, status_code=404)

    return {"job_id": job_id, "status": status}


# Дополнительные эндпоинты для ручного управления
@app.post("/control/enable")
async def enable_analysis():
    """
    Вручную разрешает запуск анализа.

    ВХОД:
        None (POST-запрос без тела)

    ВЫХОД:
        JSONResponse: Подтверждение установки флага
    """
    storage.save(CONTROL_KEY, "ready")
    return {"status": "ok", "value": "ready"}


@app.post("/control/disable")
async def disable_analysis():
    """
    Вручную запрещает автозапуск анализа.

    ВХОД:
        None (POST-запрос без тела)

    ВЫХОД:
        JSONResponse: Подтверждение установки флага
    """
    storage.save(CONTROL_KEY, "blocked")
    return {"status": "ok", "value": "blocked"}