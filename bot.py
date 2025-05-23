import os, asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import *
from ffmpeg_split import split_video_by_size
from queue_manager import global_queue

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim video (maks 2GB) untuk dipotong jadi bagian 99MB.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.video.get_file()
    size_mb = file.file_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return await update.message.reply_text("Ukuran file melebihi 2GB.")

    user_id = update.message.from_user.id
    input_path = os.path.join(UPLOAD_FOLDER, f"{user_id}_input.mp4")
    output_dir = os.path.join(OUTPUT_FOLDER, str(user_id))
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    await update.message.reply_text("Mengunduh video...")
    await file.download_to_drive(input_path)

    async def job():
        try:
            await update.message.reply_text("Memproses video...")
            files = split_video_by_size(input_path, output_dir, SPLIT_SIZE_MB)
            for f in files:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=open(f, 'rb'))
        except Exception as e:
            await update.message.reply_text(f"Gagal: {e}")
        finally:
            os.remove(input_path)
            for f in os.listdir(output_dir):
                os.remove(os.path.join(output_dir, f))
            os.rmdir(output_dir)

    try:
        await global_queue.add(job)
        await update.message.reply_text("Video masuk antrean.")
    except Exception as e:
        await update.message.reply_text(str(e))

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Video.ALL, handle_video))
    asyncio.create_task(global_queue.process())
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
