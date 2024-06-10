import unittest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import basket_callback, Delivery
from keyboards.inline.english_choise_inline_buttons import (
    to_box_eng,
    how_much_choise_eng,
    confirmation_eng,
)


class TestInlineKeyboardsEng(unittest.TestCase):
    def test_to_box_eng_keyboard(self):
        # Check the structure of to_box_eng keyboard
        self.assertIsInstance(to_box_eng, InlineKeyboardMarkup)
        self.assertEqual(len(to_box_eng.inline_keyboard), 2)

        # Check the buttons in the first row
        row1 = to_box_eng.inline_keyboard[0]
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
        row2 = to_box_eng.inline_keyboard[1]
        self.assertEqual(len(row2), 1)
        self.assertEqual(
            row2[0].callback_data,
            Delivery.new(
                item_name="Delivery", which_item="Box", how_many=1, how_much_it="5.000"
            ),
        )

    def test_how_much_choise_eng_keyboards(self):
        # Check the structure of how_much_choise_eng keyboards
        self.assertEqual(len(how_much_choise_eng), 8)
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

        for i, keyboard in enumerate(how_much_choise_eng):
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
                    which_item=button_labels_eng[i],
                    how_many=1,
                    how_much_it=selling_rate_eng[i],
                ),
            )

    def test_confirmation_eng_keyboard(self):
        # Check the structure of confirmation_eng keyboard
        self.assertIsInstance(confirmation_eng, InlineKeyboardMarkup)
        self.assertEqual(len(confirmation_eng.inline_keyboard), 1)

        # Check the buttons
        row = confirmation_eng.inline_keyboard[0]
        self.assertEqual(len(row), 2)
        self.assertIsInstance(row[0], InlineKeyboardButton)
        self.assertIsInstance(row[1], InlineKeyboardButton)
        self.assertEqual(row[0].callback_data, "confirm")
        self.assertEqual(row[1].callback_data, "cancel")
