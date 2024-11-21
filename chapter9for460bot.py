from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Quiz data
quiz_questions = [
    {
        "question": "According to AIIC, in which type of language do interpreters possess native-like proficiency?",
        "options": ["Working language", "A language", "Active language", "Passive"],
        "correct": "B"
    },
    {
        "question": "Which of the following is a significant difference between interpreter and translator skills?",
        "options": ["Working language level", "Cognitive skills", "Grammatical competence", "Theoretical concepts"],
        "correct": "C"
    },
    # Add more questions here...
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message and start the quiz."""
    await update.message.reply_text("Welcome to the Quiz Bot! Type /quiz to begin.")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the first question."""
    question_index = 0
    await ask_question(update, context, question_index)

async def ask_question(update, context, question_index):
    """Send a question with answer options."""
    question = quiz_questions[question_index]
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"{question_index}|{opt}")]
        for opt in question["options"]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(question["question"], reply_markup=reply_markup)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the answer selection."""
    query = update.callback_query
    await query.answer()
    
    question_index, selected_option = map(str, query.data.split('|'))
    question_index = int(question_index)
    correct_answer = quiz_questions[question_index]["correct"]
    correct_option = quiz_questions[question_index]["options"][ord(correct_answer) - ord('A')]
    
    if selected_option == correct_option:
        await query.edit_message_text(f"Correct! ✅ The answer is: {correct_option}")
    else:
        await query.edit_message_text(f"Wrong! ❌ The correct answer was: {correct_option}")
    
    # Move to the next question
    if question_index + 1 < len(quiz_questions):
        await ask_question(query, context, question_index + 1)
    else:
        await query.message.reply_text("Quiz completed! 🎉")

def main():
    """Run the bot."""
    application = ApplicationBuilder().token("7272579625:AAEOr6lToDy_4WRIuFbkbpd-lC60YMwcw3c").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CallbackQueryHandler(handle_answer))
    
    application.run_polling()
    
if __name__ == "__main__":
    main()
