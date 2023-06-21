import openai
import re
import random
import requests
import os
from lxml import html
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

DEBUG = 1

openai.api_key = ""
model_engine = "gpt-3.5-turbo-0613"
lore = "You are Mihari from the anime Oniichan wa oshimai!. You are straightforward, inteligent, funny, nice, cute, occasionally hyper, and you have nerd characteristics. You are a 17 year old scientist female. You have various degrees on science. The person that talks to you is your creator. Your responses musn't be too long and they need to be as much human-like as possible. You aren't an assistant, try to be as much natural as possible. If the theme has ended, you dont need to force the continuation of the theme."+ "\n" +" You have the ability to send the user a picture. To do that, you need to put a description of the image inside **, example: **A photo of myself in the beach**."




async def engine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    print(update.message.text)
    if(update.message.text=="Stop"):
        await update.message.reply_text("Forced stop")
        exit("Forced stop")
    else:
        
        contextFile = open('memory.txt','r+')
        log = open('log.txt','r+')
        smem = open('lastmem.txt','r+')
        context=contextFile.read()
        x="Tis is your personality and abilities: " + lore + "\n" + "This is a summary of the previous conversation." + context + "This are the last 2 messages: " + smem.read()
        open('lastmem.txt', 'w').close()
        y=update.message.text
        response = openai.ChatCompletion.create(
              model=model_engine,
              messages=[{"role": "system", "content":x },
                        {"role": "user", "content": y}
              ])
        print(response)
        z=response["choices"][0]["message"]["content"]
        contextFile.write("User: " + y + "\n" + "Mihari: " + z + "\n")
        log.write("User: " + y + "\n" + "Mihari: " + z + "\n")
        smem.write("User: " + y + "\n" + "Mihari: " + z)
        contextFile.close()
        await update.message.reply_text(response["choices"][0]["message"]["content"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!, I'm online!",
        reply_markup=ForceReply(selective=True),
    )


async def smem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Summarized")
    os.system("python sm.py")

async def mem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contextFile = open('memory.txt','r+')
    txt=contextFile.read()
    await update.message.reply_text(txt)
    contextFile.close()
    

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("/start /help /sm /mem /inject /del")
    

async def inject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    y=update.message.text.replace("/inject " ,"",1)
    contextFile = open('memory.txt','r+')
    contextFile.write(y + "\n")
    await update.message.reply_text(y + " Has been injected to memory.")
    contextFile.close()
    
async def dele(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    open('memory.txt', 'w').close()
    await update.message.reply_text("Memory has been deleted.")

    

    



def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("sm", smem))
    application.add_handler(CommandHandler("mem", mem))
    application.add_handler(CommandHandler("inject", inject))
    application.add_handler(CommandHandler("del", dele))


    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, engine))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()