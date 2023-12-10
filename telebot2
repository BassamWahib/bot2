import os
from telegram import Update
from rembg import remove
from PIL import Image

import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

TOKEN = "6705629015:AAEGa-InW-23Vl-WsidDmU_qT1uZTRlwWo4"

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hi, I am an image manipulation program. To start click /start')

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hi, {update.message.chat.first_name}, To remove image background, please send your image')

async def process_image(photo_name: str):
    name, _ = os.path.splitext(photo_name)
    output_photo_path = f'./processed/{name}.png'
    input_image_path = f'./temp/{photo_name}'
    output_image_path = f'./temp/{name}.png'

    input_image = Image.open(input_image_path)
    output_image = remove(input_image)
    output_image.save(output_image_path)

    return output_image_path

@app.get("/help")
async def help_route(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await help_handler(update, context)

@app.get("/start")
async def start_route(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_handler(update, context)

@app.post("/process_image")
async def process_image_route(file: UploadFile):
    unique_file_id = file.filename
    photo_name = f'{unique_file_id}.png'

    input_image_path = f'./temp/{photo_name}'
    await file.save(input_image_path)

    await context.bot.send_message(chat_id=update.effective_chat.id, text='Processing your image')
    processed_image = await process_image(photo_name)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=processed_image)

    os.remove(input_image_path)
    os.remove(processed_image)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Run the application
    application.run_polling()
