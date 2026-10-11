import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command

# Проверьте, чтобы этот токен в точности совпадал с BotFather!
TOKEN = "8659582793:AAFuqmD6Ihf6igZuBClfg-X7-0bq8fqsEuM"
WEBAPP_URL = "https://vercel.app"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🌟 Войти в StarMarket Premium", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    
    await message.answer(
        f"👑 **Добро пожаловать в StarMarket Premium!**\n\n"
        f"Вы успешно авторизовались в главном маркетплейсе цифровых ценностей Telegram.\n\n"
        f"Нажмите на золотую кнопку ниже, чтобы открыть витрину товаров, управлять вашим NFT-профилем или выставить лот на продажу:",
        reply_markup=keyboard
    )

async def main():
    # Перед запуском принудительно очищаем старые зависшие запросы в Telegram
    await bot.delete_webhook(drop_pending_updates=True)
    print("🚀 Робот StarMarket успешно запущен и очистил очередь запросов...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

