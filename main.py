from aiogram import Bot, Dispatcher, types

TOKEN_API = "7059449160:AAHVxRTEd7HuCAjajZ6j9nGloxvvmdb_rFM"

bot = Bot(TOKEN_API)
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    await message.answer(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)
