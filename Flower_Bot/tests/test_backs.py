from aiogram import types
import unittest
from unittest.mock import MagicMock, AsyncMock, patch
from handlers.ukr_users.backs import (
    back,
    back_location,
    back_to_bouquet,
    back_to_menu,
    back_to_setting_time,
)


class TestBackFunctions(unittest.IsolatedAsyncioTestCase):
    async def test_back(self):
        message = types.Message()
        message.chat = MagicMock()
        message.chat.id = 1
        message.answer = AsyncMock()

        with patch(
            "handlers.ukr_users.backs.TRANSLATE_USER_LANG.query_sql"
        ) as query_sql, patch(
            "handlers.ukr_users.backs.keyboards_reply"
        ) as keyboards_reply:
            query_sql.return_value = MagicMock(), MagicMock()
            keyboards_reply.get.return_value = {"start": MagicMock()}
            await back(message)

        message.answer.assert_called_once()

    async def test_back_location(self):
        message = types.Message()
        message.chat = MagicMock()
        message.chat.id = 1
        message.answer = AsyncMock()

        with patch(
            "handlers.ukr_users.backs.TRANSLATE_USER_LANG.query_sql"
        ) as query_sql, patch(
            "handlers.ukr_users.backs.keyboards_reply"
        ) as keyboards_reply:
            query_sql.return_value = MagicMock(), MagicMock()
            keyboards_reply.get.return_value = {"location": MagicMock()}
            await back_location(message)

        message.answer.assert_called_once()

    async def test_back_to_bouquet(self):
        message = types.Message()
        message.chat = MagicMock()
        message.chat.id = 1
        message.answer = AsyncMock()

        with patch(
            "handlers.ukr_users.backs.TRANSLATE_USER_LANG.query_sql"
        ) as query_sql, patch(
            "handlers.ukr_users.backs.keyboards_reply"
        ) as keyboards_reply:
            query_sql.return_value = MagicMock(), MagicMock()
            keyboards_reply.get.return_value = {"Bouquet": MagicMock()}

            await back_to_bouquet(message)

        message.answer.assert_called_once()

    async def test_back_to_menu(self):
        message = types.Message()
        message.chat = MagicMock()
        message.chat.id = 1
        message.answer = AsyncMock()

        with patch(
            "handlers.ukr_users.backs.TRANSLATE_USER_LANG.query_sql"
        ) as query_sql, patch(
            "handlers.ukr_users.backs.keyboards_reply"
        ) as keyboards_reply:
            query_sql.return_value = MagicMock(), MagicMock()
            keyboards_reply.get.return_value = {"Menu": MagicMock()}
            await back_to_menu(message)

        message.answer.assert_called_once()

    async def test_back_to_setting_time(self):
        message = types.Message()
        message.chat = MagicMock()
        message.chat.id = 1
        message.answer = AsyncMock()

        with patch(
            "handlers.ukr_users.backs.TRANSLATE_USER_LANG.query_sql"
        ) as query_sql, patch(
            "handlers.ukr_users.backs.keyboards_reply"
        ) as keyboards_reply:
            query_sql.return_value = MagicMock(), MagicMock()
            keyboards_reply.get.return_value = {"Order": MagicMock()}
            await back_to_setting_time(message)

        message.answer.assert_called_once()
