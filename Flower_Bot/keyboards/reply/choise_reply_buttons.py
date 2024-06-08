from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.reply.english_choise_reply_buttons import (
    change_language_eng,
    last_agree_eng,
    Back_to_location_yes_eng,
    Box_eng,
    Bouquet_eng,
    Cancel_eng,
    Confirmation_location_eng,
    Confirmation_style_eng,
    Contact_eng,
    Each_eng,
    Immediately_delivery_time_eng,
    Later_delivery_time_eng,
    Location_eng,
    Menu_eng,
    Order_eng,
    Settings_eng,
    Start_eng,
)


# start keyboards, ukr
Start: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Tmp_Menu: KeyboardButton = KeyboardButton("🌹 Меню")
Basket: KeyboardButton = KeyboardButton("📥 Корзина")
Tmp_Location: KeyboardButton = KeyboardButton("✍️ Залишити коментар")
Tmp_Settings: KeyboardButton = KeyboardButton("⚙️ Налаштування")
Start.add(Tmp_Menu).add(Basket).add(Tmp_Location).insert(Tmp_Settings)

# location part
Location: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Location.add(KeyboardButton(text="⬅ Назад до встановлення часу"))


# Menu Keyboards
Menu: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Box: KeyboardButton = KeyboardButton("🥡 Квіти в боксі")
Bouquet: KeyboardButton = KeyboardButton("💐 Квіти в букеті")
Basket = KeyboardButton("📥 Корзина")
Back_to_Menu: KeyboardButton = KeyboardButton("⬅ Назад")
Menu.add(Box).insert(Bouquet).add(Basket).add(Back_to_Menu)

# Box Keyboards
Box = ReplyKeyboardMarkup(resize_keyboard=True)
Back_to_Box: KeyboardButton = KeyboardButton("⬅ Повернутись до меню")
Check_basket_2: KeyboardButton = KeyboardButton("📥 Корзина")
Box.add(Check_basket_2).add(Back_to_Box)

# Bouquet keyboards
Bouquet = ReplyKeyboardMarkup(
    [
        [KeyboardButton("101"), KeyboardButton("201")],
        [KeyboardButton("301"), KeyboardButton("401")],
        [KeyboardButton("501"), KeyboardButton("601")],
        [KeyboardButton("701"), KeyboardButton("1001")],
        [KeyboardButton("📥 Корзина")],
        [KeyboardButton("⬅ Повернутись до меню")],
    ],
    resize_keyboard=True,
)

# Order keyboards
Order: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Immediately: KeyboardButton = KeyboardButton("📭 Якнайшвидша доставка")
Set_time: KeyboardButton = KeyboardButton("⏱ Обрати час доставки")
Back_to_orders: KeyboardButton = KeyboardButton("⬅ Повернутись до меню")
Order.add(Immediately).insert(Set_time).add(Back_to_orders)


# delivery keyboards
Later_delivery_time: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Immediately_delivery_time: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    resize_keyboard=True
)
Back_to_delivery_time_choice: KeyboardButton = KeyboardButton("⬅ Назад")
Immediately_delivery_time.add(
    KeyboardButton(text="📲 Номер телефону", request_contact=True)
).add(Back_to_delivery_time_choice)
Cancel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text="⬅ Назад")
)
Contact: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Contact.add(KeyboardButton(text="📲 Номер телефону", request_contact=True)).add(
    KeyboardButton(text="⬅ Назад до локації")
)

# Each bouquet keyboards
Each: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Check_basket: KeyboardButton = KeyboardButton("📥 Корзина")
Back_to_bouquet: KeyboardButton = KeyboardButton("⬅ Повернутись до букетів")
Each.add(Check_basket).add(Back_to_bouquet)

# location's yes and no
Confirmation_location = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Так"), KeyboardButton(text="❌ Ні")],
        [KeyboardButton(text="⬅ Назад")],
    ],
    resize_keyboard=True,
)

# yes or no for style_write
Confirmation_style: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Confirmation_style.add(KeyboardButton(text="✅ Так"), KeyboardButton(text="❌ Ні"))

# location's yes of Back
Back_to_location_yes: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Back_to_location_yes.add(KeyboardButton(text="⬅ Назад"))

# buttons used when admin panel is opening
Admin_panel_buttons: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Admin_panel_buttons.add(
    KeyboardButton(text="🆕 Нові клієнти"), KeyboardButton(text="📢 Надіслати оголошення")
).add(
    KeyboardButton(text="💸 Змінити ціну"), KeyboardButton(text="🖼️ Змінити зображення")
).add(
    KeyboardButton(text="✍️ Переглянути коментарі")
)

# buttons used when admin wants to post advertisement
Admin_post_advertisement = ReplyKeyboardMarkup(resize_keyboard=True)
Admin_post_advertisement.add(KeyboardButton(text="⬅ Назад"))

# buttons used when admin changing cost
Admin_change_cost: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Admin_change_cost.add(
    KeyboardButton(text="🥡 Вартість коробки"), KeyboardButton("💐 Вартість букета")
).add(KeyboardButton(text="⬅ Повернутися до меню"))

# buttons used when admin wants to go back
Admin_back_to_choosing_roses: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    resize_keyboard=True
).add(KeyboardButton(text="⬅ Назад"))

# buttons used when admin wants to check new users and orders
Admin_orders_markup = ReplyKeyboardMarkup(resize_keyboard=True)
Admin_orders_markup.add(KeyboardButton(text="Перевірка клієнтів за день"))
Admin_orders_markup.add(KeyboardButton(text="Перевірка замовлень за останню годину"))
Admin_orders_markup.add(KeyboardButton(text="Перевірка клієнтів за три дні"))
Admin_orders_markup.add(KeyboardButton(text="Перевірка останніх 10 замовлень")).add(
    KeyboardButton(text="⬅ Повернутися до меню")
)

# buttons used when admin wants to check comments
Admin_check_comments = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Переглянути коментарі за 1 тиждень"),
            KeyboardButton(text="Переглянути коментарі за 1 день"),
        ],
        [KeyboardButton(text="⬅ Повернутися до меню")],
    ],
    resize_keyboard=True,
)

# buttons used when admin wants to change price of bouquets
Admin_bouquet_price: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    [
        [KeyboardButton("101 flowers"), KeyboardButton("201 flowers")],
        [KeyboardButton("301 flowers"), KeyboardButton("401 flowers")],
        [KeyboardButton("501 flowers"), KeyboardButton("601 flowers")],
        [KeyboardButton("701 flowers"), KeyboardButton("1001 flowers")],
        [KeyboardButton("⬅ Повернутись до квітів")],
    ],
    resize_keyboard=True,
)

# buttons used when admin wants to change photo of flowers
Admin_bouquet_photo: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    [
        [KeyboardButton("101 ros"), KeyboardButton("201 ros")],
        [KeyboardButton("301 ros"), KeyboardButton("401 ros")],
        [KeyboardButton("501 ros"), KeyboardButton("601 ros")],
        [KeyboardButton("701 ros"), KeyboardButton("1001 ros")],
        [KeyboardButton("Box photo")],
        [KeyboardButton("⬅ Повернутися до меню")],
    ],
    resize_keyboard=True,
)

Settings = ReplyKeyboardMarkup(resize_keyboard=True)
Settings.add("Змінити мову")
Settings.add("⬅ Назад")

change_language = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇸 English"), KeyboardButton(text="🇺🇦 Українська")],
        [KeyboardButton(text="⬅ Назад")],
    ],
    resize_keyboard=True,
)

change_language_begin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇸 English"), KeyboardButton(text="🇺🇦 Українська")]
    ],
    resize_keyboard=True,
)

last_agree = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="✅ Так"), KeyboardButton(text="❌ Ні")]],
    resize_keyboard=True,
)

keyboards_reply: dict[str, dict[str, ReplyKeyboardMarkup]] = {
    "ukr": {
        "start": Start,
        "location": Location,
        "Menu": Menu,
        "Box": Box,
        "Bouquet": Bouquet,
        "Order": Order,
        "Later": Later_delivery_time,
        "Now": Immediately_delivery_time,
        "cancel": Cancel,
        "Contact": Contact,
        "Each": Each,
        "Confirmation_location": Confirmation_location,
        "yes_or_no": Confirmation_style,
        "Back_to_Yes": Back_to_location_yes,
        "Admin_panel_buttons": Admin_panel_buttons,
        "Admin_post_advertisement": Admin_post_advertisement,
        "Admin_back_to_choosing_roses": Admin_back_to_choosing_roses,
        "Admin_change_cost": Admin_change_cost,
        "Admin_orders_markup": Admin_orders_markup,
        "settings": Settings,
        "change_language": change_language,
        "last_agree": last_agree,
        "change_language_begin": change_language_begin,
    },
    "eng": {
        "start": Start_eng,
        "location": Location_eng,
        "Menu": Menu_eng,
        "Box": Box_eng,
        "Bouquet": Bouquet_eng,
        "Order": Order_eng,
        "Later": Later_delivery_time_eng,
        "Now": Immediately_delivery_time_eng,
        "cancel": Cancel_eng,
        "Contact": Contact_eng,
        "Each": Each_eng,
        "Confirmation_location": Confirmation_location_eng,
        "yes_or_no": Confirmation_style_eng,
        "Back_to_Yes": Back_to_location_yes_eng,
        "settings": Settings_eng,
        "change_language": change_language_eng,
        "last_agree": last_agree_eng,
        "change_language_begin": change_language_begin,
    },
}
