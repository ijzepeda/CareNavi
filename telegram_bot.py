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

from to_pdf import save_pdf


import nlp_similarity
import nlp



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


def get_diagnotic_and_details(full_text):
    """get_diagnotic_and_details() Receives the text from the user. and it will process all information"""
    
    ###################
    # I need to process the text twice at least, first, to extract user details.
    # If possible delete that information.
    # Second run: get the symptoms
    ###################
    #Step1: ()SPlit main_text into User, and symptoms, or iterate.
    user_text , symptoms_text = nlp.split_text_content(full_text)

    # Step2: User_DETAILS
    txt_user_data = nlp.extract_user_details(user_text)

    #Step3: (Symptoms)Send symp_text to nlp_similarity and receive a dictionary
    txt_disease_details=nlp_similarity.find_similar_disease(symptoms_text,"symptoms")

    # combine txt_user_data and txt_disease_details in one dictionary
    diagnosis = {**txt_user_data, **txt_disease_details}

    return diagnosis


##############
### COMMANDS
##############

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user to send a voicenote."""
   
    await update.message.reply_text(
        f"Hello! This is a {BOTNAME}. \n Your Medical and Care Navigator.\n"
        f"I will understand your illness and provide a treatment\n"
        f"While you reach out for professional medical help.\n"
        f"Start with your Name, age, weight heigh.\n Followed up by all your symptoms."
        "Start sending a Voice Note, or a Text"
    )
    # return AUDIO

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """This function will recive the text from any other part and send it to process"""
    user = update.message.from_user
    full_text = update.message.text
    logger.info("Text of %s: %s", user.first_name, full_text)
    await update.message.reply_text(
        "Oh! I understand, let me think....."
    )

    # SECOND SCAN TO GET ALL SYMPTOMS. Everything happens in that function
    user_diagnostics = get_diagnotic_and_details(full_text)

    await update.message.reply_text(
        f"This is your diagnostic:\n"
        f"{user_diagnostics['disease']}"
    )

    print(user_diagnostics)
    pdf_path = save_pdf(user_diagnostics)
    if(pdf_path!=None):
        with open(pdf_path, 'rb') as pdf_file:
            await update.message.reply_document(pdf_file)

    await update.message.reply_text(
        f"That's gonna be $20,000!"
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
    
    x=  get_transcript(audio_path)
    await update.message.reply_text(
        "Transcript:\n"+x
    )   
    y=  get_diagnotic_and_details(x)
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
    y=  get_diagnotic_and_details(x)
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

# Create the error handler function
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error."""
    logging.error(msg="Exception occurred", exc_info=context.error)
    await update.message.reply_text(
        f"{BOTNAME} is sick as well. There was an error. Please try again.", reply_markup=ReplyKeyboardRemove()
    )


def main() -> None:
    """Start the amazing CareNavi bot."""
    application = Application.builder().token(TOKEN).build()
    print(f">>>>> {BOTNAME} IS ALIVE <<<<<<<<<<<<<<<<")

    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler("start", start)],
    #     states={
    #     AUDIO: [
    #     MessageHandler(filters.VOICE, voice),
    #     MessageHandler(filters.AUDIO, audio),
    #     MessageHandler(filters.TEXT, text)
    #                 ], 
    #     },
    #     fallbacks=[CommandHandler("cancel", cancel)],
    # )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start),
                      ],
        states={ 
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add the error handler
    application.add_error_handler(error_handler)
    application.add_handler(conv_handler)

    application.add_handler(MessageHandler(filters.VOICE, voice))
    application.add_handler(MessageHandler(filters.TEXT, text))
    application.add_handler(MessageHandler(filters.AUDIO, audio))

    
    application.add_handler(conv_handler)
    application.run_polling()




if __name__ == "__main__":
    main()

# based on the example at their website: