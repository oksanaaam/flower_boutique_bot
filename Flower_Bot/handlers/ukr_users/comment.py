import pytz

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from datetime import datetime

from database.sqlite_db_user import CreateDB
from handlers.ukr_users.states import Comments_
from handlers.ukr_users.purchase import TRANSLATE_USER_LANG
from keyboards.reply.choise_reply_buttons import keyboards_reply
from loader import dp

ukr_now = datetime.now(pytz.timezone("Europe/Kiev"))

query_comments = "(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, comments TEXT NOT NULL, text_time TEXT NOT NULL)"
creat_db = CreateDB(db_file_name="flower.db", tabel_name="comment")
creat_db.set_db(values=query_comments)


@dp.message_handler(text=["✍️ Comment", "✍️ Залишити коментар"])
async def commenting(message: Message, state: FSMContext):
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        dict_f = {
            "ukr": "Якщо у вас є зауваження чи недоліки щодо нашого бота, напишіть це, і ми постараємося це виправити",
            "eng": "Write your thoughts about our bot or we will try to correct the bot's shortcomings",
        }
        cursor.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
        )
        select = cursor.fetchall()
        await message.answer(
            dict_f[select[0][0]],
            reply_markup=keyboards_reply[select[0][0]]["Back_to_Yes"],
        )
        await Comments_.comments.set()
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду /start\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(state=Comments_.comments)
async def write_comment(message: Message, state: FSMContext):
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        dict_f = {"ukr": "Ви в головному меню", "eng": "You are in the main menu"}
        dict_f1 = {
            "ukr": "Дякуємо за вашу оцінку, нам важлива кожна думка",
            "eng": "Thank you for rating our service, your opinion is very important to us",
        }
        cursor.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
        )
        select = cursor.fetchall()

        user_id = message.chat.id if message.chat.id else None
        if message.text == "⬅ Back" or message.text == "⬅ Назад":
            await message.answer(
                dict_f[select[0][0]],
                reply_markup=keyboards_reply[select[0][0]]["start"],
            )
        else:
            await creat_db.add_db(
                values=(user_id, message.text, str(ukr_now)),
                str_v="(user_id, comments, text_time)",
                how_many_values="(?, ?, ?)",
            )
            await message.answer(
                dict_f1[select[0][0]],
                reply_markup=keyboards_reply[select[0][0]]["start"],
            )
        await state.finish()
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )
