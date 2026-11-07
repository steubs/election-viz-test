from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import Base, engine
from .routes import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)  # swap for Alembic migrations once the schema settles
    yield


app = FastAPI(title="Election Viz API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=["GET"])
app.include_router(router, prefix="/api")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
