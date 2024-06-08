from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import basket_callback, Delivery
from keyboards.inline.english_choise_inline_buttons import (
    to_box_eng,
    how_much_choise_eng,
    confirmation_eng,
)

# For Box inline_buttons
to_box = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="-",
                callback_data=basket_callback.new(item_name="minus", how_much=0),
            ),
            InlineKeyboardButton(
                text="1", callback_data=basket_callback.new(item_name="sum", how_much=1)
            ),
            InlineKeyboardButton(
                text="+",
                callback_data=basket_callback.new(item_name="plus", how_much=0),
            ),
        ],
        [
            InlineKeyboardButton(
                text="📥 Додати до замовлення",
                callback_data=Delivery.new(
                    item_name="Delivery",
                    which_item="Коробка",
                    how_many=1,
                    how_much_it="5.000",
                ),
            )
        ],
    ],
    row_width=3,
)

# for each bouquet inline_buttons
how_much_choise = []
button_labels = ["101", "201", "301", "401", "501", "601", "701", "1001"]
selling_rate = [
    "180.000",
    "280.000",
    "380.000",
    "500.000",
    "600.000",
    "700.000",
    "900.000",
    "1800.000",
]
all_zip_data = dict(zip(button_labels, selling_rate))
for i in all_zip_data:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="-",
                    callback_data=basket_callback.new(item_name="minus", how_much=0),
                ),
                InlineKeyboardButton(
                    text="1",
                    callback_data=basket_callback.new(item_name="sum", how_much=1),
                ),
                InlineKeyboardButton(
                    text="+",
                    callback_data=basket_callback.new(item_name="plus", how_much=0),
                ),
            ]
        ],
        row_width=3,
    )
    keyboard.add(
        InlineKeyboardButton(
            text="📥 Додати до замовлення",
            callback_data=Delivery.new(
                item_name="Delivery",
                which_item=i,
                how_many=1,
                how_much_it=all_zip_data[i],
            ),
        )
    )
    how_much_choise.append(keyboard)

confirmation = InlineKeyboardMarkup()
confirmation.add(
    InlineKeyboardButton(text="✅ Підтвердити", callback_data="confirm"),
    InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel"),
)

inline_keyboards = {
    "ukr": {
        "to_box": to_box,
        "how_much_choise": how_much_choise,
        "confirmation": confirmation,
    },
    "eng": {
        "to_box": to_box_eng,
        "how_much_choise": how_much_choise_eng,
        "confirmation": confirmation_eng,
    },
}
