import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from database.sqlite_db_user import CreateDB
from keyboards.reply.choise_reply_buttons import keyboards_reply
from keyboards.inline.choice_inline_buttons import inline_keyboards
from keyboards.inline.callback_datas import basket_callback, Delivery
from loader import dp, bot
from handlers.ukr_users.each_bouquet import get_data
from handlers.ukr_users.states import States_


values_delivery = """(id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, user_fname TEXT, user_lname TEXT,
        bouquet TEXT, how_many INTEGER, how_much_it TEXT,
        style TEXT,is_fulfilled TEXT,contact TEXT, zakaz_time_str TEXT, order_time TIMESTAMP,
        location_name TEXT)"""
DL = CreateDB(db_file_name="flower.db", tabel_name="shopping")
DL.set_db(values=values_delivery)


@dp.callback_query_handler(Delivery.filter(item_name="Delivery"))
async def buy_chooses(call: CallbackQuery, callback_data: dict, state: FSMContext):
    try:
        t_conn = sqlite3.connect("flower.db")
        t_curr = t_conn.cursor()
        t_curr.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
        )
        select = t_curr.fetchall()
        translate_dict = {
            "eng": "Do you want to add inscription in the bouquet?",
            "ukr": "Хочете додати листівку в букет?",
        }
        callback_data["how_many"] = call.message.reply_markup.inline_keyboard[0][1].text
        # print(f'User_id: {call.message.chat.id}, Chat_id: {call.message.message_id},   {callback_data=}')
        if callback_data["which_item"] == "Коробка":
            open_p = "Box"
        else:
            open_p = callback_data["which_item"].split()[0]
        async with state.proxy() as data:
            if (
                callback_data["which_item"] == "Коробка"
                or callback_data["which_item"] == "Box"
            ):
                data["which_item"] = "Коробка"
            else:
                data["which_item"] = callback_data["which_item"].split()[0]

        try:
            with open(f"imgs/{open_p}units.jpg", "rb") as photo_:
                await bot.send_photo(
                    chat_id=call.message.chat.id,
                    photo=photo_,
                    caption=translate_dict[select[0][0]],
                    reply_markup=keyboards_reply[select[0][0]]["yes_or_no"],
                )
        except:
            with open("imgs/Kоробкa.jpg", "rb") as photo_:
                await bot.send_photo(
                    chat_id=call.message.chat.id,
                    photo=photo_,
                    caption=translate_dict[select[0][0]],
                    reply_markup=keyboards_reply[select[0][0]]["yes_or_no"],
                )

        v = "(user_id, user_fname, user_lname, bouquet, how_many, how_much_it, style, is_fulfilled, contact, zakaz_time_str, order_time)"
        async with state.proxy() as data:
            values = (
                call.message.chat.id,
                call.message.chat.first_name,
                call.message.chat.last_name,
                data["which_item"],
                int(callback_data["how_many"]),
                callback_data["how_much_it"],
                "Without inscription",
                "No",
                None,
                None,
                None,
            )
        await DL.add_db(
            values=values, str_v=v, how_many_values="(?,?,?,?,?,?,?,?,?,?,?)"
        )
        await States_.CHOOSING_OPTION.set()
    except:
        await bot.send_message(
            call.message.chat.id,
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(text=["❌ Ні", "❌ No"], state=States_.CHOOSING_OPTION)
async def process_cancel_style(message: Message, state: FSMContext):
    try:
        t_conn = sqlite3.connect("flower.db")
        t_curr = t_conn.cursor()
        t_curr.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
        )
        select = t_curr.fetchall()
        translate_dict = {
            "eng": "The selected bouquet has been added to the cart🌸",
            "ukr": "Букет доданий в корзину🌸",
        }
        async with state.proxy() as data:
            if data["which_item"] == "Коробка":
                await message.answer(
                    translate_dict[select[0][0]],
                    reply_markup=keyboards_reply[select[0][0]]["Box"],
                )
            else:
                await message.answer(
                    translate_dict[select[0][0]],
                    reply_markup=keyboards_reply[select[0][0]]["Bouquet"],
                )
        await state.finish()
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(text=["✅ Так", "✅ Yes"], state=States_.CHOOSING_OPTION)
async def process_make_style(message: Message, state: FSMContext):
    try:
        t_conn = sqlite3.connect("flower.db")
        t_curr = t_conn.cursor()
        t_curr.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
        )
        select = t_curr.fetchall()
        translate_dict = {
            "eng": "Write the words you would like to see in the bouquet, for example: Happy Birthday!",
            "ukr": "Напишіть слова для листівки на букеті\nПриклад: З Днем Народження!",
        }

        await States_.STYLE_NAME.set()
        await message.answer(
            translate_dict[select[0][0]],
            reply_markup=keyboards_reply[select[0][0]]["Back_to_Yes"],
        )
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(state=States_.STYLE_NAME)
async def process_write(message: Message, state: FSMContext):
    try:
        t_conn = sqlite3.connect("flower.db")
        t_curr = t_conn.cursor()
        t_curr.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
        )
        select = t_curr.fetchall()
        translate_dict = {"ukr": "Ви повернулися", "eng": "You're back"}
        translate_dict1 = {
            "ukr": "Підтверджуєте, щоб вище написаний текст був надписом на букеті?",
            "eng": "Do you confirm the above written text to be the inscription of the bouquet?",
        }
        async with state.proxy() as data:
            if (message.text == "⬅ Назад" and data["which_item"] == "Коробка") or (
                message.text == "⬅ Back" and data["which_item"] == "Box"
            ):
                await message.answer(
                    translate_dict[select[0][0]],
                    reply_markup=keyboards_reply[select[0][0]]["Box"],
                )
                await state.finish()
            elif message.text == "⬅ Back" or message.text == "⬅ Назад":
                await message.answer(
                    translate_dict[select[0][0]],
                    reply_markup=keyboards_reply[select[0][0]]["Bouquet"],
                )
                await state.finish()
            else:
                data["style"] = message.text
                await message.answer(
                    translate_dict1[select[0][0]],
                    reply_markup=inline_keyboards[select[0][0]]["confirmation"],
                )
                await States_.CONFIRMATION.set()
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.callback_query_handler(text="confirm", state=States_.CONFIRMATION)
async def confirm_inscription_style(call: CallbackQuery, state: FSMContext):
    try:
        t_conn = sqlite3.connect("flower.db")
        t_curr = t_conn.cursor()
        t_curr.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {str(call.message.chat.id)}"
        )
        select = t_curr.fetchall()
        translate_dict1 = {
            "ukr": "Супер, букет з цією листівкою додано до корзини",
            "eng": "All right, the bouquet with inscription added to cart",
        }
        async with state.proxy() as data:
            if data["which_item"] == "Коробка":
                conn = sqlite3.connect("flower.db")
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id FROM shopping WHERE user_id = ? AND id ORDER BY id DESC LIMIT 1",
                    (str(call.message.chat.id),),
                )
                last_id = cursor.fetchall()[0]
                cursor.execute(
                    "UPDATE shopping SET style = ? WHERE user_id = ? AND bouquet = ? AND id = ?",
                    (
                        data["style"],
                        call.message.chat.id,
                        data["which_item"],
                        last_id[0],
                    ),
                )
                conn.commit()
                await bot.send_message(
                    chat_id=call.message.chat.id,
                    text=translate_dict1[select[0][0]],
                    reply_markup=keyboards_reply[select[0][0]]["Box"],
                )
            else:
                conn = sqlite3.connect("flower.db")
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id FROM shopping WHERE user_id = ? AND id ORDER BY id DESC LIMIT 1",
                    (str(call.message.chat.id),),
                )
                last_id = cursor.fetchall()[0]
                cursor.execute(
                    "UPDATE shopping SET style = ? WHERE user_id = ? AND bouquet = ? AND id = ?",
                    (
                        data["style"],
                        call.message.chat.id,
                        data["which_item"],
                        last_id[0],
                    ),
                )
                conn.commit()
                conn.close()
                await bot.send_message(
                    chat_id=call.message.chat.id,
                    text=translate_dict1[select[0][0]],
                    reply_markup=keyboards_reply[select[0][0]]["Bouquet"],
                )

            await bot.delete_message(
                chat_id=call.message.chat.id, message_id=call.message.message_id
            )
            await state.finish()
    except:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command",
        )


@dp.callback_query_handler(text="cancel", state=States_.CONFIRMATION)
async def reject_inscription_style(call: CallbackQuery, state: FSMContext):
    try:
        t_conn = sqlite3.connect("flower.db")
        t_curr = t_conn.cursor()
        t_curr.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
        )
        select = t_curr.fetchall()
        translate_dict = {
            "ukr": "Ви відмінили те, що написали",
            "eng": "You canceled what you wrote",
        }
        async with state.proxy() as data:
            if data["which_item"] == "Коробка":
                await bot.send_message(
                    chat_id=call.message.chat.id,
                    text=translate_dict[select[0][0]],
                    reply_markup=keyboards_reply[select[0][0]]["Box"],
                )
            else:
                await bot.send_message(
                    chat_id=call.message.chat.id,
                    text=translate_dict[select[0][0]],
                    reply_markup=keyboards_reply[select[0][0]]["Bouquet"],
                )
        await bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
        await state.finish()

    except:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command",
        )


@dp.callback_query_handler(lambda query: query.data.startswith("del"))
async def delete_each_delivery(call: CallbackQuery):
    try:
        t_conn = sqlite3.connect("flower.db")
        t_curr = t_conn.cursor()
        t_curr.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
        )
        select = t_curr.fetchall()
        translate_dict = {
            "ukr": "Вибачте, щось пішло не так, спробуйте ще раз",
            "eng": "Sorry, something went wrong, try again",
        }
        translate_dict1 = {
            "ukr": "Ваша корзина порожня",
            "eng": "Your cart is empty",
        }
        data = call.data
        t = (
            data.split("del")[1].split("-")[0]
            if data.split("del")[1] != "Коробка"
            else "Коробка"
        )
        try:
            conn = sqlite3.connect("flower.db")
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM shopping WHERE bouquet = ? AND user_id = ? AND is_fulfilled = ?",
                (t, str(call.message.chat.id), "No"),
            )
            conn.commit()
            cursor.execute(
                "SELECT how_many, bouquet, how_much_it FROM shopping WHERE user_id=? AND is_fulfilled=?",
                (call.message.chat.id, "No"),
            )
            query = cursor.fetchall()
            set_select = set([i[1] for i in query])

            if select[0][0] == "ukr" and set_select:
                group, total_price, tariff, total = get_data(query)
                key = [
                    types.InlineKeyboardButton(
                        text="❌" + i, callback_data="del{}".format(i)
                    )
                    for i in set_select
                ]
                new_but = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="🚖 Замовлення",
                                callback_data="open_delivery",
                                cache_time=1,
                            )
                        ],
                        [
                            InlineKeyboardButton(text="⬅ Назад", callback_data="close"),
                            InlineKeyboardButton(
                                text="🗑 Очистити корзину", callback_data="clear_to_"
                            ),
                        ],
                    ]
                ).add(*key)
                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=f"📥 В корзині:\n{group.to_string(index=False, header=False)}\nТовар: {str(total_price)} grn\nДоставка: {tariff}\nВсього: {total} grn",
                    reply_markup=new_but,
                )
            elif set_select and select[0][0] == "eng":
                group, total_price, tariff, total = get_data(query)
                ukr = [
                    "101",
                    "201",
                    "301",
                    "401",
                    "501",
                    "601",
                    "701",
                    "1001",
                    "Коробка",
                ]
                eng = [
                    "101 roses",
                    "201 roses",
                    "301 roses",
                    "401 roses",
                    "501 roses",
                    "601 roses",
                    "701 roses",
                    "1001 roses",
                    "Box",
                ]
                get_it = dict(zip(ukr, eng))
                key = [
                    types.InlineKeyboardButton(
                        text="❌" + get_it[i], callback_data="del{}".format(i)
                    )
                    for i in set_select
                ]
                new_but = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="🚖 Order",
                                callback_data="open_delivery",
                                cache_time=1,
                            )
                        ],
                        [
                            InlineKeyboardButton(text="⬅ Back", callback_data="close"),
                            InlineKeyboardButton(
                                text="🗑 Empty basket", callback_data="clear_to_"
                            ),
                        ],
                    ]
                ).add(*key)
                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=f"📥 In the basket:\n{group.to_string(index=False, header=False)}\nProduct: {str(total_price)} grn\nDelivery: {tariff}\n Total: {total} grn",
                    reply_markup=new_but,
                )

            else:
                await bot.send_message(
                    chat_id=call.message.chat.id, text=translate_dict1[select[0][0]]
                )
                await bot.delete_message(
                    chat_id=call.message.chat.id, message_id=call.message.message_id
                )
        except:
            await call.message.answer(text=translate_dict[select[0][0]])
            await bot.delete_message(
                chat_id=call.message.chat.id, message_id=call.message.message_id
            )
    except:
        await bot.send_message(
            call.message.chat.id,
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.callback_query_handler(basket_callback.filter(item_name="minus"))
async def subtract_the_choice(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    minus = -1
    text = int(call.message.reply_markup.inline_keyboard[0][1].text) + minus
    if text > 0:
        call.message.reply_markup.inline_keyboard[0][1].text = str(text)
        temp = types.InlineKeyboardMarkup(
            inline_keyboard=call.message.reply_markup.inline_keyboard
        )
        await bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=temp,
        )


@dp.callback_query_handler(basket_callback.filter(item_name="sum"))
async def how_many_choices(call: CallbackQuery, callback_data: dict):
    try:
        t_conn = sqlite3.connect("flower.db")
        t_curr = t_conn.cursor()
        t_curr.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
        )
        select = t_curr.fetchall()
        translate_dict = {"ukr": "одиниць", "eng": "pcs"}
        await call.answer(translate_dict[select[0][0]])
    except:
        await bot.send_message(
            call.message.chat.id,
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.callback_query_handler(basket_callback.filter(item_name="plus"))
async def add_the_choice(call: CallbackQuery, callback_data: dict):
    try:
        t_conn = sqlite3.connect("flower.db")
        t_curr = t_conn.cursor()
        t_curr.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
        )
        select = t_curr.fetchall()
        translate_dict = {
            "ukr": "Будь ласка, зачекайте, це може зайняти кілька хвилин, дякую за ваше терпіння",
            "eng": "Please wait, this may take a few minutes, thank you for your patience",
        }

        await call.answer(cache_time=1)
        minus = 1
        text = int(call.message.reply_markup.inline_keyboard[0][1].text)
        call.message.reply_markup.inline_keyboard[0][1].text = str(text + minus)
        temp = types.InlineKeyboardMarkup(
            inline_keyboard=call.message.reply_markup.inline_keyboard
        )
        try:
            await bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=temp,
            )
        except:
            await call.answer(translate_dict[select[0][0]])
    except:
        await bot.send_message(
            call.message.chat.id,
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.callback_query_handler(text="close")
async def back_for_inline(call: CallbackQuery):
    await bot.delete_message(
        chat_id=call.message.chat.id, message_id=call.message.message_id
    )


@dp.callback_query_handler(text="clear_to_")
async def clear_for_inline(call: CallbackQuery):
    conn = sqlite3.connect("flower.db")
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM shopping WHERE user_id = ? AND is_fulfilled = ?",
        (call.message.chat.id, "No"),
    )
    conn.commit()
    conn.close()
    await bot.delete_message(
        chat_id=call.message.chat.id, message_id=call.message.message_id
    )


@dp.callback_query_handler(text="open_delivery")
async def forward_callback(call: CallbackQuery):
    try:
        t_conn = sqlite3.connect("flower.db")
        t_curr = t_conn.cursor()
        t_curr.execute(
            f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
        )
        select = t_curr.fetchall()
        translate_dict = {
            "ukr": "Оберіть зручний час для доставки замовлення:",
            "eng": "Choose a time for you to accept your order:",
        }
        await call.message.answer(
            text=translate_dict[select[0][0]],
            reply_markup=keyboards_reply[select[0][0]]["Order"],
        )
    except:
        await bot.send_message(
            call.message.chat.id,
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )
