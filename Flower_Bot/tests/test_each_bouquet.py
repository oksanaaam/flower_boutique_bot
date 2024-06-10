import unittest
from unittest.mock import AsyncMock

import pandas as pd
from handlers.ukr_users.each_bouquet import (
    get_data,
    number_to_emoji,
    check_basket,
    button_handler,
)
from aiogram import types


class TestFunctions(unittest.IsolatedAsyncioTestCase):
    async def test_get_data(self):
        data = [(1, "bouquet1", "100.00"), (2, "bouquet2", "50.00")]
        group, total_price, tariff, total = get_data(data)
        self.assertIsInstance(group, pd.DataFrame)
        self.assertIsInstance(total_price, str)
        self.assertIsInstance(tariff, str)
        self.assertIsInstance(total, str)

    def test_number_to_emoji(self):
        emoji_number = number_to_emoji("12345")
        self.assertEqual(emoji_number, "1️⃣2️⃣3️⃣4️⃣5️⃣")


class TestHandlers(unittest.IsolatedAsyncioTestCase):
    async def test_check_basket(self):
        message = types.Message(message_id=1, chat=types.Chat(id=123))
        message.reply = AsyncMock()
        await check_basket(message)
        message.reply.assert_called()
