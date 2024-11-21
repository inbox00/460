import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Quiz data
quiz_questions = [
    {
        "question": "According to the International Association of Conference Interpreters (AIIC), in which type of language do interpreters possess native-like proficiency?",
        "options": ["Working language", "A language", "Active language", "Passive"],
        "correct": "B"
    },
    {
        "question": "Which of the following is a significant difference between interpreter skills and translator skills?",
        "options": ["Working language level", "Cognitive skills", "Grammatical competence", "Theoretical concepts"],
        "correct": "C"
    },
    {
        "question": "Permutation is a useful exercise for which type of skill?",
        "options": ["Translation", "Oral presentation", "Written presentation", "Written preparation"],
        "correct": "B"
    },
    {
        "question": "The use of pauses and hesitations in oral speech are signs of which of the following?",
        "options": ["High working complexity", "High idiom usage", "Low linguistic knowledge", "Low availability"],
        "correct": "D"
    },
    {
        "question": "The inability to finish a sentence which has been started is a sign of which of the following?",
        "options": ["Low speech translation", "Low speech production availability", "Low cognitive skills", "Low memory processing capacity"],
        "correct": "B"
    },
    {
        "question": "Low availability in written text production as compared to speech production is a lesser problem because of which of the following reasons?",
        "options": ["There is less need for written text production", "Written text production involves revisions", "Speech production is a natural grammatical exercise", "Written text production is performed manually"],
        "correct": "B"
    },
    {
        "question": "The first processing area for language comprehension is which of the following?",
        "options": ["Short-term memory", "Working memory", "Sensory memory", "Dual memory"],
        "correct": "C"
    },
    {
        "question": "Which of the following language comprehension processes is automatic?",
        "options": ["Determining meaning", "Perception by senses", "Storage into memory", "Comparison to experience"],
        "correct": "B"
    },
    {
        "question": "The language constituents known as lexical units are described as which of the following?",
        "options": ["Language special purpose rules", "General compositional statements", "Words and idioms", "Mental vocabularies"],
        "correct": "C"
    },
    {
        "question": "The language constituent that governs the way words are assembled is called which of the following?",
        "options": ["Compositional rules", "Special purpose rules", "Lexical units", "Mental comprehension"],
        "correct": "A"
    },
    {
        "question": "The language constituent that deals with stylistics and preferences is called which of the following?",
        "options": ["Compositional rules", "Special purpose rules", "Lexical units", "Mental comprehension"],
        "correct": "B"
    },
    {
        "question": "In the Gravitation Model of language availability, LC stands for which of the following?",
        "options": ["Language comprehension", "Language constituents", "Linguistic clarity", "Labeling constructs"],
        "correct": "B"
    },
    {
        "question": "In the Gravitation Model of language availability, the various sectors represent which of the following?",
        "options": ["Comprehension", "Classifications", "Lexical mapping", "Level of availability"],
        "correct": "D"
    },
    {
        "question": "The sector which is furthest from the nucleus of the Gravitation Model is which form of availability?",
        "options": ["Spoken comprehension", "Reading comprehension", "Spoken production", "Written production"],
        "correct": "D"
    },
    {
        "question": "The sector which is closest to the nucleus of the Gravitation Model is which form of availability?",
        "options": ["Spoken comprehension", "Reading comprehension", "Spoken production", "Written production"],
        "correct": "C"
    },
    {
        "question": "The Centrifugal Principle of the Gravitation Model is described in which of the following statements?",
        "options": ["Lexical constituents that are stimulated by use move outward", "Lexical constituents that are stimulated by use move inward", "Lexical constituents lacking stimulation move outward", "Lexical constituents lacking stimulation move inward"],
        "correct": "C"
    },
    {
        "question": "The Centripetal Effect of Stimulation in the Gravitation Model is described in which of the following statements?",
        "options": ["Lexical constituents that are stimulated by use move outward", "Lexical constituents that are stimulated by use move inward", "Lexical constituents lacking stimulation move outward", "Lexical constituents lacking stimulation move inward"],
        "correct": "B"
    },
    {
        "question": "The effect of Frequency in the Gravitation Model is described in which of the following statements?",
        "options": ["Frequent stimulation increases the Centrifugal Principle", "Less frequent stimulation decreases the Centrifugal Principle", "Frequent stimulation increases the Centripetal Effect", "Less frequent stimulation increases the Centripetal Effect"],
        "correct": "C"
    },
    {
        "question": "The Escort Effect in the Gravitation Model is described in which of the following statements?",
        "options": ["Lexical constituents that are similar are affected by the Centripetal Effect", "Lexical constituents that differ are affected by the Centripetal Effect", "Lexical constituents that are similar are affected by centrifugal drift", "Lexical constituents that differ are included in Centripetal Effect"],
        "correct": "A"
    },
    {
        "question": "True or False? Oral and written availability have a strong correlation.",
        "options": ["True", "False"],
        "correct": "B"
    }
]



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message with a 'Begin Quiz' button."""
    keyboard = [
        [InlineKeyboardButton("Begin Quiz", callback_data="start_quiz")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the Quiz Bot! Type anything or click the button to begin the quiz.", reply_markup=reply_markup)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the first question."""
    context.user_data['score'] = 0  # Initialize score
    context.user_data['total_questions'] = len(quiz_questions)  # Total questions
    context.user_data['question_index'] = 0  # Start at the first question
    question_index = 0
    await ask_question(update, context, question_index)

async def ask_question(update, context, question_index):
    """Send a question with answer options."""
    question = quiz_questions[question_index]
    total_questions = context.user_data['total_questions']
    
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"answer|{question_index}|{opt}")]
        for opt in question["options"]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if hasattr(update, 'message'):
        await update.message.reply_text(f"Question {question_index + 1} of {total_questions}\n{question['question']}", reply_markup=reply_markup)
    elif hasattr(update, 'callback_query'):
        await update.callback_query.message.reply_text(f"Question {question_index + 1} of {total_questions}\n{question['question']}", reply_markup=reply_markup)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the answer selection."""
    query = update.callback_query
    await query.answer()
    
    _, question_index, selected_option = query.data.split('|')
    question_index = int(question_index)
    question = quiz_questions[question_index]
    correct_answer = question["correct"]
    correct_option = question["options"][ord(correct_answer) - ord('A')]
    
    # Display the full question with the selected answer and the correct answer
    if selected_option == correct_option:
        context.user_data['score'] += 1
        await query.edit_message_text(f"Question {question_index + 1} of {len(quiz_questions)}\n{question['question']}\n\nCorrect! ✅ The answer is: {correct_option}")
    else:
        await query.edit_message_text(f"Question {question_index + 1} of {len(quiz_questions)}\n{question['question']}\n\nWrong! ❌ The correct answer was: {correct_option}")
    
    # Move to the next question
    if question_index + 1 < len(quiz_questions):
        context.user_data['question_index'] = question_index + 1
        await ask_question(query, context, question_index + 1)
    else:
        score = context.user_data['score']
        total_questions = context.user_data['total_questions']
        
        if score == total_questions:
            await query.message.reply_text(
                f"Quiz completed! 🎉\nYour score: {score}/{total_questions}\nWell done! 🎉"
            )
        else:
            keyboard = [
                [InlineKeyboardButton("Try Again", callback_data="start_quiz")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                f"Quiz completed! 🎉\nYour score: {score}/{total_questions}\n"
                "Keep practicing to achieve full marks!",
                reply_markup=reply_markup
            )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'Begin Quiz' and 'Try Again' actions."""
    query = update.callback_query
    await query.answer()

    if query.data == "start_quiz":
        await quiz(query, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any message to start the quiz."""
    await quiz(update, context)

def main():
    """Run the bot."""
    application = ApplicationBuilder().token("7272579625:AAEOr6lToDy_4WRIuFbkbpd-lC60YMwcw3c").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Handle any text message
    application.add_handler(CallbackQueryHandler(handle_callback, pattern="^start_quiz$"))
    application.add_handler(CallbackQueryHandler(handle_answer, pattern="^answer\\|"))

    application.run_polling()
    
if __name__ == "__main__":
    main()
