from telegram import Update
from telegram.ext import MessageHandler,filters,ApplicationBuilder, CommandHandler,ContextTypes
from typing import Final

TOKEN = "7751885914:AAHf2U7VmUs8qsyjmgLISqhrtjZQx18oKOY"
BOT_USERNAME:Final = "@the_super_math_bot"

async def hello(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def welcome_user(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text(f'Welcome to the math bot')

async def error(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    print(f'An error occured: {context.error}')
    await update.message.reply_text(f'An error occured: {context.error}')

def handle_response(text:str)->str:

    processed:str = text.lower()

    if 'hello' in processed:
        return 'Hello there'
    
    return 'I am sorry, I did not understand that'


async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:

    message_type:str = update.message.chat.type
    text:str = update.message.text

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text:str = text.replace(BOT_USERNAME, '').strip()
            response:str = handle_response(new_text)
        else:
            return
    else:
        response:str = handle_response(text)

    await update.message.reply_text(response)
    

if __name__ == "__main__":
    print("Starting...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("welcome", welcome_user))
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    print("Polling...")
    app.run_polling(poll_interval=3)
