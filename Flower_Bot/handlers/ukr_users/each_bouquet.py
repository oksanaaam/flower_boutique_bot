from typing import Any

from keyboards.inline.choice_inline_buttons import how_much_choise
from keyboards.reply.choise_reply_buttons import Each, Menu
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
import sqlite3


def get_data(data: list[tuple[Any, Any, Any]]) -> tuple[pd.DataFrame, str, str, str]:
    # df = pd.DataFrame(data, columns=["nechta", "bouquet", "narxi"])["скільки", "букет", "ціна"])
    df = pd.DataFrame(data, columns=["amount", "bouquet", "price"])
    df["price"] = [int("".join(i.split("."))) for i in df["price"]]
    df = df.sort_values(by="price", ascending=False)
    df["price"] = df["amount"] * df["price"]
    group = df.groupby("bouquet").sum()
    group.insert(1, "bouquet_name", group.index.values)
    total_price = group["price"].sum()
    group["price"] = group["price"].astype(str)
    group["price"] = [
        i[:-6] + "." + i[-6:-3] + "." + i[-3:] if i[:-6] else i[:-3] + "." + i[-3:]
        for i in group["price"]
    ]
    group["amount"] = [
        number_to_emoji(group["amount"][i]) for i in range(len(group["amount"]))
    ]
    group.insert(1, "X", ["✖️" for i in range(len(group))])
    group.insert(3, "дорівнює", ["🟰" for i in range(len(group))])
    tariff = "0.100 grn"
    total_temp = str(total_price + 100)
    total = (
        total_temp[:-6] + "." + total_temp[-6:-3] + "." + total_temp[-3:]
        if total_temp[:-6] != ""
        else total_temp[-6:-3] + "." + total_temp[-3:]
    )
    total_price = (
        str(total_price)[:-6]
        + "."
        + str(total_price)[-6:-3]
        + "."
        + str(total_price)[-3:]
        if str(total_price)[:-6] != ""
        else str(total_price)[-6:-3] + "." + str(total_price)[-3:]
    )
    return group, total_price, tariff, total


def number_to_emoji(number: str) -> str:
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


@dp.message_handler(text=["📥 Корзина"])
async def check_basket(message: types.Message) -> None:
    conn1 = sqlite3.connect("flower.db")
    cursor1 = conn1.cursor()
    cursor1.execute(
        "SELECT bouquet FROM shopping WHERE user_id=? AND is_fulfilled=?",
        (message.chat.id, "No"),
    )
    set_select = set([i[0] for i in cursor1.fetchall()])
    print("set_select in basket", set_select)
    key = [
        types.InlineKeyboardButton(text="❌" + i, callback_data="del{}".format(i))
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
    conn = sqlite3.connect("flower.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT how_many, bouquet, how_much_it FROM shopping WHERE is_fulfilled = ? and user_id = ?",
        ("No", message.chat.id),
    )
    query = cursor.fetchall()
    # print("query", query)
    if query:
        group, total_price, tariff, total = get_data(query)
        # print("total", total, "total_price", total_price, "tariff", tariff, "group", group)

        await message.answer(
            f"📥 В корзині:\n{group.to_string(index=False, header=False)}\nТовар: {str(total_price)} grn\nДоставка: {tariff}\nВсього: {total} grn",
            reply_markup=new_but,
        )
    else:
        await message.reply("📥 Ваша корзина порожня")


button_labels = [
    "101",
    "201",
    "301",
    "401",
    "501",
    "601",
    "701",
    "1001",
    "⬅ Повернутись до меню",
]


async def button_handler(message: types.Message, state: FSMContext) -> None:
    if message.text == "⬅ Повернутись до меню":
        await message.answer("Виберіть одне з наступного:", reply_markup=Menu)
    else:
        button_label = message.text
        await message.answer("Виберіть кількість букетів:", reply_markup=Each)

        sp = button_label.split()[0]
        for i in how_much_choise:
            if i.inline_keyboard[1][0].callback_data.split(":")[2].split()[0] == sp:
                with open(f"imgs/{sp}units.jpg", "rb") as photo_:
                    await bot.send_photo(
                        message.chat.id,
                        photo=photo_,
                        caption=f'Букет на вибір: {sp} троянд.\nЦіна: {i.inline_keyboard[1][0].callback_data.split(":")[-1]} grn',
                        reply_markup=i,
                    )


for label in button_labels:
    dp.register_message_handler(button_handler, Text(label))
