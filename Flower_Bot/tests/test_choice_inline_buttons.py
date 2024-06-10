import unittest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import basket_callback, Delivery
from keyboards.inline.english_choise_inline_buttons import (
    to_box_eng,
    how_much_choise_eng,
    confirmation_eng,
)
from keyboards.inline.choice_inline_buttons import (
    to_box,
    how_much_choise,
    confirmation,
    inline_keyboards,
)  # Import your objects


class TestInlineKeyboards(unittest.TestCase):
    def test_to_box_keyboard(self):
        # Check the structure of to_box keyboard
        self.assertIsInstance(to_box, InlineKeyboardMarkup)
        self.assertEqual(len(to_box.inline_keyboard), 2)

        # Check the buttons in the first row
        row1 = to_box.inline_keyboard[0]
        self.assertEqual(len(row1), 3)
        self.assertIsInstance(row1[0], InlineKeyboardButton)
        self.assertIsInstance(row1[1], InlineKeyboardButton)
        self.assertIsInstance(row1[2], InlineKeyboardButton)

        # Check the callback data of buttons in the first row
        self.assertEqual(
            row1[0].callback_data, basket_callback.new(item_name="minus", how_much=0)
        )
        self.assertEqual(
            row1[1].callback_data, basket_callback.new(item_name="sum", how_much=1)
        )
        self.assertEqual(
            row1[2].callback_data, basket_callback.new(item_name="plus", how_much=0)
        )

        # Check the second row
        row2 = to_box.inline_keyboard[1]
        self.assertEqual(len(row2), 1)
        self.assertEqual(
            row2[0].callback_data,
            Delivery.new(
                item_name="Delivery",
                which_item="Коробка",
                how_many=1,
                how_much_it="5.000",
            ),
        )

    def test_how_much_choise_keyboards(self):
        # Check the structure of how_much_choise keyboards
        self.assertEqual(len(how_much_choise), 8)
        button_labels = ["101", "201", "301", "401", "501", "601", "701", "1001"]
        selling_rate = [
            "3.000",
            "6.000",
            "10.000",
            "14.000",
            "19.000",
            "26.000",
            "31.000",
            "40.000",
        ]

        for i, keyboard in enumerate(how_much_choise):
            self.assertIsInstance(keyboard, InlineKeyboardMarkup)
            self.assertEqual(len(keyboard.inline_keyboard), 2)

            # Check the buttons in the first row
            row1 = keyboard.inline_keyboard[0]
            self.assertEqual(len(row1), 3)
            self.assertIsInstance(row1[0], InlineKeyboardButton)
            self.assertIsInstance(row1[1], InlineKeyboardButton)
            self.assertIsInstance(row1[2], InlineKeyboardButton)

            # Check the callback data of buttons in the first row
            self.assertEqual(
                row1[0].callback_data,
                basket_callback.new(item_name="minus", how_much=0),
            )
            self.assertEqual(
                row1[1].callback_data, basket_callback.new(item_name="sum", how_much=1)
            )
            self.assertEqual(
                row1[2].callback_data, basket_callback.new(item_name="plus", how_much=0)
            )

            # Check the second row
            row2 = keyboard.inline_keyboard[1]
            self.assertEqual(len(row2), 1)
            self.assertEqual(
                row2[0].callback_data,
                Delivery.new(
                    item_name="Delivery",
                    which_item=button_labels[i],
                    how_many=1,
                    how_much_it=selling_rate[i],
                ),
            )

    def test_confirmation_keyboard(self):
        # Check the structure of confirmation keyboard
        self.assertIsInstance(confirmation, InlineKeyboardMarkup)
        self.assertEqual(len(confirmation.inline_keyboard), 1)

        # Check the buttons
        row = confirmation.inline_keyboard[0]
        self.assertEqual(len(row), 2)
        self.assertIsInstance(row[0], InlineKeyboardButton)
        self.assertIsInstance(row[1], InlineKeyboardButton)
        self.assertEqual(row[0].callback_data, "confirm")
        self.assertEqual(row[1].callback_data, "cancel")

    def test_inline_keyboards(self):
        # Check the structure of inline_keyboards dictionary
        self.assertIn("ukr", inline_keyboards)
        self.assertIn("eng", inline_keyboards)

        # Check the Ukrainian keyboards
        ukr_keyboards = inline_keyboards["ukr"]
        self.assertEqual(ukr_keyboards["to_box"], to_box)
        self.assertEqual(ukr_keyboards["how_much_choise"], how_much_choise)
        self.assertEqual(ukr_keyboards["confirmation"], confirmation)

        # Check the English keyboards
        eng_keyboards = inline_keyboards["eng"]
        self.assertEqual(eng_keyboards["to_box"], to_box_eng)
        self.assertEqual(eng_keyboards["how_much_choise"], how_much_choise_eng)
        self.assertEqual(eng_keyboards["confirmation"], confirmation_eng)
