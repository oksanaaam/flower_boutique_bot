from aiogram import types
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from handlers.admins.admin import (
    password,
    back_to_admin_panel,
    change_bouquets_cost,
    choose_bouquet_for_change_cost,
    change_img,
    new_customers,
)

from keyboards.reply.choise_reply_buttons import (
    Admin_bouquet_photo,
    Admin_bouquet_price,
    Admin_change_cost,
    Admin_orders_markup,
    Admin_panel_buttons,
)


class TestAdminHandlers(unittest.IsolatedAsyncioTestCase):
    async def test_back_to_admin_panel(self):
        message = types.Message()
        state = MagicMock()
        message.reply = AsyncMock()
        await back_to_admin_panel(message, state)
        message.reply.assert_called_once_with(
            "Адмін панель",
            reply_markup=Admin_panel_buttons,
        )

    async def test_password_incorrect(self):
        message = types.Message()
        state = MagicMock()
        state.finish = MagicMock()
        message.text = "incorrect_password"
        message.reply = AsyncMock()
        PASSWORD = "correct_password"  # Assuming correct password
        await password(message, state)
        message.reply.assert_called_once_with("Спробуйте ще раз")
        state.finish.assert_not_called()

    async def test_change_bouquets_cost(self):
        message = types.Message()
        message.reply = AsyncMock()

        await change_bouquets_cost(message)

        message.reply.assert_called_once_with(
            "Ціну якої квіткової композиції ви бажаєте змінити?",
            reply_markup=Admin_change_cost,
        )

    async def test_new_customers(self):
        message = types.Message()
        message.reply = AsyncMock()

        await new_customers(message)

        message.reply.assert_called_once_with(
            "Ви у розділі для перевірки нових клієнтів та замовлень",
            reply_markup=Admin_orders_markup,
        )

    async def test_choose_bouquet_for_change_cost(self):
        message = types.Message()
        message.answer = AsyncMock()

        await choose_bouquet_for_change_cost(message)

        message.answer.assert_called_once_with(
            "Оберіть букет, ціну якого ви хочете змінити:",
            reply_markup=Admin_bouquet_price,
        )

    async def test_change_img(self):
        message = types.Message()
        message.answer = AsyncMock()

        await change_img(message)

        message.answer.assert_called_once_with(
            text="Виберіть, яке зображення потрібно змінити:",
            reply_markup=Admin_bouquet_photo,
        )
