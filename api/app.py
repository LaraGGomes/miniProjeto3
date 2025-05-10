from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_db
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=router, prefix="/api")


@app.get("/")
def base():
    return {"Hello": "World"}
