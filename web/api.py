from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import os
import uuid

from models import RedisStorage

app = FastAPI(title="Keyboard Analyzer API")

STATIC_DIR = os.getenv("STATIC_DIR")
CSS_DIR = os.getenv("CSS_DIR")
JS_DIR = os.getenv("JS_DIR")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(CSS_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

storage = RedisStorage()

# Ключи в Redis
CONTROL_KEY = os.getenv("CONTROL_KEY")
DATA_KEY = os.getenv("DATA_KEY")
FILENAMES_KEY = os.getenv("FILENAMES_KEY")


def _job_status_key(job_id: str) -> str:
    return f"job:{job_id}:status"


@app.get("/")
async def root():
    """Главная страница."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/index.html")
async def root():
    """Главная страница."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/css/main.css")
async def root_sheets():
    """Главная страница стили."""
    return FileResponse(os.path.join(CSS_DIR, "main.css"))

@app.get("/js/main.js")
async def root_scripts():
    """Главная страница скрипты."""
    return FileResponse(os.path.join(JS_DIR, "main.js"))


@app.get("/analysis.html")
async def analysis():
    """Страница анализа."""
    return FileResponse(os.path.join(STATIC_DIR, "analysis.html"))

@app.get("/css/analysis.css")
async def analysis_sheets():
    """Страница анализа стили."""
    return FileResponse(os.path.join(CSS_DIR, "analysis.css"))

@app.get("/js/analysis.js")
async def analysis_scripts():
    """Страница анализа скрипты."""
    return FileResponse(os.path.join(JS_DIR, "analysis.js"))

@app.get("/statistics.html")
async def statistics():
    """Страница статистики."""
    return FileResponse(os.path.join(STATIC_DIR, "statistics.html"))

@app.get("/css/statistics.css")
async def statistics_sheets():
    """Страница статистики стили."""
    return FileResponse(os.path.join(CSS_DIR, "statistics.css"))

@app.get("/js/statistics.js")
async def statistics_scripts():
    """Страница статистики скрипты."""
    return FileResponse(os.path.join(JS_DIR, "statistics.js"))

@app.post("/analyze")
async def start_analysis(background_tasks: BackgroundTasks,
        files: List[UploadFile] = File(...),):
    """
    Принимает файлы, сохраняет их, пишет пути в Redis,
    даёт сигнал analyzer'у на запуск.
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
async def metrics(data: str):
    if not data:
        return JSONResponse({"error": "no data uploaded"}, status_code=400)

    storage.save(DATA_KEY, data)
    return JSONResponse({"data": data}, status_code=200)

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """
    Возвращает текущий статус анализа.
    queued / running / finished / error:...
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
    """Вручную разрешить запуск анализа."""
    storage.save(CONTROL_KEY, "ready")
    return {"status": "ok", "value": "ready"}


@app.post("/control/disable")
async def disable_analysis():
    """Вручную запретить автозапуск анализа."""
    storage.save(CONTROL_KEY, "blocked")
    return {"status": "ok", "value": "blocked"}



