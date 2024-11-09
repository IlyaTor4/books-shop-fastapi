from fastapi import FastAPI

from authentication import TokenValidationMiddleware
from core.config import Settings
from starlette.middleware.cors import CORSMiddleware

from core.database import Base, engine

from books.routes.books_router import book_router

Base.metadata.create_all(bind=engine)

settings = Settings()
app = FastAPI()

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.add_middleware(TokenValidationMiddleware)

app.include_router(book_router, prefix='/api')


@app.get("/")
def read_root():
    return {"Hello": "World"}
