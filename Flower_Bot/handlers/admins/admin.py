import os
from typing import Callable

import pytz
import sqlite3 as sql
from datetime import datetime, timedelta
from dotenv import load_dotenv
from PIL import Image

import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import (
    ContentTypes,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from handlers.ukr_users.states import (
    Advertisement,
    Authentication,
    ChangeBoxPrice,
    ChangeBouquetPrice,
    ChangePicture,
)
from keyboards.inline.choice_inline_buttons import how_much_choise, to_box
from keyboards.inline.english_choise_inline_buttons import (
    how_much_choise_eng,
    to_box_eng,
)
from keyboards.reply.choise_reply_buttons import (
    Admin_back_to_choosing_roses,
    Admin_bouquet_photo,
    Admin_bouquet_price,
    Admin_change_cost,
    Admin_check_comments,
    Admin_orders_markup,
    Admin_panel_buttons,
    Admin_post_advertisement,
)
from loader import bot, dp

load_dotenv()
PASSWORD = os.environ.get("PASSWORD")
ADMIN_ID = os.environ.get("ADMIN_ID")

db = sql.connect("flower.db")
cursor = db.cursor()
ukr_date = pytz.timezone("Europe/Kiev")


def register_handlers(
    reply_button: types.ReplyKeyboardMarkup,
    function: Callable,  # type: ignore[type-arg]
) -> None:
    for row in reply_button.keyboard:
        for button in row:
            dp.register_message_handler(function, Text(button.text), user_id=ADMIN_ID)


@dp.message_handler(user_id=ADMIN_ID, commands=["admin"])
async def admin_panel(message: Message, state: FSMContext) -> None:
    await message.reply(
        "Будь ласка, введіть пароль адміністратора:", reply_markup=ReplyKeyboardRemove()
    )
    await Authentication.password.set()


@dp.message_handler(user_id=ADMIN_ID, text="⬅ Повернутися до меню")
async def back_to_admin_panel(message: Message, state: FSMContext) -> None:
    await message.reply("Адмін панель", reply_markup=Admin_panel_buttons)


@dp.message_handler(user_id=ADMIN_ID, state=Authentication.password)
async def password(message: Message, state: FSMContext) -> None:
    if message.text == PASSWORD:
        await message.reply(
            "Введений пароль правильний, тепер можете обрати опції для адміністратора",
            reply_markup=Admin_panel_buttons,
        )
        await state.finish()
    else:
        await message.reply("Спробуйте ще раз")


@dp.message_handler(user_id=ADMIN_ID, text="💸 Змінити ціну")
async def change_bouquets_cost(message: Message) -> None:
    await message.reply(
        "Ціну якої квіткової композиції ви бажаєте змінити?",
        reply_markup=Admin_change_cost,
    )


@dp.message_handler(user_id=ADMIN_ID, text="🆕 Нові клієнти")
async def new_customers(message: Message) -> None:
    await message.reply(
        "Ви у розділі для перевірки нових клієнтів та замовлень",
        reply_markup=Admin_orders_markup,
    )


@dp.message_handler(user_id=ADMIN_ID, text="🥡 Вартість коробки")
async def current_price(message: Message) -> None:
    await message.answer(
        f'Вартість коробки: {to_box.inline_keyboard[1][0].callback_data.split(":")[-1]} grn\nЯкщо ви хочете змінити ціну, напишіть нижче\nБудь ласка {to_box.inline_keyboard[1][0].callback_data.split(":")[-1]} в такому ж форматі',
        reply_markup=Admin_back_to_choosing_roses,
    )
    await ChangeBoxPrice.change_box_price.set()


@dp.message_handler(user_id=ADMIN_ID, state=ChangeBoxPrice.change_box_price)
async def change_box_cost(message: Message, state: FSMContext) -> None:
    if message.text == "⬅ Назад":
        await message.reply("Ви повернулись", reply_markup=Admin_change_cost)
        await state.finish()
    else:
        current_price_ukr = to_box_eng.inline_keyboard[1][0].callback_data.split(":")[
            -1
        ]
        try:
            changes = message.text
            callback = to_box.inline_keyboard[1][0].callback_data
            callback_eng = to_box_eng.inline_keyboard[1][0].callback_data
            to_box.inline_keyboard[1][0].callback_data = ":".join(
                callback.split(":")[:-1] + [changes]
            )
            to_box_eng.inline_keyboard[1][0].callback_data = ":".join(
                callback_eng.split(":")[:-1] + [changes]
            )
            await message.reply(
                f'Ціну для коробки змінено успішно !!!\nЗмінено ціну на: {to_box.inline_keyboard[1][0].callback_data.split(":")[-1]}',
                reply_markup=Admin_change_cost,
            )
            await state.finish()
        except:
            await message.reply(
                f"Виникла помилка!!!\nВідформатуйте {current_price_ukr} наступним чином"
            )


@dp.message_handler(user_id=ADMIN_ID, text="💐 Вартість букета")
async def choose_bouquet_for_change_cost(message: Message) -> None:
    await message.answer(
        "Оберіть букет, ціну якого ви хочете змінити:", reply_markup=Admin_bouquet_price
    )


async def change_bouquet_cost(message: Message, state: FSMContext) -> None:
    if message.text == "⬅ Повернутись до квітів":
        await message.reply("Ви повернулись", reply_markup=Admin_change_cost)
        await state.finish()
    else:
        for choice in how_much_choise:
            if (
                choice.inline_keyboard[1][0].callback_data.split(":")[-3]
                == message.text.split(" ")[0]
            ):
                async with state.proxy() as data:
                    data["which_item"] = message.text.split(" ")[0]
                    data["price"] = choice.inline_keyboard[1][0].callback_data.split(
                        ":"
                    )[-1]
                await message.answer(
                    f'💐 Вартість букета: {choice.inline_keyboard[1][0].callback_data.split(":")[-1]} grn\nЯкщо ви хочете змінити ціну, напишіть нижче\nБудь ласка {choice.inline_keyboard[1][0].callback_data.split(":")[-1]} в такому ж форматі',
                    reply_markup=Admin_back_to_choosing_roses,
                )
                await ChangeBouquetPrice.change_bouquet_price.set()


@dp.message_handler(user_id=ADMIN_ID, state=ChangeBouquetPrice.change_bouquet_price)
async def show_bouquet_cost(message: Message, state: FSMContext) -> None:
    if message.text == "⬅ Назад":
        await message.answer(
            "Ціну якої квіткової композиції ви юажаєте змінити?",
            reply_markup=Admin_change_cost,
        )
        await state.finish()
    else:
        try:
            change_price = message.text
            async with state.proxy() as data:
                pressed = data["which_item"]
                for choice_eng in how_much_choise_eng:
                    if (
                        choice_eng.inline_keyboard[1][0].callback_data.split(":")[-3]
                        == pressed + " roses"
                    ):
                        callback_bouquet_ukr = choice_eng.inline_keyboard[1][
                            0
                        ].callback_data
                        choice_eng.inline_keyboard[1][0].callback_data = ":".join(
                            callback_bouquet_ukr.split(":")[:-1] + [change_price]
                        )
                for choice in how_much_choise:
                    if (
                        choice.inline_keyboard[1][0].callback_data.split(":")[-3]
                        == pressed
                    ):
                        callback_bouquet = choice.inline_keyboard[1][0].callback_data
                        choice.inline_keyboard[1][0].callback_data = ":".join(
                            callback_bouquet.split(":")[:-1] + [change_price]
                        )
                        await message.reply(
                            f'Ціну букета змінено успішно !!!\nЗмінено ціну на: {choice.inline_keyboard[1][0].callback_data.split(":")[-1]}',
                            reply_markup=Admin_bouquet_price,
                        )
            await state.finish()
        except:
            await message.reply(
                "Введено помилку!\nВідформатуйте ціну правильно!!!",
            )


@dp.message_handler(user_id=ADMIN_ID, text="Перевірка клієнтів за день")
async def check_new_customers_day(message: types.Message) -> None:
    day_ago = (datetime.now(ukr_date) - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    request_day_ago = cursor.execute(
        f"SELECT * FROM shopping WHERE order_time >= '{day_ago}' AND is_fulfilled == 'Yes'"
    )
    customers_day_ago = request_day_ago.fetchall()
    num_orders = f"Сьогоднішні замовлення: {len(customers_day_ago)}"
    await message.answer(num_orders)
    for i in range(len(customers_day_ago)):
        df = pd.DataFrame(
            {
                "ID:              ": customers_day_ago[i][0],
                "Час доставки:    ": customers_day_ago[i][11],
                "Тип букета:      ": f"{customers_day_ago[i][4]} троянд"
                if customers_day_ago[i][4] != "Коробка"
                else customers_day_ago[i][4],
                "Скільки штук:    ": customers_day_ago[i][5],
                "Скільки коштує кожен:  ": customers_day_ago[i][6],
                "Напис на букеті: ": "Немає"
                if customers_day_ago[i][7] == "Without inscription"
                else customers_day_ago[i][7],
                "Ім'я:            ": customers_day_ago[i][2],
                "Номер телефону:  ": customers_day_ago[i][9],
                "Адреса:          ": customers_day_ago[i][12],
            },
            index=[0],
        ).transpose()
        df.columns = [" "]
        await message.answer(df)


@dp.message_handler(user_id=ADMIN_ID, text="Перевірка клієнтів за три дні")
async def check_orders_three_days(message: types.Message) -> None:
    day_ago = (datetime.now(ukr_date) - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
    request_three_days_ago = cursor.execute(
        f"SELECT * FROM shopping WHERE order_time >= '{day_ago}' AND is_fulfilled == 'Yes'"
    )
    three_days_ago = request_three_days_ago.fetchall()
    num_orders = f"Кількість замовлень за останні 3 дні: {len(three_days_ago)}"
    await message.answer(num_orders)
    for i in range(len(three_days_ago)):
        df = pd.DataFrame(
            {
                "ID:              ": three_days_ago[i][0],
                "Час доставки:    ": three_days_ago[i][11],
                "Тип букета:      ": f"{three_days_ago[i][4]} троянд"
                if three_days_ago[i][4] != "Коробка"
                else three_days_ago[i][4],
                "Скільки штук:    ": three_days_ago[i][5],
                "Скільки коштує кожен:  ": three_days_ago[i][6],
                "Напис на букеті: ": "Немає"
                if three_days_ago[i][7] == "Without inscription"
                else three_days_ago[i][7],
                "Ім'я:            ": three_days_ago[i][2],
                "Номер телефону:  ": three_days_ago[i][9],
                "Адреса:          ": three_days_ago[i][12],
            },
            index=[0],
        ).transpose()
        df.columns = [" "]
        await message.answer(df)


@dp.message_handler(user_id=ADMIN_ID, text="Перевірка замовлень за останню годину")
async def check_orders_last_hour(message: types.Message) -> None:
    one_hour = (datetime.now(ukr_date) - timedelta(hours=1)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    request_day_ago = cursor.execute(
        f"SELECT * FROM shopping WHERE order_time >= '{one_hour}' AND is_fulfilled == 'Yes'"
    )
    one_hour_ago = request_day_ago.fetchall()
    num_orders = f"Кількість замовлень за останню годину: {len(one_hour_ago)}"
    await message.answer(num_orders)
    for i in range(len(one_hour_ago)):
        df = pd.DataFrame(
            {
                "ID:              ": one_hour_ago[i][0],
                "Час доставки:    ": one_hour_ago[i][11],
                "Тип букета:      ": f"{one_hour_ago[i][4]} троянд"
                if one_hour_ago[i][4] != "Коробка"
                else one_hour_ago[i][4],
                "Скільки штук:    ": one_hour_ago[i][5],
                "Скільки коштує кожен:  ": one_hour_ago[i][6],
                "Напис на букеті: ": "Немає"
                if one_hour_ago[i][7] == "Without inscription"
                else one_hour_ago[i][7],
                "Ім'я:            ": one_hour_ago[i][2],
                "Номер телефону:  ": one_hour_ago[i][9],
                "Адреса:          ": one_hour_ago[i][12],
            },
            index=[0],
        ).transpose()
        df.columns = [" "]
        await message.answer(df)


@dp.message_handler(user_id=ADMIN_ID, text="Перевірка останніх 10 замовлень")
async def check_last_ten_orders(message: types.Message) -> None:
    request_ten_orders = cursor.execute(
        "SELECT * FROM shopping WHERE is_fulfilled == 'Yes' ORDER BY order_time DESC LIMIT 10"
    )
    last_ten_orders = request_ten_orders.fetchall()
    num_orders = f"{len(last_ten_orders)} останніх замовлень:"
    await message.answer(num_orders)
    for i in range(len(last_ten_orders)):
        df = pd.DataFrame(
            {
                "ID:              ": last_ten_orders[i][0],
                "Час доставки:    ": last_ten_orders[i][11],
                "Тип букета:      ": f"{last_ten_orders[i][4]} троянд"
                if last_ten_orders[i][4] != "Коробка"
                else last_ten_orders[i][4],
                "Скільки штук:    ": last_ten_orders[i][5],
                "Скільки коштує кожен:  ": last_ten_orders[i][6],
                "Напис на букеті: ": "Немає"
                if last_ten_orders[i][7] == "Without inscription"
                else last_ten_orders[i][7],
                "Ім'я:            ": last_ten_orders[i][2],
                "Номер телефону:  ": last_ten_orders[i][9],
                "Адреса:          ": last_ten_orders[i][12],
            },
            index=[0],
        ).transpose()
        df.columns = [" "]
        await message.answer(df)


@dp.message_handler(user_id=ADMIN_ID, text="📢 Надіслати оголошення")
async def add_advertisement(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Залиште пост нижче і напишіть під ним текст для оголошення",
        reply_markup=Admin_post_advertisement,
    )
    await Advertisement.advertisement.set()


@dp.message_handler(
    user_id=ADMIN_ID,
    content_types=types.ContentType.PHOTO,
    state=Advertisement.advertisement,
)
async def post(message: Message, state: FSMContext) -> None:
    text_for_photo = message.caption
    if message.content_type == types.ContentType.PHOTO:
        cursor.execute("SELECT user_id FROM translates_from_id")
        all_users = [*set(cursor.fetchall())]
        for user_id in all_users:
            if user_id[0] != str(ADMIN_ID):
                try:
                    photo_file_id = message.photo[-1].file_id
                    await bot.send_photo(
                        photo=photo_file_id, chat_id=user_id[0], caption=text_for_photo
                    )
                except:
                    pass
            else:
                pass
        await message.answer(
            "💬 Ваше оголошення успішно опубліковано", reply_markup=Admin_panel_buttons
        )
        await state.finish()
    else:
        await message.answer("Сталася помилка під час надсилання, спробуйте ще раз")


@dp.message_handler(user_id=ADMIN_ID, text="⬅ Назад", state=Advertisement.advertisement)
async def back_from_advertisement(message: Message, state: FSMContext) -> None:
    await message.reply(
        "Вітаємо в панелі адміністратора", reply_markup=Admin_panel_buttons
    )
    await state.finish()


@dp.message_handler(user_id=ADMIN_ID, text="🖼️ Змінити зображення")
async def change_img(message: Message) -> None:
    await message.answer(
        text="Виберіть, яке зображення потрібно змінити:",
        reply_markup=Admin_bouquet_photo,
    )


async def show_pictures(message: Message, state: FSMContext) -> None:
    if message.text == "⬅ Повернутися до меню":
        await message.answer("Виберіть одну нижче", reply_markup=Admin_panel_buttons)
        await state.finish()
    else:
        file_path = (
            message.text.split()[0] + "units"
            if "Box" not in message.text
            else "Kоробкa"
        )
        with open(f"imgs/{file_path}.jpg", "rb") as img:
            await bot.send_photo(
                chat_id=ADMIN_ID,
                photo=img,
                caption="Перетягніть зображення, яке потрібно змінити",
                reply_markup=Admin_back_to_choosing_roses,
            )
            async with state.proxy() as data:
                data["file_path"] = f"imgs/{file_path}.jpg"
        await ChangePicture.change_picture.set()


async def replace_image(old_image: str, new_image: str) -> None:
    os.remove(old_image)
    with Image.open(new_image) as new_img:
        new_img.save(old_image)


@dp.message_handler(
    user_id=ADMIN_ID,
    content_types=ContentTypes.PHOTO,
    state=ChangePicture.change_picture,
)
async def change_only_pic(message: Message, state: FSMContext) -> None:
    photo_file_id = message.photo[-1].file_id
    file_path = await bot.download_file_by_id(photo_file_id)
    async with state.proxy() as data:
        await replace_image(data["file_path"], file_path)
    await message.answer("Змінено успішно! 👍", reply_markup=Admin_panel_buttons)
    await state.finish()


@dp.message_handler(
    user_id=ADMIN_ID, text="⬅ Назад", state=ChangePicture.change_picture
)
async def back_only_picture(message: Message, state: FSMContext) -> None:
    await message.answer("Виберіть одну нижче", reply_markup=Admin_bouquet_photo)
    await state.finish()


@dp.message_handler(user_id=ADMIN_ID, text="✍️ Переглянути коментарі")
async def check_comments(message: Message) -> None:
    await message.reply(
        "Виберіть, які саме коментарі ви хочете переглянути:",
        reply_markup=Admin_check_comments,
    )


@dp.message_handler(user_id=ADMIN_ID, text="Переглянути коментарі за 1 тиждень")
async def check_one_week_comments(message: Message) -> None:
    request_one_week = datetime.now(ukr_date) - timedelta(days=7)
    request_week_ago = cursor.execute(
        f"SELECT * FROM comment WHERE text_time >= '{request_one_week}'"
    )
    request_week_data = request_week_ago.fetchall()

    if not request_week_data:
        await message.answer("Немає коментарів за останній тиждень.")
        return

    sorted_week_data = sorted(request_week_data, key=lambda x: x[0])
    for entry in sorted_week_data:
        df_for_week_comments = pd.DataFrame(
            {
                "ID: ": entry[0],
                "User_id: ": entry[1],
                "Comment writing time: ": entry[3],
                "Comment:": entry[2],
            },
            index=[0],
        ).transpose()
        df_for_week_comments.columns = [" "]

        await message.answer(df_for_week_comments.to_string())


@dp.message_handler(user_id=ADMIN_ID, text="Переглянути коментарі за 1 день")
async def check_one_day_comments(message: Message) -> None:
    one_day = datetime.now(ukr_date) - timedelta(days=1)
    request_one_day = cursor.execute(
        f"SELECT * FROM comment WHERE text_time >= '{one_day}'"
    )
    comments = request_one_day.fetchall()

    if not comments:
        await message.answer("Немає коментарів за останній день.")
        return

    sorted_one_data = sorted(comments, key=lambda x: x[0])
    for entry in sorted_one_data:
        df_for_day_comments = pd.DataFrame(
            {
                "ID: ": entry[0],
                "User_id: ": entry[1],
                "Comment writing time: ": entry[3],
                "Comment:": entry[2],
            },
            index=[0],
        ).transpose()
        df_for_day_comments.columns = [" "]

        await message.answer(df_for_day_comments.to_string())


register_handlers(Admin_bouquet_price, change_bouquet_cost)
register_handlers(Admin_bouquet_photo, show_pictures)
