from aiogram.utils.callback_data import CallbackData

basket_callback = CallbackData("basket", "item_name", "how_much")
button_callback = CallbackData("button", "time")
Delivery = CallbackData(
    "to_basket", "item_name", "which_item", "how_many", "how_much_it"
)
