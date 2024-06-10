import unittest
from unittest.mock import MagicMock, AsyncMock, patch

from handlers.eng_users.english_each_bouquet import check_basket, button_handler


class TestCheckBasket(unittest.IsolatedAsyncioTestCase):
    async def test_check_basket_empty(self):
        message = MagicMock()
        message.chat.id = 123456
        message.text = "📥 Basket"
        message.reply = AsyncMock()

        with patch("sqlite3.connect") as mock_connect:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = []
            mock_cursor.fetchall.side_effect = [[], []]  # For both queries
            mock_connect.return_value.cursor.return_value = mock_cursor

            await check_basket(message)

            message.reply.assert_called_once_with("📥 Your basket is empty")

    async def test_check_basket_with_items(self):
        message = AsyncMock()
        message.chat = MagicMock()
        message.chat.id = 123456
        message.text = "📥 Basket"
        message.answer = AsyncMock()

        with patch("sqlite3.connect") as mock_connect:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.side_effect = [
                [(3, "101 roses", "100.00"), (1, "Коробка", "50.00")],
                [("101 roses",), ("Коробка",)],
            ]
            mock_connect.return_value.cursor.return_value = mock_cursor

            await check_basket(message)

            message.answer.called_once()

    async def test_button_handler(self):
        message = MagicMock()
        message.text = "101 roses"
        message.answer = AsyncMock()

        with patch("builtins.open"), patch("aiogram.types.PhotoSize"), patch(
            "loader.bot.send_photo"
        ) as mock_send_photo:
            await button_handler(message, MagicMock())

            mock_send_photo.assert_called()
