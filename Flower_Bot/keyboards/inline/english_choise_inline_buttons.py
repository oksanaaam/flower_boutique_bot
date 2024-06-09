from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import basket_callback, Delivery

# For Box inline_buttons
to_box_eng = InlineKeyboardMarkup(
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
                text="📥 Add to cart",
                callback_data=Delivery.new(
                    item_name="Delivery",
                    which_item="Box",
                    how_many=1,
                    how_much_it="5.000",
                ),
            )
        ],
    ],
    row_width=3,
)

# for each bouquet inline_buttons
how_much_choise_eng = []
button_labels_eng = [
    "101 roses",
    "201 roses",
    "301 roses",
    "401 roses",
    "501 roses",
    "601 roses",
    "701 roses",
    "1001 roses",
]
selling_rate_eng = [
    "3.000",
    "6.000",
    "10.000",
    "14.000",
    "19.000",
    "26.000",
    "31.000",
    "40.000",
]
all_zip_data_eng = dict(zip(button_labels_eng, selling_rate_eng))
for i in all_zip_data_eng:
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
            text="📥 Add to cart",
            callback_data=Delivery.new(
                item_name="Delivery",
                which_item=i,
                how_many=1,
                how_much_it=all_zip_data_eng[i],
            ),
        )
    )
    how_much_choise_eng.append(keyboard)

confirmation_eng = InlineKeyboardMarkup()
confirmation_eng.add(
    InlineKeyboardButton(text="✅ Confirm", callback_data="confirm"),
    InlineKeyboardButton(text="❌ Cancel", callback_data="cancel"),
)
