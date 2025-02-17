from fastapi import FastAPI
from app.endpoints import router


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет, Авито!"}


app.include_router(router)