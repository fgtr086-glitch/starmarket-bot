import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiohttp import web

# Проверьте токен вашего оранжевого бота!
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

# Создаем микро-веб-сервер для бесплатного тарифа Render
async def handle_index(request):
    return web.Response(text="StarMarket Бэкенд запущен и работает! 🚀")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_index)
    runner = web.AppRunner(app)
    await runner.setup()
    # Бесплатный Render автоматически передает нужный порт в переменную PORT, по умолчанию берем 8080
    import os
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Микро-веб-сервер успешно запущен на порту {port}")

async def main():
    # Запускаем сайт-заглушку для прохождения проверки Render
    await start_web_server()
    
    # Очищаем зависшие сообщения и запускаем чтение команд Telegram
    await bot.delete_webhook(drop_pending_updates=True)
    print("🚀 Робот StarMarket успешно подключен к Telegram!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

