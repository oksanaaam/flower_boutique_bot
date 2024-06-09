from aiogram import types

from handlers.ukr_users.purchase import TRANSLATE_USER_LANG
from keyboards.reply.choise_reply_buttons import keyboards_reply
from loader import dp


@dp.message_handler(text=["⬅ Назад", "⬅ Back"])
async def back(message: types.Message) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        dict_f = {
            "ukr": "Виберіть одне з наступного:",
            "eng": "Select one of the following:",
        }
        cursor.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
        )
        select = cursor.fetchall()
        await message.answer(
            dict_f.get(select[0][0], dict_f["ukr"]),
            reply_markup=keyboards_reply.get(select[0][0], dict_f["ukr"])["start"],  # type: ignore[index]
        )
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(text=["⬅ Назад до локації", "⬅ Back to location address"])
async def back_location(message: types.Message) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        dict_f = {
            "ukr": "📍 Надішліть адресу доставки замовлення",
            "eng": "📍 Send the delivery location",
        }
        cursor.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
        )
        select = cursor.fetchall()
        await message.answer(
            dict_f.get(select[0][0], dict_f["ukr"]),
            reply_markup=keyboards_reply.get(select[0][0], dict_f["ukr"])["location"],  # type: ignore[index]
        )
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(text=["⬅ Повернутись до букетів", "⬅ Back to bouquets"])
async def back_to_bouquet(message: types.Message) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        dict_f: dict[str, str] = {
            "ukr": "Виберіть букети",
            "eng": "Select bouquets:",
        }
        cursor.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
        )
        select: list[tuple[str]] = cursor.fetchall()
        await message.answer(
            dict_f.get(select[0][0], dict_f["ukr"]),
            reply_markup=keyboards_reply.get(select[0][0], dict_f["ukr"])["Bouquet"],  # type: ignore[index]
        )
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(text=["⬅ Повернутись до меню", "⬅ Back to menu"])
async def back_to_menu(message: types.Message) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        dict_f = {
            "ukr": "Виберіть одне з наступного:",
            "eng": "Select one of the following:",
        }
        cursor.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
        )
        select = cursor.fetchall()
        await message.answer(
            dict_f.get(select[0][0], dict_f["ukr"]),
            reply_markup=keyboards_reply.get(select[0][0], dict_f["ukr"])["Menu"],  # type: ignore[index]
        )
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(text=["⬅ Назад до встановлення часу", "⬅ Back to set time"])
async def back_to_setting_time(message: types.Message) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        dict_f = {
            "ukr": "Виберіть одне з наступного:",
            "eng": "Select one of the following:",
        }
        cursor.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
        )
        select = cursor.fetchall()
        await message.answer(
            dict_f.get(select[0][0], dict_f["ukr"]),
            reply_markup=keyboards_reply.get(select[0][0], dict_f["ukr"])["Order"],  # type: ignore[index]
        )
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )
