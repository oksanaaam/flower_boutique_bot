import unittest
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.reply.choise_reply_buttons import (
    Start,
    Location,
    Menu,
    Box,
    Bouquet,
    Order,
    Immediately_delivery_time,
    Contact,
    Each,
    Confirmation_location,
    Confirmation_style,
    Admin_panel_buttons,
    Admin_post_advertisement,
    Admin_change_cost,
    Admin_back_to_choosing_roses,
    Admin_orders_markup,
    Admin_check_comments,
    Admin_bouquet_price,
    Admin_bouquet_photo,
    Settings,
    change_language,
    change_language_begin,
    last_agree,
    keyboards_reply,
)


class TestChoiceReplyButtons(unittest.TestCase):
    def test_start_buttons(self):
        buttons = [button.text for row in Start.keyboard for button in row]
        expected_buttons = [
            "🌹 Меню",
            "📥 Корзина",
            "✍️ Залишити коментар",
            "⚙️ Налаштування",
        ]
        self.assertEqual(buttons, expected_buttons)

    def test_location_buttons(self):
        buttons = [button.text for row in Location.keyboard for button in row]
        self.assertIn("⬅ Назад до встановлення часу", buttons)

    def test_menu_buttons(self):
        buttons = [button.text for row in Menu.keyboard for button in row]
        expected_buttons = [
            "🥡 Квіти в боксі",
            "💐 Квіти в букеті",
            "📥 Корзина",
            "⬅ Назад",
        ]
        self.assertEqual(buttons, expected_buttons)

    def test_box_buttons(self):
        buttons = [button.text for row in Box.keyboard for button in row]
        expected_buttons = ["📥 Корзина", "⬅ Повернутись до меню"]
        self.assertEqual(buttons, expected_buttons)

    def test_bouquet_buttons(self):
        buttons = [button.text for row in Bouquet.keyboard for button in row]
        expected_buttons = [
            "101",
            "201",
            "301",
            "401",
            "501",
            "601",
            "701",
            "1001",
            "📥 Корзина",
            "⬅ Повернутись до меню",
        ]
        self.assertEqual(buttons, expected_buttons)

    def test_order_buttons(self):
        buttons = [button.text for row in Order.keyboard for button in row]
        expected_buttons = [
            "📭 Якнайшвидша доставка",
            "⏱ Обрати час доставки",
            "⬅ Повернутись до меню",
        ]
        self.assertEqual(buttons, expected_buttons)

    def test_immediately_delivery_time_buttons(self):
        buttons = [
            button.text for row in Immediately_delivery_time.keyboard for button in row
        ]
        expected_buttons = ["📲 Номер телефону", "⬅ Назад"]
        self.assertEqual(buttons, expected_buttons)

    def test_contact_buttons(self):
        buttons = [button.text for row in Contact.keyboard for button in row]
        expected_buttons = ["📲 Номер телефону", "⬅ Назад до локації"]
        self.assertEqual(buttons, expected_buttons)

    def test_each_buttons(self):
        buttons = [button.text for row in Each.keyboard for button in row]
        expected_buttons = ["📥 Корзина", "⬅ Повернутись до букетів"]
        self.assertEqual(buttons, expected_buttons)

    def test_confirmation_location_buttons(self):
        buttons = [
            button.text for row in Confirmation_location.keyboard for button in row
        ]
        expected_buttons = ["✅ Так", "❌ Ні", "⬅ Назад"]
        self.assertEqual(buttons, expected_buttons)

    def test_confirmation_style_buttons(self):
        buttons = [button.text for row in Confirmation_style.keyboard for button in row]
        expected_buttons = ["✅ Так", "❌ Ні"]
        self.assertEqual(buttons, expected_buttons)

    def test_admin_panel_buttons(self):
        buttons = [
            button.text for row in Admin_panel_buttons.keyboard for button in row
        ]
        expected_buttons = [
            "🆕 Нові клієнти",
            "📢 Надіслати оголошення",
            "💸 Змінити ціну",
            "🖼️ Змінити зображення",
            "✍️ Переглянути коментарі",
        ]
        self.assertEqual(buttons, expected_buttons)

    def test_admin_post_advertisement_buttons(self):
        buttons = [
            button.text for row in Admin_post_advertisement.keyboard for button in row
        ]
        self.assertIn("⬅ Назад", buttons)

    def test_admin_change_cost_buttons(self):
        buttons = [button.text for row in Admin_change_cost.keyboard for button in row]
        expected_buttons = [
            "🥡 Вартість коробки",
            "💐 Вартість букета",
            "⬅ Повернутися до меню",
        ]
        self.assertEqual(buttons, expected_buttons)

    def test_admin_back_to_choosing_roses_buttons(self):
        buttons = [
            button.text
            for row in Admin_back_to_choosing_roses.keyboard
            for button in row
        ]
        self.assertIn("⬅ Назад", buttons)

    def test_admin_orders_markup_buttons(self):
        buttons = [
            button.text for row in Admin_orders_markup.keyboard for button in row
        ]
        expected_buttons = [
            "Перевірка клієнтів за день",
            "Перевірка замовлень за останню годину",
            "Перевірка клієнтів за три дні",
            "Перевірка останніх 10 замовлень",
            "⬅ Повернутися до меню",
        ]
        self.assertEqual(buttons, expected_buttons)

    def test_admin_check_comments_buttons(self):
        buttons = [
            button.text for row in Admin_check_comments.keyboard for button in row
        ]
        expected_buttons = [
            "Переглянути коментарі за 1 тиждень",
            "Переглянути коментарі за 1 день",
            "⬅ Повернутися до меню",
        ]
        self.assertEqual(buttons, expected_buttons)

    def test_admin_bouquet_price_buttons(self):
        buttons = [
            button.text for row in Admin_bouquet_price.keyboard for button in row
        ]
        expected_buttons = [
            "101 flowers",
            "201 flowers",
            "301 flowers",
            "401 flowers",
            "501 flowers",
            "601 flowers",
            "701 flowers",
            "1001 flowers",
            "⬅ Повернутись до квітів",
        ]
        self.assertEqual(buttons, expected_buttons)

    def test_admin_bouquet_photo_buttons(self):
        buttons = [
            button.text for row in Admin_bouquet_photo.keyboard for button in row
        ]
        expected_buttons = [
            "101 ros",
            "201 ros",
            "301 ros",
            "401 ros",
            "501 ros",
            "601 ros",
            "701 ros",
            "1001 ros",
            "Box photo",
            "⬅ Повернутися до меню",
        ]
        self.assertEqual(buttons, expected_buttons)

    def test_settings_buttons(self):
        self.assertIsInstance(Settings, ReplyKeyboardMarkup)
        buttons = []
        for row in Settings.keyboard:
            for item in row:
                if isinstance(item, KeyboardButton):
                    buttons.append(item.text)
                else:
                    buttons.append(item)
        self.assertIn("Змінити мову", buttons)
        self.assertIn("⬅ Назад", buttons)

    def test_change_language_buttons(self):
        buttons = [button.text for row in change_language.keyboard for button in row]
        expected_buttons = ["🇺🇸 English", "🇺🇦 Українська", "⬅ Назад"]
        self.assertEqual(buttons, expected_buttons)

    def test_change_language_begin_buttons(self):
        buttons = [
            button.text for row in change_language_begin.keyboard for button in row
        ]
        expected_buttons = ["🇺🇸 English", "🇺🇦 Українська"]
        self.assertEqual(buttons, expected_buttons)

    def test_last_agree_buttons(self):
        buttons = [button.text for row in last_agree.keyboard for button in row]
        expected_buttons = ["✅ Так", "❌ Ні"]
        self.assertEqual(buttons, expected_buttons)

    def test_keyboards_reply(self):
        self.assertIn("ukr", keyboards_reply)
        self.assertIn("eng", keyboards_reply)
        self.assertIn("start", keyboards_reply["ukr"])
        self.assertIn("location", keyboards_reply["ukr"])
        self.assertIn("start", keyboards_reply["eng"])
        self.assertIn("location", keyboards_reply["eng"])
