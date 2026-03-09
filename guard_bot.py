import os
import asyncio
from telegram import Bot
import logging

logging.basicConfig(level=logging.INFO)

SLEEP_BOT_TOKEN = os.getenv("SLEEP_BOT_TOKEN")
YOUR_USER_ID = os.getenv("YOUR_USER_ID")
MAIN_BOT_USERNAME = os.getenv("MAIN_BOT_USERNAME")

last_update_file = "last_update.txt"

def get_last_update_id():
    try:
        with open(last_update_file, 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def save_last_update_id(update_id):
    with open(last_update_file, 'w') as f:
        f.write(str(update_id))

async def check_and_reply():
    bot = Bot(token=SLEEP_BOT_TOKEN)
    last_id = get_last_update_id()

    try:
        updates = await bot.get_updates(offset=last_id + 1, timeout=30)

        for update in updates:
            if not update.message or update.message.from_user.is_bot:
                continue

            if str(update.message.from_user.id) == YOUR_USER_ID:
                continue

            msg = update.message
            user = msg.from_user
            text = msg.text or msg.caption or "[медиа/стикер/гс]"

            # Отправляем короткий автоответ
            await bot.send_message(
                chat_id=msg.chat.id,
                text="Люкс спит. 😴 
Попробуйте позже."
            )

            # Пересылаем тебе в личку
            await bot.send_message(
                chat_id=YOUR_USER_ID,
                text=(
                    f"📩 **Сообщение для Люкса (бот спит)**\n"
                    f"От: {user.first_name}\n"
                    f"Текст: {text}"
                ),
                parse_mode="Markdown"
            )

            if update.update_id > last_id:
                last_id = update.update_id
                save_last_update_id(last_id)

    except Exception as e:
        logging.error(f"Ошибка: {e}")

async def main():
    await check_and_reply()

if __name__ == "__main__":
    asyncio.run(main())