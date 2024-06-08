from aiogram import executor, Dispatcher
from handlers import dp
from loader import bot


async def on_shutdown(dp: Dispatcher) -> None:
    await bot.close()


if __name__ == "__main__":
    executor.start_polling(dp, on_shutdown=on_shutdown, skip_updates=True)
