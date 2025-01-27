from telegram import Update
from telegram.ext import MessageHandler,filters,ApplicationBuilder, CommandHandler,ContextTypes
from typing import Final
import random

TOKEN = "7751885914:AAHf2U7VmUs8qsyjmgLISqhrtjZQx18oKOY"
BOT_USERNAME:Final = "@the_super_math_bot"

user_math_problems = {}

async def hello(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def error(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    print(f'An error occured: {context.error}')
    await update.message.reply_text(f'An error occured: {context.error}')


def generate_math_problem() -> (str, int):
    operators = ['+', '-', '*', '/']
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(operators)
    
    if operator == '/':
        num1 = num1 * num2
    
    problem = f"{num1} {operator} {num2}"
    answer = eval(problem)
    return problem, round(answer, 2)  

async def send_math_problem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_math_problems
    user_id = update.effective_user.id
    
    problem, answer = generate_math_problem()
    user_math_problems[user_id] = answer
    
    await update.message.reply_text(f"Solve this: {problem}")

def handle_response(text:str)->str:

    processed:str = text.lower()

    if 'hello' in processed:
        return 'Hello there'
    
    return 'I am sorry, I did not understand that'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_math_problems
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if user_id in user_math_problems:
        try:
            user_answer = float(text)
            correct_answer = user_math_problems.pop(user_id)
            
            if user_answer == correct_answer:
                await update.message.reply_text("🎉 Correct! Well done.")
            else:
                await update.message.reply_text(f"❌ Wrong. The correct answer was {correct_answer}.")
        except ValueError:
            await update.message.reply_text("Please send a valid number as your answer.")
    else:
        await update.message.reply_text("Type /math to get a new problem!")
    

if __name__ == "__main__":
    print("Starting...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("math", send_math_problem))
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    app.add_error_handler(error)
    print("Polling...")
    app.run_polling(poll_interval=3)
