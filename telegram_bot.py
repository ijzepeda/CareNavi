#!/usr/bin/env python

# https://docs.python-telegram-bot.org/en/stable/examples.conversationbot.html


import logging
from telegram import __version__ as TG_VER
import whisper
import openai  # New version of whisper available on openai

import os
import toml
from telegram import ReplyKeyboardRemove, Update
TOKEN=toml.load('./secrets.toml')['TELEGRAM_API_KEY']




import nlp
# from nlp import process_text

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This bot is not compatible with your current PTB version {TG_VER}. Please use a different device Sorry!"
        
    )

# TELEGRAM INITIALIZATION
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

VOICE, AUDIO, TRANSLATE = range(3)
BOTNAME="CareNavi"
WHISPER_MODEL="small"
language="english"
user_data="user_data" #server folder



if not os.path.exists(os.path.join('./',(user_data))):
        print(f"Making a folder for {user_data}")
        os.makedirs(os.path.join('./',(user_data)))

try:
    model = whisper.load_model(WHISPER_MODEL, device='gpu')
    print("GPU Found,")
except:
    print("No GPU found, using CPU")
    model = whisper.load_model(WHISPER_MODEL, device='cpu')  


def get_transcript(audio_file):
    out = model.transcribe(audio_file)
    return out['text']  


def get_diagnotic(text):
    """get_diagnotic() Receives the text from the user. and it will process all information"""
    diagnosis = nlp.process_text(text)
    return diagnosis

##############
### COMMANDS
##############

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user to send a voicenote."""
   
    await update.message.reply_text(
        f"Hello! This is a {BOTNAME}. \n Your Medical and Care Navigator.\n"
        f"I will understand your illness and provide a treatment\n",
        f"While you reach out for professional medical help.\n",
        f"Start with your Name, age, weight heigh. Then Give me all your symptoms.",
        "Start sending a Voice Note, or a Text",
    )
    # return AUDIO

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """This function will recive the text from any other part and send it to process"""
    user = update.message.from_user
    text = update.message.text
    logger.info("Text of %s: %s", user.first_name, text)
    await update.message.reply_text(
        "Oh! I understand, let me think....."
    )

    diagnostics = get_diagnotic(text)

    await update.message.reply_text(
        f"This is your diagnostics:\n",
        f"{diagnostics}",
    )

async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """VOICE is a voicenote, using the microphone directly."""
    await update.message.reply_text(
        "I am listening to it, give me a second...."
    )
    user = update.message.from_user
    #1
    # audio_file = update.message.voice.file_id
    # new_file = context.bot.get_file(update.message.voice.file_id)
    # new_file.download(f"./{user_data}/voice_note.ogg")
    #2
    audio_file = await update.message.voice.get_file()
    audio_path=f"./{user_data}/user_voice.ogg"
    
    if not os.path.exists(os.path.join('./',(user_data))):
        print(f"Making a folder for {user_data}")
        os.makedirs(os.path.join('./',(user_data)))

    await audio_file.download_to_drive(audio_path)
    logger.info("Audio of %s: %s", user.first_name, "user_voice.ogg")
    await update.message.reply_text(
        "Working on it..."
    )
    x=  get_transcript(audio_path)
    await update.message.reply_text(
        "Transcript:\n"+x
    )   
    y=  get_diagnotic(x)
    await update.message.reply_text(
        "Your Diagnostic:\n"+y
    )  

async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """AUDIO will receive an audio file from the device."""
    await update.message.reply_text(
        "I am listening to it, give me a second...."
    )
    user = update.message.from_user
    audio_file = await update.message.audio.get_file()
    audio_path=f"./{user_data}/user_audio.ogg"
    
    if not os.path.exists(os.path.join('./',(user_data))):
        print(f"Making a folder for {user_data}")
        os.makedirs(os.path.join('./',(user_data)))

    await audio_file.download_to_drive(audio_path)
    logger.info("Audio of %s: %s", user.first_name, "user_audio.ogg")
    await update.message.reply_text(
        "Working on it..."
    )
    x=  get_transcript(audio_path)
    await update.message.reply_text(
        "Transcript:\n"+x
    )   
    y=  get_diagnotic(x)
    await update.message.reply_text(
        "Summary:\n"+y
    )  


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        f"{BOTNAME} wishes you well, please visit your doctor regularly.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Start the amazing CareNavi bot."""
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
        AUDIO: [
        MessageHandler(filters.VOICE, voice),
        MessageHandler(filters.AUDIO, audio),
        MessageHandler(filters.TEXT, text)
                    ], 

        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()

# based on the example at their website: