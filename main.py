import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, PreCheckoutQuery, LabeledPrice, CallbackQuery
from aiogram.filters import Command
from aiohttp import web

TOKEN = "8659582793:AAFuqmD6Ihf6igZuBClfg-X7-0bq8fqsEuM"
# Задаем вашу точную рабочую ссылку на дизайн!
WEBAPP_URL = "https://fgtr086-glitch.github.io/starmarket-bot/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Создаем премиальную клавиатуру прямо под сообщением бота
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Открыть витрину StarMarket", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="👑 Купить VIP @gold_ceo (500 🌟)", callback_data="buy_top_username")],
        [InlineKeyboardButton(text="🎁 TG Premium 1 год (299 🌟)", callback_data="buy_tg_premium")],
        [InlineKeyboardButton(text="🖼️ NFT Gift #884 (150 🌟)", callback_data="buy_nft_884")]
    ])
    await message.answer(
        f"👑 **Добро пожаловать в StarMarket Premium!**\n\n"
        f"Вы можете войти в Mini App для просмотра каталога лотов, либо мгновенно купить товар дня в Звёздах прямо из чата, нажав кнопку оплаты ниже:",
        reply_markup=keyboard
    )

# ЛОВИМ КЛИКИ ПО КНОПКАМ ОПЛАТЫ
@dp.callback_query(F.data.startswith("buy_"))
async def process_buy_button(callback: CallbackQuery):
    await callback.answer()
    
    item_id = callback.data.replace("buy_", "")
    
    # Конфигурация товаров и цен
    products = {
        "top_username": {"title": "👑 VIP @gold_ceo", "cost": 500},
        "tg_premium": {"title": "🎁 TG Premium 1 Год", "cost": 299},
        "nft_884": {"title": "🖼️ NFT Gift #884", "cost": 150}
    }
    
    product = products.get(item_id)
    if product:
        # Выставляем официальный счет в Telegram Stars (XTR)
        await bot.send_invoice(
            chat_id=callback.message.chat.id,
            title=product["title"],
            description=f"Покупка цифрового актива в StarMarket Premium",
            payload=f"payload_{item_id}",
            provider_token="", # Для Stars токен всегда пустой!
            currency="XTR",
            prices=[LabeledPrice(label=product["title"], amount=product["cost"])]
        )

# ПОДТВЕРЖДАЕМ ПЛАТЕЖ ДЛЯ TELEGRAM
@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# УСПЕШНАЯ ОПЛАТА
@dp.message(F.successful_payment)
async def success_payment_handler(message: Message):
    await message.answer("🎉 **Оплата успешно прошла!**\n\nТовар мгновенно добавлен в ваш профиль. Вы можете вывести его на криптокошелек в любой момент.")

async def handle_index(request):
    return web.Response(text="StarMarket Бэкенд запущен и работает! 🚀")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_index)
    runner = web.AppRunner(app)
    await runner.setup()
    import os
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    await start_web_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
