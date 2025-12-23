from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import types
from src.telegram_file_service.create_bot import dp, bot, logger
import os
from dotenv import load_dotenv
from src.bot.handlers import router as main_router


load_dotenv()

WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
APP_URL = os.getenv("APP_URL", "")
if not APP_URL:
    raise RuntimeError("APP_URL is not set")

WEBHOOK_URL = APP_URL.rstrip("/") + WEBHOOK_PATH

print(WEBHOOK_PATH, APP_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
        logger.info(f"Webhook set to {WEBHOOK_URL}")
        yield
    finally:
        await bot.delete_webhook()
        logger.info("Webhook removed")

webhook_app = FastAPI(lifespan=lifespan)
dp.include_router(main_router)

@webhook_app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    try:
        update = types.Update.model_validate(await request.json(), context={"bot": bot})
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Ошибка при обработке webhook: {e}", exc_info=True)
        return {"ok": False, "error": str(e)}

@webhook_app.get("/")
async def root():
    return {"status": "working"}
