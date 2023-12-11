import os
from telegram import Update
from rembg import remove
from PIL import Image

import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse

nest_asyncio.apply()

app = FastAPI()
TOKEN = "6705629015:AAEGa-InW-23Vl-WsidDmU_qT1uZTRlwWo4"

# Adjust file paths for Render
temp_folder = '/mnt/data/temp'
processed_folder = '/mnt/data/processed'

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hi, I am an image manipulation program. To start click /start')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hi, {update.message.chat.first_name}, To remove image background, please send your image')

async def process_image(photo_name: str):
    name, _ = os.path.splitext(photo_name)
    output_photo_path = os.path.join(processed_folder, f'{name}.png')
    input_path = os.path.join(temp_folder, photo_name)

    input_image = Image.open(input_path)
    output_image = remove(input_image)
    output_image.save(output_photo_path)

    return output_photo_path

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... (other code remains the same)

    file_path = os.path.join(temp_folder, photo_name)
    await photo_file.download_to_drive(custom_path=file_path)

    if os.path.exists(file_path):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Processing your image')
        processed_image = await process_image(photo_name)
        await context.bot.send_document(chat_id=update.effective_chat.id, document=processed_image)
        os.remove(processed_image)
        os.remove(file_path)  # Optionally remove the downloaded file after processing
    else:
        print(f"File not found after download: {file_path}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Command handler
    help_handler = CommandHandler('help', help)
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_message)

    # Register command
    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(message_handler)

    # Run the application
    application.run_polling()
