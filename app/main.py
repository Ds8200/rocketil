import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.routes import health, ws
from app.core.poller import poll_loop

from pathlib import Path

path_current = Path(__file__).parent
path_dashboard = path_current / "templates" / "dashboard.html"


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(poll_loop())
    yield
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)


app = FastAPI(title="RocketIL Dashboard", lifespan=lifespan)

app.include_router(ws.router)
app.include_router(health.router)


@app.get("/")
async def dashboard() -> FileResponse:
    try:
        return FileResponse(path_dashboard)
    except FileNotFoundError:
        return {"error": "Dashboard file not found" }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
