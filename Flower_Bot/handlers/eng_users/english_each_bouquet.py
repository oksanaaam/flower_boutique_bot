import sqlite3

import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.english_choise_inline_buttons import how_much_choise_eng
from keyboards.reply.english_choise_reply_buttons import Each_eng, Menu_eng
from loader import bot, dp

db = sqlite3.connect("flower.db")
cursor = db.cursor()


def number_to_emoji(number: int) -> str:
    emoji_digits = [
        "0️⃣",
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣",
    ]
    return "".join(emoji_digits[int(digit)] for digit in str(number))


button_labels = [
    "101 roses",
    "201 roses",
    "301 roses",
    "401 roses",
    "501 roses",
    "601 roses",
    "701 roses",
    "1001 roses",
    "⬅ Back to menu",
]


@dp.message_handler(lambda message: message.text == "📥 Basket")
async def check_basket(message: types.Message) -> None:
    cursor.execute(
        "SELECT how_many, bouquet, how_much_it FROM shopping WHERE is_fulfilled = ? and user_id = ?",
        ("No", message.chat.id),
    )
    query = cursor.fetchall()

    cursor.execute(
        "SELECT bouquet FROM shopping WHERE user_id=? AND is_fulfilled=?",
        (message.chat.id, "No"),
    )
    select = cursor.fetchall()
    set_select = set([entry[0] for entry in select])
    ukr = ["101", "201", "301", "401", "501", "601", "701", "1001", "Коробка"]
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
    new_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚖 Order", callback_data="open_delivery", cache_time=1
                )
            ],
            [
                InlineKeyboardButton(text="⬅ Назад", callback_data="close"),
                InlineKeyboardButton(text="🗑 Empty basket", callback_data="clear_to_"),
            ],
        ]
    ).add(*key)
    if query:
        df = pd.DataFrame(query, columns=["amount", "bouquet", "price"])
        df["bouquet"] = df["bouquet"].str.replace("Коробка", "Box")
        df["price"] = [int("".join(i.split("."))) for i in df["price"]]
        df = df.sort_values(by="price", ascending=True)
        df["price"] = df["amount"] * df["price"]
        group = df.groupby("bouquet").sum()
        group.insert(1, "bouquet_name", group.index.values)
        total_cost = group["price"].sum()
        group["price"] = group["price"].astype(str)
        group["price"] = [
            i[:-6] + "." + i[-6:-3] + "." + i[-3:] if i[:-6] else i[:-3] + "." + i[-3:]
            for i in group["price"]
        ]
        group["amount"] = [
            number_to_emoji(group["amount"][i]) for i in range(len(group["amount"]))
        ]
        group.insert(1, "X", ["✖️" for i in range(len(group))])
        group.insert(3, "sum", ["🟰" for i in range(len(group))])
        tariff = "0.100 grn"  # for delivery
        total_temp = str(total_cost + 100)
        total = (
            total_temp[:-6] + "." + total_temp[-6:-3] + "." + total_temp[-3:]
            if total_temp[:-6] != ""
            else total_temp[-6:-3] + "." + total_temp[-3:]
        )
        total_price = (
            str(total_cost)[:-6]
            + "."
            + str(total_cost)[-6:-3]
            + "."
            + str(total_cost)[-3:]
            if str(total_cost)[:-6] != ""
            else str(total_cost)[-6:-3] + "." + str(total_cost)[-3:]
        )
        await message.answer(
            f"📥 In the basket:\n{group.to_string(index=False, header=False)}\nProduct: {str(total_price)} grn\nDelivery: {tariff}\nTotal: {total} grn",
            reply_markup=new_button,
        )
    else:
        await message.reply("📥 Your basket is empty")


async def button_handler(message: types.Message, state: FSMContext) -> None:
    if message.text == "⬅ Back to menu":
        await message.answer("Select one of the following:", reply_markup=Menu_eng)
    else:
        button_label = message.text
        await message.answer("Choose amount of bouquets:", reply_markup=Each_eng)

        sp = button_label.split()[0]
        for choice_eng in how_much_choise_eng:
            if (
                choice_eng.inline_keyboard[1][0].callback_data.split(":")[2].split()[0]
                == sp
            ):
                with open(f"imgs/{sp}units.jpg", "rb") as photo_:
                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=photo_,
                        caption=f'Bouquet that you selected: {sp} roses\nPrice: {choice_eng.inline_keyboard[1][0].callback_data.split(":")[-1]} grn',
                        reply_markup=choice_eng,
                    )


for label in button_labels:
    dp.register_message_handler(button_handler, Text(label))
