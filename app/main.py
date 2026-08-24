"""FastAPIアプリケーションのエントリポイント。"""

from fastapi import FastAPI

from app.routers import hello1, hello2

app = FastAPI()

app.include_router(hello1.router)
app.include_router(hello2.router)
