import unittest
from aiogram.utils.callback_data import CallbackData
from keyboards.inline.callback_datas import basket_callback, button_callback, Delivery


class TestCallbackData(unittest.TestCase):
    def test_basket_callback(self):
        self.assertIsInstance(basket_callback, CallbackData)
        callback_data = basket_callback.new(item_name="rose", how_much=10)
        self.assertEqual(callback_data, "basket:rose:10")

    def test_button_callback(self):
        self.assertIsInstance(button_callback, CallbackData)
        callback_data = button_callback.new(time="12")
        self.assertEqual(callback_data, "button:12")

    def test_delivery_callback(self):
        self.assertIsInstance(Delivery, CallbackData)
        callback_data = Delivery.new(
            item_name="rose", which_item="flower", how_many=10, how_much_it=100
        )
        self.assertEqual(callback_data, "to_basket:rose:flower:10:100")
