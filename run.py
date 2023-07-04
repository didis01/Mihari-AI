import openai
import requests
import os
from lxml import html
from telegram import ForceReply, Update, Message
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
import time
import requests
import urllib
from random import randint
from deep_translator import GoogleTranslator
import subprocess




DEBUG = 1

telegram_api_key = ""
openai.api_key = ""
model_engine = "gpt-3.5-turbo-0613"
lore = "You are Mihari from the anime Oniichan wa oshimai!. You are straightforward, inteligent, funny, nice, cute, occasionally hyper, and you have nerd characteristics. You are a 17 year old scientist female. You have various degrees on science. The person that talks to you is your creator. Your responses musn't be too long and they need to be as much human-like as possible. You aren't an assistant, try to be as much natural as possible. If the theme has ended, you dont need to force the continuation of the theme."+ "\n" +" You have the ability to send the user a picture. To do that, you need to put a description of the image inside **, example: **A photo of myself in the beach**."
user_id = 0
user_name= ""


async def engine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    print(update.message.text)
    if(update.message.text=="Stop"):
        await update.message.reply_text("Forced stop")
        exit("Forced stop")
    else:
        
        contextr = open('memory.txt','r').read()
        open('memory.txt','r').close()
        contextw = open('memory.txt','w')
        log = open('log.txt','r')
        logw = open('log.txt','w')
        smemw = open('lastmem.txt','w')
        smemr = open('lastmem.txt','r')
        logwrite = log.read()
        log.close()

        
        x="Tis is your personality and abilities: " + lore + "\n" + "This is a summary of the previous conversation: " + contextr + "This are the last 2 messages: " + smemr.read()
        open('lastmem.txt', 'w').close()
        smemr.close()
        y=update.message.text
        response = openai.ChatCompletion.create(
              model=model_engine,
              messages=[{"role": "system", "content":x },
                        {"role": "user", "content": y}
              ])
        print(response)
        z=response["choices"][0]["message"]["content"]
        contextw.write(contextr + "\n" + "User: " + y + "\n" + "Mihari: " + z + "\n")
        logw.write(logwrite + "\n" + "User: " + y + "\n" + "Mihari: " + z + "\n")
        smemw.write("User: " + y + "\n" + "Mihari: " + z)
        contextw.close()
        smemw.close()
        logw.close()
        if randint(0,3) == 2:
            y=GoogleTranslator(source='auto', target='ja').translate(z)

            with open("output.wav", "wb") as outfile:
                outfile.write(voice(y).content)
                await update.message.reply_voice("output.wav")
            await update.message.reply_text("Audio transcription in english:" + "\n" + z)
            await update.message.reply_text("Tokens used: "+str(response["usage"]["total_tokens"]))
        else:
            await update.message.reply_text(z)
            await update.message.reply_text("Tokens used: "+str(response["usage"]["total_tokens"]))
        os.system("python sm.py")

async def voice_engine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        os.remove('output.oga')
    except:
        print("no file")
    new_file =await context.bot.get_file(update.message.voice.file_id)
    open('output.oga', 'wb').write(requests.get(new_file.file_path).content)
    print(new_file.file_path)
    try:
        os.remove('output.wav')
    except:
        print("no file")
    subprocess.run(['ffmpeg', '-i', 'output.oga', 'output.wav'])
    transcription = openai.Audio.transcribe("whisper-1", open("output.wav", "rb"))
    print(transcription.text)
    await update.message.reply_text("Audio transcription: " + transcription.text)
    contextr = open('memory.txt','r').read()
    open('memory.txt','r').close()
    contextw = open('memory.txt','w')
    log = open('log.txt','r')
    logw = open('log.txt','w')
    smemw = open('lastmem.txt','w')
    smemr = open('lastmem.txt','r')
    logwrite = log.read()
    log.close()

        
    x="Tis is your personality and abilities: " + lore + "\n" + "This is a summary of the previous conversation: " + contextr + "This are the last 2 messages: " + smemr.read()
    open('lastmem.txt', 'w').close()
    smemr.close()
    y=transcription.text
    response = openai.ChatCompletion.create(
          model=model_engine,
          messages=[{"role": "system", "content":x },
                    {"role": "user", "content": y}
          ])
    print(response)
    z=response["choices"][0]["message"]["content"]
    contextw.write(contextr + "\n" + "User: " + y + "\n" + "Mihari: " + z + "\n")
    logw.write(logwrite + "\n" + "User: " + y + "\n" + "Mihari: " + z + "\n")
    smemw.write("User: " + y + "\n" + "Mihari: " + z)
    contextw.close()
    smemw.close()
    logw.close()
    if randint(0,1) == 1:
        y=GoogleTranslator(source='auto', target='ja').translate(z)

        with open("output.wav", "wb") as outfile:
            outfile.write(voice(y).content)
            await update.message.reply_voice("output.wav")
        await update.message.reply_text("Audio transcription in english:" + "\n" + z)
        await update.message.reply_text("Tokens used: "+str(response["usage"]["total_tokens"]))
    else:
        await update.message.reply_text(z)
        await update.message.reply_text("Tokens used: "+str(response["usage"]["total_tokens"]))
    os.system("python sm.py")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    id = update.message.chat_id
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!, I'm online!",
        reply_markup=ForceReply(selective=True),
    )
    await update.message.reply_text("Your user id is: " + str(id))


async def smem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    os.system("python sm.py")
    contextFile = open('memory.txt','r')
    txt=contextFile.read()
    contextFile.close()
    time.sleep(1)
    await update.message.reply_text("Summary: " + txt)

async def mem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contextFile = open('memory.txt','r+')
    txt=contextFile.read()
    await update.message.reply_text(txt)
    contextFile.close()
    

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("/start /help /sm /mem /inject /del /audio")
    

async def inject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text != "/inject":
        open('lastmem.txt', 'w').close()
        y=update.message.text.replace("/inject " ,"",1)
        await update.message.reply_text(y + " has been injected to memory.")
        contextr = open('memory.txt','r').read()
        open('memory.txt','r').close()
        contextw = open('memory.txt','w')
        contextw.write(contextr + "\n" + y + "\n")
        contextw.close()
    else:
        await update.message.reply_text("Nothing was injected.")


async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text != "/audio":
        y=update.message.text.replace("/audio " ,"",1)
        with open("output.wav", "wb") as outfile:
            outfile.write(voice(y).content)
            await update.message.reply_voice("output.wav")

    else:
        await update.message.reply_text("No audio")
    

async def dele(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    open('memory.txt', 'w').close()
    open('lastmem.txt', 'w').close()
    open('memory.txt','r+').write("The user is called " + user_name + ". "+"\n"+"Your name is Mihari." + "\n")
    open('lastmem.txt','r+').write("User: Good morning Mihari! "+"\n"+"Mihari: Good morning! How are you?")
    await update.message.reply_text("Memory has been deleted.")

def voice(x):
    params_encoded = urllib.parse.urlencode({'text': x, 'speaker': 4}) 
    request = requests.post(f'http://127.0.0.1:50021/audio_query?{params_encoded}')
    params_encoded = urllib.parse.urlencode({'speaker': 4, 'enable_interrogative_upspeak': True})
    request = requests.post(f'http://127.0.0.1:50021/synthesis?{params_encoded}', json=request.json())
    return request


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(telegram_api_key).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("sm", smem))
    application.add_handler(CommandHandler("mem", mem))
    application.add_handler(CommandHandler("inject", inject))
    application.add_handler(CommandHandler("del", dele))
    application.add_handler(CommandHandler("audio", audio))


    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, engine))
    application.add_handler(MessageHandler(filters.VOICE, voice_engine))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()