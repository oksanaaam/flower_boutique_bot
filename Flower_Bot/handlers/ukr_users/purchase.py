import openai
import os
import sqlite3
import pytz

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.utils.markdown import code, italic, text
from datetime import datetime
from dotenv import load_dotenv

from database.sqlite_db_user import CreateDB
from handlers.ukr_users.each_bouquet import get_data
from handlers.ukr_users.states import (
    AddressState,
    OrderConfirmation,
    StateOrderTime,
    Translate,
    HelpConversation,
)
from keyboards.inline.choice_inline_buttons import inline_keyboards
from keyboards.reply.choise_reply_buttons import keyboards_reply
from loader import bot, dp
from prompts.generator import PromptsGenerator

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

ukr_date = pytz.timezone("Europe/Kiev")
order_current_time = datetime.now(ukr_date).strftime("%Y-%m-%d %H:%M")


####################DB_CREATE_PLACE###################################
TRANSLATE_USER_LANG = CreateDB(
    db_file_name="flower.db", tabel_name="translates_from_id"
)
TRANSLATE_USER_LANG.set_db(
    values="""(user_id INTEGER PRIMARY KEY,language TEXT NOT NULL)"""
)


@dp.message_handler(text="🇺🇦 Українська")
async def to_ukrainian(message: types.Message) -> None:
    conn, cursor = TRANSLATE_USER_LANG.query_sql()
    cursor.execute(
        "UPDATE translates_from_id SET language = ? WHERE rowid = (SELECT rowid FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1)",
        ("ukr", int(message.chat.id)),
    )
    conn.commit()
    dict_f = {"ukr": "Ласкаво просимо до нашого квіткового магазину🌸🌷"}
    cursor.execute(
        "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
        (message.chat.id,),
    )
    select = cursor.fetchall()
    await message.answer(
        dict_f[select[0][0]], reply_markup=keyboards_reply[select[0][0]]["start"]
    )


@dp.message_handler(text="🇺🇸 English")
async def to_english(message: types.Message) -> None:
    conn, cursor = TRANSLATE_USER_LANG.query_sql()
    cursor.execute(
        "UPDATE translates_from_id SET language = ? WHERE rowid = (SELECT rowid FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1)",
        ("eng", int(message.chat.id)),
    )
    conn.commit()
    dict_f = {"eng": "Hi, welcome to our flower shop🌸🌷"}
    cursor.execute(
        "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
        (message.chat.id,),
    )
    select = cursor.fetchall()
    await message.answer(
        dict_f[select[0][0]], reply_markup=keyboards_reply[select[0][0]]["start"]
    )


@dp.message_handler(
    content_types=[
        types.ContentType.STICKER,
        types.ContentType.AUDIO,
        types.ContentType.STICKER,
        types.ContentType.UNKNOWN,
    ]
)
async def unknown_message(msg: types.Message) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        cursor.execute(
            "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
            (msg.chat.id,),
        )

        select = cursor.fetchall()

        message_text = text(
            "Вибачте, бот вас не зрозумів," + "\U0001F914",
            italic("\nкоманда,"),
            code("/help"),
            "допоможе зрозуміти бота",
        )
        message_text1 = text(
            "Sorry, I don't know what to do with this" + "\U0001F914",
            italic("\nI'll just remind you,"),
            "what is",
            code("command"),
            "/help",
        )
        dict_f = {"eng": message_text1, "ukr": message_text}
        await msg.reply(dict_f[select[0][0]], parse_mode=types.ParseMode.MARKDOWN)
    except:
        await msg.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message) -> None:
    conn, cursor = TRANSLATE_USER_LANG.query_sql()
    try:
        cursor.execute(
            "INSERT INTO translates_from_id (user_id, language) VALUES (?,?)",
            (int(message.chat.id), "ukr"),
        )
    except:
        cursor.execute(
            "UPDATE translates_from_id SET language = ? WHERE rowid = (SELECT rowid FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1)",
            ("ukr", int(message.chat.id)),
        )

    conn.commit()
    dict_f = {"ukr": "🇺🇦 Виберіть мову:\n🇺🇸 Choose language:"}
    cursor.execute(
        "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
        (message.chat.id,),
    )

    select = cursor.fetchall()
    await message.answer(
        dict_f[select[0][0]],
        reply_markup=keyboards_reply[select[0][0]]["change_language_begin"],
    )


@dp.message_handler(text=["🌹 Меню", "🌹 Menu"])
async def main_menu(message: types.Message) -> None:
    try:
        dict_f = {
            "ukr": "Виберіть тип букета:",
            "eng": "Choose the type of bouquet that suits you:",
        }
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        cursor.execute(
            "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
            (message.chat.id,),
        )
        select = cursor.fetchall()
        await message.answer(
            dict_f[select[0][0]], reply_markup=keyboards_reply[select[0][0]]["Menu"]
        )
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(
    Text(
        [
            "🥡 Квіти в боксі",
            "💐 Квіти в букеті",
            "🥡 Flowers in a box",
            "💐 Flowers in a bouquet",
        ]
    )
)
async def choose_type_of_flowers(
    message_flowers_in_box: types.Message, state: FSMContext
) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        dict_f = {
            "ukr": "Виберіть кількість букетів:",
            "eng": "Chose the number of bouquets:",
        }
        price = (
            inline_keyboards["ukr"]["to_box"]
            .inline_keyboard[1][0]
            .callback_data.split(":")[-1]
        )
        dict_f1 = {
            "ukr": f"Вибраний вами букет: 🥡 У коробці\nЦіна: {price} grn",
            "eng": f"The bouquet you chose:🥡 Flowers in a box\n\nPrice: {price} grn",
        }
        dict_f2 = {
            "ukr": "Виберіть одне з наступного:",
            "eng": "Select one of the following:",
        }
        cursor.execute(
            "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
            (message_flowers_in_box.chat.id,),
        )

        select = cursor.fetchall()
        if (
            message_flowers_in_box.text == "🥡 Квіти в боксі"
            or message_flowers_in_box.text == "🥡 Flowers in a box"
        ):
            await message_flowers_in_box.answer(
                dict_f[select[0][0]], reply_markup=keyboards_reply
            )
            with open("imgs/Kоробкa.jpg", "rb") as photo_:
                await bot.send_photo(
                    message_flowers_in_box.chat.id,
                    photo=photo_,
                    caption=f"{dict_f1[select[0][0]]}",
                    reply_markup=inline_keyboards[select[0][0]]["to_box"],
                )

        elif (
            message_flowers_in_box.text == "💐 Квіти в букеті"
            or message_flowers_in_box.text == "💐 Flowers in a bouquet"
        ):
            await message_flowers_in_box.answer(
                dict_f2[select[0][0]],
                reply_markup=keyboards_reply[select[0][0]]["Bouquet"],
            )
    except:
        await message_flowers_in_box.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(text=["📭 Якнайшвидша доставка", "📭 Immediately delivery"])
async def immediately_delivery(immediately_message: types.Message) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        dict_f = {
            "ukr": "Доставка здійснюється до 90 хвилин🚴‍♂️\nВведіть адресу для доставки у форматі: Місто Львів, вул. Львівська, 1",
            "eng": "Delivery within 90 minutes🚴‍♂️\nEnter the delivery address in the format: City Lviv, Lvivska street, 1",
        }
        cursor.execute(
            "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
            (immediately_message.chat.id,),
        )

        select = cursor.fetchall()
        await immediately_message.answer(
            dict_f[select[0][0]], reply_markup=keyboards_reply[select[0][0]]["location"]
        )

        conn1 = sqlite3.connect("flower.db")
        cursor1 = conn1.cursor()
        cursor1.execute(
            "UPDATE shopping SET zakaz_time_str = ? WHERE rowid = (SELECT rowid FROM shopping WHERE user_id = ? AND is_fulfilled = ? ORDER BY rowid DESC LIMIT 1)",
            ("immediately", immediately_message.chat.id, "No"),
        )
        conn1.commit()
        await AddressState.waiting_for_address.set()
    except Exception as e:
        print(e)
        await immediately_message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


current_time_without_year = datetime.now(ukr_date).strftime("%m.%d.%H:%M")


@dp.message_handler(text=["⏱ Обрати час доставки", "⏱ Set delivery time"])
async def choose_delivery_time(message_key: types.Message, state: FSMContext) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        dict_f = {
            "ukr": f"❗Виберіть час доставки, наш магазин працює кожного дня з 10:00 до 18:00💫\nОберіть час у форматі: місяць.число.година:хвилина, наприклад {current_time_without_year}",
            "eng": f"❗Choose the delivery time, our store works every day from 10:00 to 18:00💫\nChoose the time in the format: Month.Date.Hour:Minute, for example {current_time_without_year}",
        }
        cursor.execute(
            "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
            (message_key.chat.id,),
        )
        select = cursor.fetchall()
        await message_key.answer(
            dict_f[select[0][0]], reply_markup=keyboards_reply[select[0][0]]["cancel"]
        )
        await StateOrderTime.start_order_time.set()
    except:
        await message_key.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(state=StateOrderTime.start_order_time)
async def start_typing_time(message: types.Message, state: FSMContext) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        dict_f = {
            "ukr": "Оберіть зручний час для отримання замовлення",
            "eng": "Select the time that suits you to receive your order",
        }
        dict_f1 = {
            "ukr": "Надішліть адресу куди замовдяєте букет",
            "eng": "To order a bouquet, send location adress",
            "ukr": "🚴‍♂️Введіть адресу для доставки у форматі: Місто Львів, вул. Львівська, 1",
            "eng": "🚴‍♂️Enter the delivery address in the format: City Lviv, Lvivska street, 1",
        }
        dict_f2 = {
            "ukr": f"❌Введений час має не правильний формат\n\nБудь ласка, введіть час доставки\nу такому форматі: місяць.число.година:хвилина:{current_time_without_year}",
            "eng": f"❌The time you entered was entered incorrectly\n\nPlease enter the time for delivery\napplied in this format: Month.Date.Hour:Minute: {current_time_without_year}",
        }
        dict_f3 = {
            "ukr": f"‼️Введена дата має бути в майбутньому та у форматі: місяць.число.година:хвилина⏩ {current_time_without_year}",
            "eng": f"‼️The date entered must be in the future and in the format: Month.Date.Hour:Minute⏩ {current_time_without_year}",
        }
        cursor.execute(
            "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
            (message.chat.id,),
        )
        select = cursor.fetchall()

        if message.text == "⬅ Назад" or message.text == "⬅ Back":
            await message.answer(
                dict_f[select[0][0]],
                reply_markup=keyboards_reply[select[0][0]]["Order"],
            )
            await state.finish()
        else:
            check_it_time = message.text.split(".")
            date_format = "%Y-%m-%d-%H:%M"  # Оновлений формат дати
            try:
                # Перевірка, чи дата не швидше поточного часу
                current_datetime = datetime.now()
                input_datetime = datetime.strptime(
                    str(current_datetime.year)
                    + "-"
                    + "-".join(message.text.split(".")),
                    date_format,
                )
                if input_datetime <= current_datetime:
                    await message.answer(dict_f3[select[0][0]])
                    return

                date_time_obj = input_datetime
                if len(check_it_time) == 3:
                    await message.answer(
                        dict_f1[select[0][0]],
                        reply_markup=keyboards_reply[select[0][0]]["location"],
                    )
                    base = sqlite3.connect("flower.db")
                    curr = base.cursor()
                    curr.execute(
                        "UPDATE shopping SET zakaz_time_str = ? WHERE rowid = (SELECT rowid FROM shopping WHERE user_id = ? AND is_fulfilled = ? ORDER BY rowid DESC LIMIT 1)",
                        (
                            date_time_obj,
                            message.chat.id,
                            "No",
                        ),  # Оновлений параметр дати
                    )
                    base.commit()
                    await AddressState.waiting_for_address.set()
                else:
                    await message.answer(dict_f2[select[0][0]])
            except:
                await message.answer(dict_f2[select[0][0]])
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(commands=["help"], state="*")
async def helper_function(message: types.Message) -> None:
    try:
        await HelpConversation.waiting_for_user_message.set()
        await message.answer("How can I assist you with our flower shop today?")
    except:
        await message.reply(
            "Sorry, there was an error. Restart the bot with /start command please"
        )


@dp.message_handler(state=HelpConversation.waiting_for_user_message)
async def continue_help_conversation(message: types.Message, state: FSMContext) -> None:
    user_message = message.text

    response = openai.ChatCompletion.create(  # type: ignore[no-untyped-call]
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PromptsGenerator.instructions["bot_chat_completion"]},
            {"role": "user", "content": user_message},
        ],
    )

    answer = response.choices[0].message["content"]
    await message.answer(answer, parse_mode=ParseMode.HTML)

    # Stay in the current state to continue the conversation
    await HelpConversation.waiting_for_user_message.set()


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message, state: FSMContext) -> None:
    try:
        phone_number = (
            message.contact.phone_number
            if message.contact and message.contact.phone_number
            else None
        )
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        cursor.execute(
            "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
            (message.chat.id,),
        )
        select = cursor.fetchall()

        dict_f2 = {
            "ukr": "Ваші дані правильні?",
            "eng": "Are your data correct?",
        }
        dict_f1 = {
            "ukr": "Відправте контактний номер, для того щоб зв'язатись з вами",
            "eng": "Send your contact number to get in touch with you",
        }

        if phone_number:
            conn1 = sqlite3.connect("flower.db")
            cursor1 = conn1.cursor()
            cursor1.execute(
                "UPDATE shopping SET contact = ? WHERE rowid = (SELECT rowid FROM shopping WHERE user_id = ? AND is_fulfilled = ? ORDER BY rowid DESC LIMIT 1)",
                (message.contact.phone_number, message.chat.id, "No"),
            )
            conn1.commit()
            cursor1.execute(
                "SELECT * FROM shopping WHERE user_id = ? AND is_fulfilled = ?",
                (str(message.chat.id), "No"),
            )
            orders = cursor1.fetchall()
            conn1.close()
            if orders:
                group, total_price, tariff, total = get_data(
                    [(i[5], i[4], i[6]) for i in orders]
                )

                df_immediately = {
                    "ukr": (
                        "🛍Ваше замовлення: \n{}\n\n"
                        "💵Вартість доставки: {}\n"
                        "💰Всього: {}\n"
                        "️💌Напис на букеті: {}\n"
                        "📞Номер телефону: {}\n"
                        "🏰Адреса замовлення: {}\n"
                        "🚕Час доставки замовлення: {}"
                    ).format(
                        "\n".join(
                            [f"{i[4]}: {i[5]} шт. по {i[6]} grn" for i in orders]
                        ),
                        "0.100 grn.",
                        total + " grn.",
                        "Немає"
                        if orders[-1][7] == "Without inscription"
                        else orders[-1][7],
                        orders[-1][9],
                        orders[-1][12],
                        "Якнайшвидше"
                        if orders[-1][10] == "immediately"
                        else orders[-1][10],
                    ),
                    "eng": (
                        "🛍Your order: \n{}\n\n"
                        "💵Delivery price: {}\n"
                        "💰Total price: {}\n"
                        "️💌The inscription: {}\n"
                        "📞Phone number: {}\n"
                        "🏰Address: {}\n"
                        "🚕Delivery time: {}"
                    ).format(
                        "\n".join(
                            [f"{i[4]}: {i[5]} pc. each {i[6]} grn" for i in orders]
                        ),
                        "0.100 grn.",
                        total + " grn.",
                        orders[-1][7],
                        orders[-1][9],
                        orders[-1][12],
                        orders[-1][10],
                    ),
                }

                df_now = df_immediately[select[0][0]]
                await message.answer(
                    dict_f2[select[0][0]],
                    reply_markup=keyboards_reply[select[0][0]]["last_agree"],
                )
                await message.answer(df_now)
        else:
            await message.answer(dict_f1[select[0][0]])

        await OrderConfirmation.yes_or_no.set()

    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(text=["❌ Ні", "❌ No"], state=OrderConfirmation.yes_or_no)
async def last_process_no(message: types.Message, state: FSMContext) -> None:
    conn, cursor = TRANSLATE_USER_LANG.query_sql()
    cursor.execute(
        "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
        (message.chat.id,),
    )
    select = cursor.fetchall()
    try_again = {
        "ukr": "Зробіть замовлення ще раз, будь ласка",
        "eng": "Please, make an order again",
    }

    try:
        await message.answer(
            try_again[select[0][0]], reply_markup=keyboards_reply[select[0][0]]["start"]
        )
        await state.finish()

    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(text=["✅ Так", "✅ Yes"], state=OrderConfirmation.yes_or_no)
async def last_process_yes(message: types.Message, state: FSMContext) -> None:
    conn, cursor = TRANSLATE_USER_LANG.query_sql()
    cursor.execute(
        "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
        (message.chat.id,),
    )
    select = cursor.fetchall()
    dict_f = {
        "ukr": "Дякуємо за замовлення, ми зв'яжемося з вами найближчим часом💞",
        "eng": "Thank you for your order, we will contact you soon💞",
    }
    try:
        db = sqlite3.connect("flower.db")
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE shopping 
            SET is_fulfilled = ?, order_time = ? 
            WHERE rowid = (
                SELECT rowid 
                FROM shopping 
                WHERE user_id = ? AND is_fulfilled = ? 
                ORDER BY rowid DESC 
                LIMIT 1
            )
            """,
            ("Yes", order_current_time, message.chat.id, "No"),
        )

        db.commit()
        db.close()
        await message.answer(
            dict_f[select[0][0]], reply_markup=keyboards_reply[select[0][0]]["start"]
        )
        await state.finish()
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(
    state=AddressState.waiting_for_address, content_types=types.ContentType.TEXT
)
async def process_location_address(msg: types.Message, state: FSMContext) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        cursor.execute(
            "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
            (msg.chat.id,),
        )
        select = cursor.fetchall()

        address = msg.text
        dict_f = {
            "ukr": "Ваша адреса доставки успішно збережена.\nПоділіться номером телефону: 📞",
            "eng": "Address was successfully saved.\nShare your phone number: 📞",
        }
        dict_f1 = {
            "ukr": "Вибачте, в нас немає доставки окрім міста Львів, будь ласка спробуйте ще раз",
            "eng": "Sorry, there is no delivery outside of Lviv city, please try again",
        }

        if "Львів" in address or "Lviv" in address:
            await msg.answer(
                dict_f[select[0][0]],
                reply_markup=keyboards_reply[select[0][0]]["Contact"],
            )
            conn1 = sqlite3.connect("flower.db")
            cursor1 = conn1.cursor()
            cursor1.execute(
                """
                UPDATE shopping 
                SET location_name = ? 
                WHERE user_id = ? AND is_fulfilled = ? AND rowid = (
                    SELECT rowid FROM shopping 
                    WHERE user_id = ? AND is_fulfilled = ? 
                    ORDER BY rowid DESC 
                    LIMIT 1
                )
                """,
                (
                    address,
                    msg.chat.id,
                    "No",
                    msg.chat.id,
                    "No",
                ),
            )

            conn1.commit()
            conn1.close()
        else:
            await msg.answer(
                dict_f1[select[0][0]],
                reply_markup=keyboards_reply[select[0][0]]["location"],
            )
            return  # func for getting new location

        await state.finish()
    except Exception as e:
        print(e)
        await msg.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(text=["⚙️ Налаштування", "⚙️ Settings"])
async def settings(message: types.Message) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        cursor.execute(
            "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
            (message.chat.id,),
        )
        select = cursor.fetchall()
        dict_f = {
            "ukr": "Виберіть одне з наступного:",
            "eng": "Choose one of the following:",
        }
        await message.answer(
            dict_f[select[0][0]], reply_markup=keyboards_reply[select[0][0]]["settings"]
        )
        await Translate.ukr_eng.set()
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )


@dp.message_handler(state=Translate.ukr_eng)
async def choose_language(message: types.Message, state: FSMContext) -> None:
    try:
        conn, cursor = TRANSLATE_USER_LANG.query_sql()
        cursor.execute(
            "SELECT language FROM translates_from_id WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
            (message.chat.id,),
        )
        select = cursor.fetchall()
        dict_f = {
            "ukr": "Виберіть одне з наступного:",
            "eng": "Choose one of the following:",
        }
        dict_f1 = {"ukr": "Виберіть мову:", "eng": "Choose a language:"}

        if message.text == "⬅ Назад" or message.text == "⬅ Back":
            await message.answer(
                dict_f[select[0][0]],
                reply_markup=keyboards_reply[select[0][0]]["start"],
            )
        else:
            await message.answer(
                dict_f1[select[0][0]],
                reply_markup=keyboards_reply[select[0][0]]["change_language"],
            )
        await state.finish()
    except:
        await message.reply(
            "🇺🇦 У зв'язку з оновленням нашого бота, почніть використовувати команду\n\n🇺🇸 Due to the bot update, restart the bot with the /start command"
        )
