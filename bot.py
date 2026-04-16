import os
os.system("apt update && apt install -y ghostscript")

import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

API_TOKEN = "ВСТАВЬ_СЮДА_ТОКЕН"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# старт
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.reply("Отправь PDF — я его сожму 📉")


# обработка файлов
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_docs(message: Message):
    file = message.document

    # проверка формата
    if not file.file_name.endswith(".pdf"):
        await message.reply("Пока только PDF 😅")
        return

    # ограничение размера (10MB)
    if file.file_size > 10 * 1024 * 1024:
        await message.reply("Файл слишком большой 😬 (макс 10MB)")
        return

    file_path = f"input_{file.file_name}"
    output_path = f"compressed_{file.file_name}"

    # скачиваем файл
    await file.download(destination_file=file_path)

    await message.reply("Сжимаю... ⏳")

    try:
        # команда сжатия
        command = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/ebook",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_path}",
            file_path,
        ]

        subprocess.run(command)

        # отправляем обратно
        with open(output_path, "rb") as f:
            await message.reply_document(f)

    except Exception as e:
        await message.reply("Ошибка при обработке 😢")

    finally:
        # очистка
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_path):
            os.remove(output_path)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
