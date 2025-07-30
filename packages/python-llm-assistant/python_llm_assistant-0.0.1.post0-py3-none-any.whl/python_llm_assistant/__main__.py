import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from python_llm_assistant.config import BOT_TOKEN, VERSION

# Basic logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handler for /start command"""
    await message.answer(f"Bot version: {VERSION}")


@dp.message()
async def handle_message(message: types.Message):
    """Handler for all messages"""
    await message.answer(f"Bot version: {VERSION}")


async def main():
    """Main function to start the bot"""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
