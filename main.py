import asyncio
import logging
from aiogram import Bot, Dispatcher, types
import random

import utils
from TOKEN import token
import parsers


logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    await message.answer(text=utils.HELPER_TEXT)


@dp.message_handler(commands=["matches"])
async def send_matches(message: types.Message):
    for match in parsers.matches_parser():
        await message.answer(text=match)


@dp.message_handler(commands=["news"])
async def send_news(message: types.Message):
    for news in parsers.news_parser():
        await message.answer(text=str(news[1]) + '\n' + news[0])


@dp.message_handler(commands=["table"])
async def send_table(message: types.Message):
    await message.answer(text=parsers.table_parser())


@dp.message_handler(commands=["photo"])
async def send_photo(message: types.Message):
    for photo in parsers.photo_parser():
        await message.answer(text=str(photo))


@dp.message_handler(commands=["player"])
async def send_photo(message: types.Message):
    players = parsers.players_parser()
    player = players[random.randrange(0, len(players))]
    await message.answer(text=str(player[0]) + '\n' + player[1])


@dp.message_handler()
async def unknown_message(message: types.Message):
    """Ответ на любое неожидаемое сообщение"""
    await message.answer(text=utils.UNKNOWN_TEST)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())