from aiogram import Bot, Dispatcher, types
import joblib


TOKEN_API = "your_token"

bot = Bot(TOKEN_API)
dp = Dispatcher()

# Загрузка обученной модели и инициализация векторизатора
classifier = joblib.load('my_model.joblib')
vectorizer = joblib.load('vectorizer.joblib')


# Функция для классификации текста
def classify_text(text):
    text_tfidf = vectorizer.transform([text])
    label = classifier.predict(text_tfidf)[0]
    return label


# Обработчик текстовых сообщений
@dp.message()
async def handle_text(message: types.Message):
    text = message.text
    label = classify_text(text)
    reply_text = f"Тема сообщения: {label}"
    await message.reply(reply_text)



if __name__ == '__main__':
    dp.run_polling(bot)
