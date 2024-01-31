from telegram.constants import ParseMode
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ApplicationBuilder
)
import requests
import os
import logging
from fastapi import FastAPI

app = FastAPI()

# Handle the route for /getUpdates
@app.post("/getUpdates")
def get_updates():
    # Your code to handle /getUpdates goes here
    pass

# Handle the default route
@app.get("/")
def default_route():
    return {"message": "Hello, this is your default route!"}

# TikTok Downloader API
API = 'https://api.single-developers.software/tiktok?url='

# Your BOT Token
BOT_TOKEN = "6654248660:AAEM9hTXwzeTuKMTE_HDQAt_ZSQAxLQg5N4"

# TikTok Video URL Types, You Can Add More to This :)
TikTok_Link_Types = ['https://m.tiktok.com', 'https://vt.tiktok.com', 'https://tiktok.com', 'https://www.tiktok.com']

# ParseMode Type For All Messages
_ParseMode = ParseMode.MARKDOWN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Download Task
async def Download_Video(Link, update, context):
    message = update.message
    req = None
    no_watermark = None
    watermark = None

    status_msg = await message.reply_text('🚀 Proses bntar')
    status_sticker = await message.reply_sticker('CAACAgUAAxkBAAED9jhiDqYeGjENlCjftByz0au6n4YAASEAAnUEAALpa8lXL9cvxeTK-2AjBA')

    # Getting Download Links Using API
    try:
        req = requests.get(API + Link).json()
        no_watermark = req['no_watermark']
        watermark = req['watermark']
        print('Download Links Generated \n\n\n' + str(req) + '\n\n\n')
    except Exception as e:
        print(f'Download Links Generate Error: {e}')
        await status_msg.edit_text(f'test munculin error di bot aja: \n\n{e}\n\n')
        await status_sticker.delete()
        return

    caption_text = """◇───────────────◇

    ✅ Successfully Downloaded {} Video 🔰

    🔰 Powerd by : [🏖 TikTok Download API 🏖](https://github.com/Single-Developers/API/blob/main/tiktok/Note.md)
    [🔥 Single Developers </> ](https://t.me/SingleDevelopers) Corporation ©️

    ◇───────────────◇"""

    # Uploading Downloaded Videos to Telegram
    print('Uploading Videos')
    await status_msg.edit_text('☘️ 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 𝚝𝚘 𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖....')
    try:
        await message.reply_video(video=no_watermark, supports_streaming=True, caption=caption_text.format('No Watermark'),
                                  parse_mode=_ParseMode)
        await message.reply_video(video=watermark, supports_streaming=True, caption=caption_text.format('Watermark'),
                                  parse_mode=_ParseMode)
    except Exception as e:
        print(f'Error uploading videos: {e}')
        await status_msg.edit_text(f'Error uploading videos: {e}')

    # Task Done! So, Deleting Status Messages
    await status_msg.delete()
    await status_sticker.delete()

# Message Incoming Action
async def incoming_message_action(update, context):
    message = update.message
    if any(word in str(message.text) for word in TikTok_Link_Types):
        await Download_Video(str(message.text), update, context)

async def start_handler(update, context):
    await update.message.reply_sticker('CAACAgUAAxkBAAED9kRiDq_GkOHuRHPeVv4IRhsvy4NtbwACqQQAAncUyFftN80YUiyXnyME')

# About Handler
async def tesdulu_handler(update, context):
    # await update.message.reply_sticker('CAACAgUAAxkBAAED9kZiDq_LFrib38c7DYu3jNz3ebsolgACJAUAAuTb4FdKtjtZGQ2ukiME')
    await update.message.reply_text('aman',
                              parse_mode=_ParseMode)

def error_handler(update, context):
    logging.error(f'Update {update} caused error {context.error}')

def main() -> None:
    """Run the bot."""

    # Commands Listning
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("tes", tesdulu_handler))

    # Message Incoming Action
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, incoming_message_action))

    # Error Handler
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
