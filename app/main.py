"""FastAPIアプリケーションのエントリポイント。"""

from fastapi import FastAPI

from app.routers import hello1

app = FastAPI()

app.include_router(hello1.router)
