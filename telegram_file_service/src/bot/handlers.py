import os
import re
from typing import Optional, Tuple

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .config import settings
from .api_client import send_audio_for_summarise

router = Router()

MAX_AUDIO_MB = 50

ALLOWED_MIME = {
    "audio/mpeg",
    "audio/mp3",
    "audio/wav",
    "audio/x-wav",
    "audio/mp4",
    "audio/x-m4a",
    "audio/aac",
    "audio/ogg",
    "audio/opus",
}

ALLOWED_EXT = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".opus"}


class UploadAudioState(StatesGroup):
    waiting_audio = State()


def safe_name(name: str) -> str:
    name = (name or "").strip()
    name = re.sub(r"[^\w.\-() ]+", "_", name, flags=re.UNICODE)
    return name[:120] if name else "file"


def render_bar(pct: int) -> str:
    pct = max(0, min(100, pct))
    blocks = 10
    filled = round(blocks * pct / 100)
    return "▰" * filled + "▱" * (blocks - filled) + f" {pct}%"


async def set_progress(msg: Message, pct: int, stage: str) -> None:
    await msg.edit_text(f"{stage}\n{render_bar(pct)}")


def validate_audio(
    file_name: Optional[str],
    mime: Optional[str],
    size_bytes: Optional[int],
) -> Tuple[bool, str]:
    if size_bytes is not None and size_bytes > MAX_AUDIO_MB * 1024 * 1024:
        return False, f"Файл слишком большой. Макс: {MAX_AUDIO_MB}MB."

    ext = os.path.splitext((file_name or "").lower())[1]

    if mime:
        if mime not in ALLOWED_MIME:
            if ext not in ALLOWED_EXT:
                return False, f"Неподдерживаемый формат: {mime} ({ext or 'no ext'})."
    else:
        if ext and ext not in ALLOWED_EXT:
            return False, f"Неподдерживаемое расширение: {ext}. Разрешено: {', '.join(sorted(ALLOWED_EXT))}"

    if ext and ext not in ALLOWED_EXT and (mime not in {"audio/ogg", "audio/opus"}):
        return False, f"Неподдерживаемое расширение: {ext}. Разрешено: {', '.join(sorted(ALLOWED_EXT))}"

    return True, "OK"


def build_metadata(message: Message, kind: str, file_name: Optional[str], mime: Optional[str]):
    return {
        "kind": kind,
        "file_name": file_name,
        "mime_type": mime,
        "message_id": message.message_id,
        "from_user_id": message.from_user.id if message.from_user else None,
        "chat_id": message.chat.id,
    }


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("welcomed"):
        await state.update_data(welcomed=True)
        await message.answer(
            "Привет! Я помогу сделать суммаризацию аудио.\n\n"
            "Команды:\n"
            "/upload_audio — отправь аудио для суммаризации\n"
            "/cancel — отмена ожидания\n"
            "/myid — показать chat_id\n"
            "/test_summary — тестовое сообщение"
        )
    else:
        await message.answer("Снова привет 🙂 Нажми /upload_audio, чтобы отправить аудио.")


@router.message(Command("myid"))
async def myid(message: Message):
    await message.answer(f"chat_id: <code>{message.chat.id}</code>")


@router.message(Command("test_summary"))
async def test_summary(message: Message):
    await message.answer(
        "📝 Суммаризация готова (тест без Kafka)\n\n"
        "• Пункт 1\n• Пункт 2\n• Пункт 3"
    )


@router.message(Command("upload_audio"))
async def cmd_upload_audio(message: Message, state: FSMContext):
    await state.set_state(UploadAudioState.waiting_audio)
    await message.answer(
        "Ок, пришли аудио:\n"
        "• как <b>audio</b> (mp3/m4a/wav)\n"
        "• или <b>voice</b>\n"
        "• или <b>document</b> (если mp3 отправляешь файлом)"
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Отменено.")


@router.message(UploadAudioState.waiting_audio, F.audio)
async def got_audio(message: Message, state: FSMContext):
    await state.clear()
    chat_id = str(message.chat.id)
    aud = message.audio

    ok, reason = validate_audio(aud.file_name, aud.mime_type, aud.file_size)
    if not ok:
        await message.answer(f"❌ {reason}\n\nОтправь mp3/wav/m4a/ogg или voice.")
        return

    status = await message.answer("⏳ Готовлю загрузку…")
    await set_progress(status, 10, "Подготовка")

    await set_progress(status, 30, "Скачиваю файл из Telegram")
    file = await message.bot.get_file(aud.file_id)
    data = await message.bot.download_file(file.file_path)
    file_bytes = data.read()

    await set_progress(status, 70, "Отправляю в API")
    meta = build_metadata(message, "audio", aud.file_name, aud.mime_type)

    try:
        resp = await send_audio_for_summarise(
            settings.API_BASE_URL,
            interaction_data=chat_id,
            source_type=settings.SOURCE_TYPE,
            metadata=meta,
            file_bytes=file_bytes,
            file_name=safe_name(aud.file_name or "audio.mp3"),
            mime_type=aud.mime_type or "audio/mpeg",
        )

        await set_progress(status, 100, "Готово")
        job_id = resp.get("job_id")

        await message.answer(f"✅ В очередь! job_id: <code>{job_id}</code>" if job_id else "✅ В очередь!")
    except Exception as e:
        await message.answer(f"❌ Ошибка отправки в API: {e}")


@router.message(UploadAudioState.waiting_audio, F.voice)
async def got_voice(message: Message, state: FSMContext):
    await state.clear()
    chat_id = str(message.chat.id)

    status = await message.answer("⏳ Принял voice. Начинаю…")
    await set_progress(status, 20, "Скачиваю voice из Telegram")

    file = await message.bot.get_file(message.voice.file_id)
    data = await message.bot.download_file(file.file_path)
    file_bytes = data.read()

    await set_progress(status, 70, "Отправляю в API")
    meta = build_metadata(message, "voice", "voice.ogg", "audio/ogg")

    try:
        resp = await send_audio_for_summarise(
            settings.API_BASE_URL,
            interaction_data=chat_id,
            source_type=settings.SOURCE_TYPE,
            metadata=meta,
            file_bytes=file_bytes,
            file_name="voice.ogg",
            mime_type="audio/ogg",
        )

        await set_progress(status, 100, "Готово")
        job_id = resp.get("job_id")

        await message.answer("✅ В очередь!" + (f"\njob_id: <code>{job_id}</code>" if job_id else ""))
    except Exception as e:
        await message.answer(f"❌ Ошибка отправки в API: {e}")


@router.message(UploadAudioState.waiting_audio, F.document)
async def got_document(message: Message, state: FSMContext):
    await state.clear()
    chat_id = str(message.chat.id)
    doc = message.document

    ok, reason = validate_audio(doc.file_name, doc.mime_type, doc.file_size)
    if not ok:
        await message.answer(f"❌ {reason}\n\nОтправь mp3/wav/m4a/ogg или voice.")
        return

    status = await message.answer("⏳ Принял документ. Начинаю…")
    await set_progress(status, 25, "Скачиваю файл из Telegram")

    file = await message.bot.get_file(doc.file_id)
    data = await message.bot.download_file(file.file_path)
    file_bytes = data.read()

    await set_progress(status, 70, "Отправляю в API")
    meta = build_metadata(message, "document", doc.file_name, doc.mime_type)

    try:
        resp = await send_audio_for_summarise(
            settings.API_BASE_URL,
            interaction_data=chat_id,
            source_type=settings.SOURCE_TYPE,
            metadata=meta,
            file_bytes=file_bytes,
            file_name=safe_name(doc.file_name or "audio.bin"),
            mime_type=doc.mime_type or "application/octet-stream",
        )

        await set_progress(status, 100, "Готово")
        job_id = resp.get("job_id")

        await message.answer(f"✅ В очередь! job_id: <code>{job_id}</code>" if job_id else "✅ В очередь!")
    except Exception as e:
        await message.answer(f"❌ Ошибка отправки в API: {e}")


@router.message(UploadAudioState.waiting_audio)
async def wrong_payload(message: Message, state: FSMContext):
    await message.answer("❌ Я жду аудио (audio/voice/document). Нажми /cancel чтобы отменить.")
