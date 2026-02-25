import asyncio
import json
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

# 🔐 Environment dan olish
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(F.web_app_data)
async def web_app_handler(message: Message):

    data = json.loads(message.web_app_data.data)

    text = (
        "🍔 <b>YANGI BUYURTMA</b>\n\n"
        f"👤 Ism: {data['name']}\n"
        f"📞 Telefon: {data['phone']}\n\n"
        f"🍔 Burger: {data['burger']}\n"
        f"🌯 Lavash: {data['lavash']}\n"
        f"🥤 Cola: {data['cola']}\n\n"
        f"💰 Jami: {data['total']} so'm\n\n"
        "🟡 Status: Kutilmoqda"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_{message.from_user.id}"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_{message.from_user.id}")
        ]
    ])

    await bot.send_message(ADMIN_ID, text, reply_markup=kb)
    await message.answer("🟡 Buyurtma yuborildi!")


@dp.callback_query()
async def handle_callback(callback: CallbackQuery):

    action, user_id = callback.data.split("_")
    user_id = int(user_id)

    if action == "confirm":
        await bot.send_message(user_id, "🟢 Buyurtmangiz tasdiqlandi!")
        await callback.message.edit_text(
            callback.message.text.replace("🟡 Kutilmoqda", "🟢 Tasdiqlandi")
        )

    elif action == "cancel":
        await bot.send_message(user_id, "🔴 Buyurtmangiz bekor qilindi.")
        await callback.message.edit_text(
            callback.message.text.replace("🟡 Kutilmoqda", "🔴 Bekor qilindi")
        )


async def main():
    print("🚀 BOT ISHGA TUSHDI")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())