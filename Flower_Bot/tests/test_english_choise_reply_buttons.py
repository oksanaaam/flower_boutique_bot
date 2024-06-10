import unittest
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.reply.english_choise_reply_buttons import (
    Start_eng,
    Location_eng,
    Menu_eng,
    Box_eng,
    Bouquet_eng,
    Order_eng,
    Later_delivery_time_eng,
    Immediately_delivery_time_eng,
    Cancel_eng,
    Contact_eng,
    Each_eng,
    Confirmation_location_eng,
    Confirmation_style_eng,
    Back_to_location_yes_eng,
    Settings_eng,
    change_language_eng,
    last_agree_eng,
)


class TestEnglishChoiceReplyButtons(unittest.TestCase):
    def test_start_eng(self):
        self.assertIsInstance(Start_eng, ReplyKeyboardMarkup)
        buttons = [button.text for row in Start_eng.keyboard for button in row]
        self.assertIn("🌹 Menu", buttons)
        self.assertIn("📥 Basket", buttons)
        self.assertIn("✍️ Comment", buttons)
        self.assertIn("⚙️ Settings", buttons)

    def test_location_eng(self):
        self.assertIsInstance(Location_eng, ReplyKeyboardMarkup)
        buttons = [button.text for row in Location_eng.keyboard for button in row]
        self.assertIn("⬅ Back to set time", buttons)

    def test_menu_eng(self):
        self.assertIsInstance(Menu_eng, ReplyKeyboardMarkup)
        buttons = [button.text for row in Menu_eng.keyboard for button in row]
        self.assertIn("🥡 Flowers in a box", buttons)
        self.assertIn("💐 Flowers in a bouquet", buttons)
        self.assertIn("📥 Basket", buttons)
        self.assertIn("⬅ Back", buttons)

    def test_box_eng(self):
        self.assertIsInstance(Box_eng, ReplyKeyboardMarkup)
        buttons = [button.text for row in Box_eng.keyboard for button in row]
        self.assertIn("📥 Basket", buttons)
        self.assertIn("⬅ Back to menu", buttons)

    def test_bouquet_eng(self):
        self.assertIsInstance(Bouquet_eng, ReplyKeyboardMarkup)
        buttons = [button.text for row in Bouquet_eng.keyboard for button in row]
        self.assertIn("101 roses", buttons)
        self.assertIn("201 roses", buttons)
        self.assertIn("📥 Basket", buttons)
        self.assertIn("⬅ Back to menu", buttons)

    def test_order_eng(self):
        self.assertIsInstance(Order_eng, ReplyKeyboardMarkup)
        buttons = [button.text for row in Order_eng.keyboard for button in row]
        self.assertIn("📭 Immediately delivery", buttons)
        self.assertIn("⏱ Set delivery time", buttons)
        self.assertIn("⬅ Back to menu", buttons)

    def test_immediately_delivery_time_eng(self):
        self.assertIsInstance(Immediately_delivery_time_eng, ReplyKeyboardMarkup)
        buttons = [
            button.text
            for row in Immediately_delivery_time_eng.keyboard
            for button in row
        ]
        self.assertIn("📲 Contact number", buttons)
        self.assertIn("⬅ Back", buttons)

    def test_cancel_eng(self):
        self.assertIsInstance(Cancel_eng, ReplyKeyboardMarkup)
        buttons = [button.text for row in Cancel_eng.keyboard for button in row]
        self.assertIn("⬅ Back", buttons)

    def test_contact_eng(self):
        self.assertIsInstance(Contact_eng, ReplyKeyboardMarkup)
        buttons = [button.text for row in Contact_eng.keyboard for button in row]
        self.assertIn("📲 Contact number", buttons)
        self.assertIn("⬅ Back to location address", buttons)

    def test_each_eng(self):
        self.assertIsInstance(Each_eng, ReplyKeyboardMarkup)
        buttons = [button.text for row in Each_eng.keyboard for button in row]
        self.assertIn("📥 Basket", buttons)
        self.assertIn("⬅ Back to bouquets", buttons)

    def test_confirmation_location_eng(self):
        self.assertIsInstance(Confirmation_location_eng, ReplyKeyboardMarkup)
        buttons = [
            button.text for row in Confirmation_location_eng.keyboard for button in row
        ]
        self.assertIn("✅ Yes", buttons)
        self.assertIn("❌ No", buttons)
        self.assertIn("⬅ Back", buttons)

    def test_confirmation_style_eng(self):
        self.assertIsInstance(Confirmation_style_eng, ReplyKeyboardMarkup)
        buttons = [
            button.text for row in Confirmation_style_eng.keyboard for button in row
        ]
        self.assertIn("✅ Yes", buttons)
        self.assertIn("❌ No", buttons)

    def test_back_to_location_yes_eng(self):
        self.assertIsInstance(Back_to_location_yes_eng, ReplyKeyboardMarkup)
        buttons = [
            button.text for row in Back_to_location_yes_eng.keyboard for button in row
        ]
        self.assertIn("⬅ Back", buttons)

    def test_settings_eng(self):
        self.assertIsInstance(Settings_eng, ReplyKeyboardMarkup)
        buttons = []
        for row in Settings_eng.keyboard:
            for item in row:
                if isinstance(item, KeyboardButton):
                    buttons.append(item.text)
                else:
                    buttons.append(item)
        self.assertIn("Change the language", buttons)
        self.assertIn("⬅ Back", buttons)

    def test_change_language_eng(self):
        self.assertIsInstance(change_language_eng, ReplyKeyboardMarkup)
        buttons = [
            button.text for row in change_language_eng.keyboard for button in row
        ]
        self.assertIn("🇺🇸 English", buttons)
        self.assertIn("🇺🇦 Українська", buttons)
        self.assertIn("⬅ Back", buttons)

    def test_last_agree_eng(self):
        self.assertIsInstance(last_agree_eng, ReplyKeyboardMarkup)
        buttons = [button.text for row in last_agree_eng.keyboard for button in row]
        self.assertIn("✅ Yes", buttons)
        self.assertIn("❌ No", buttons)
