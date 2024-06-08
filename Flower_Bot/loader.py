import logging
import os
from typing import Callable

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

load_dotenv()

PROXY_URL = "http://proxy.server:3128"
bot = Bot(token=os.environ.get("TOKEN"))


async def my_middleware(
    update: types.Update,
    dispatcher: Dispatcher,
    next_handler: Callable[..., types.Update],
) -> None:
    await next_handler(update)


dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(
    format="%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s",
    level=logging.INFO,
)
