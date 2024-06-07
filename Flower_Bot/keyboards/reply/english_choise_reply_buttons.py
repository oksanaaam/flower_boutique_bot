from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# start keyboards, eng
Start_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Menu_eng: KeyboardButton = KeyboardButton("🌹 Menu")
Basket: KeyboardButton = KeyboardButton("📥 Basket")
Tmp_Location_eng: KeyboardButton = KeyboardButton("✍️ Comment")
Settings_eng: KeyboardButton = KeyboardButton("⚙️ Settings")
Start_eng.add(Menu_eng).add(Basket).add(Tmp_Location_eng).insert(Settings_eng)

# location part
Location_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Location_eng.add(KeyboardButton(text="⬅ Back to set time"))

# Menu Keyboards
Menu_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Box_eng: KeyboardButton = KeyboardButton("🥡 Flowers in a box")
Bouquet_eng: KeyboardButton = KeyboardButton("💐 Flowers in a bouquet")
Basket: KeyboardButton = KeyboardButton("📥 Basket")
Back_to_Menu_eng: KeyboardButton = KeyboardButton("⬅ Back")
Menu_eng.add(Box_eng).insert(Bouquet_eng).add(Basket).add(Back_to_Menu_eng)

# Box Keyboards
Box_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Back_to_Box_eng: KeyboardButton = KeyboardButton("⬅ Back to menu")
Check_basket_2_eng: KeyboardButton = KeyboardButton("📥 Basket")
Box_eng.add(Check_basket_2_eng).add(Back_to_Box_eng)

# Bouquet keyboards
Bouquet_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    [
        [KeyboardButton("101 roses"), KeyboardButton("201 roses")],
        [KeyboardButton("301 roses"), KeyboardButton("401 roses")],
        [KeyboardButton("501 roses"), KeyboardButton("601 roses")],
        [KeyboardButton("701 roses"), KeyboardButton("1001 roses")],
        [KeyboardButton("📥 Basket")],
        [KeyboardButton("⬅ Back to menu")],
    ],
    resize_keyboard=True,
)

# Order keyboards
Order_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Immediately_eng: KeyboardButton = KeyboardButton("📭 Immediately delivery")
Set_time_eng: KeyboardButton = KeyboardButton("⏱ Set delivery time")
Back_to_orders_eng: KeyboardButton = KeyboardButton("⬅ Back to menu")
Order_eng.add(Immediately_eng).insert(Set_time_eng).add(Back_to_orders_eng)

# delivery keyboards
Later_delivery_time_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Immediately_delivery_time_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Back_to_delivery_time_choice_eng: KeyboardButton = KeyboardButton("⬅ Back")
Immediately_delivery_time_eng.add(KeyboardButton(text="📲 Contact number", request_contact=True)).add(
    Back_to_delivery_time_choice_eng
)
Cancel_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text="⬅ Back")
)
Contact_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Contact_eng.add(KeyboardButton(text="📲 Contact number", request_contact=True)).add(
    KeyboardButton(text="⬅ Back to location address")
)

# Each bouquet keyboards
Each_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Check_basket_eng: KeyboardButton = KeyboardButton("📥 Basket")
Back_to_bouquet_eng: KeyboardButton = KeyboardButton("⬅ Back to bouquets")
Each_eng.add(Check_basket_eng).add(Back_to_bouquet_eng)

# location's yes and no
Confirmation_location_eng = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Yes"), KeyboardButton(text="❌ No")],
        [KeyboardButton(text="⬅ Back")],
    ],
    resize_keyboard=True,
)

# yes or no for style_write
Confirmation_style_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Confirmation_style_eng.add(KeyboardButton(text="✅ Yes"), KeyboardButton(text="❌ No"))

# location's yes of Back
Back_to_location_yes_eng: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Back_to_location_yes_eng.add(KeyboardButton(text="⬅ Back"))

Settings_eng = ReplyKeyboardMarkup(resize_keyboard=True)
Settings_eng.add("Change the language")
Settings_eng.add("⬅ Back")

change_language_eng = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇸 English"), KeyboardButton(text="🇺🇦 Українська")],
        [KeyboardButton(text="⬅ Back")],
    ],
    resize_keyboard=True,
)

last_agree_eng = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="✅ Yes"), KeyboardButton(text="❌ No")]],
    resize_keyboard=True,
)
