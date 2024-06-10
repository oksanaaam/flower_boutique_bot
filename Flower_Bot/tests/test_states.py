import unittest
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.ukr_users.states import (
    StateOrderTime,
    States_,
    AddressState,
    Comments_,
    Translate,
    HelpConversation,
    OrderConfirmation,
    Advertisement,
    ChangeBoxPrice,
    ChangeBouquetPrice,
    ChangePicture,
    Authentication,
)


class TestStates(unittest.TestCase):
    def test_state_order_time(self):
        self.assertTrue(issubclass(StateOrderTime, StatesGroup))

    def test_states_(self):
        self.assertTrue(issubclass(States_, StatesGroup))

    def test_address_state(self):
        self.assertTrue(issubclass(AddressState, StatesGroup))

    def test_comments_(self):
        self.assertTrue(issubclass(Comments_, StatesGroup))

    def test_translate(self):
        self.assertTrue(issubclass(Translate, StatesGroup))

    def test_help_conversation(self):
        self.assertTrue(issubclass(HelpConversation, StatesGroup))

    def test_order_confirmation(self):
        self.assertTrue(issubclass(OrderConfirmation, StatesGroup))

    def test_advertisement(self):
        self.assertTrue(issubclass(Advertisement, StatesGroup))

    def test_change_box_price(self):
        self.assertTrue(issubclass(ChangeBoxPrice, StatesGroup))

    def test_change_bouquet_price(self):
        self.assertTrue(issubclass(ChangeBouquetPrice, StatesGroup))

    def test_change_picture(self):
        self.assertTrue(issubclass(ChangePicture, StatesGroup))

    def test_authentication(self):
        self.assertTrue(issubclass(Authentication, StatesGroup))
