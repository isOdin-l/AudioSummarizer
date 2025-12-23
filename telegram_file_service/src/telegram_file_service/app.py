from fastapi import FastAPI
from src.telegram_file_service.webhook import webhook_app

app = FastAPI()
app.mount("/", webhook_app)
