from aiogram.dispatcher.filters.state import State, StatesGroup


class StateOrderTime(StatesGroup):
    start_order_time = State()


class States_(StatesGroup):
    CHOOSING_OPTION = State()
    STYLE_NAME = State()
    CONFIRMATION = State()


class AddressState(StatesGroup):
    waiting_for_address = State()


class Comments_(StatesGroup):
    comments = State()


class Translate(StatesGroup):
    ukr_eng = State()


class OrderConfirmation(StatesGroup):
    yes_or_no = State()


class Advertisement(
    StatesGroup
):  # for admin
    advertisement = State()


class ChangeBoxPrice(StatesGroup):  # for admin
    change_box_price = State()


class ChangeBouquetPrice(StatesGroup):  # for admin
    change_bouquet_price = State()


class ChangePicture(StatesGroup):  # for admin
    show_picture = State()
    change_picture = State()


class Authentication(StatesGroup):  # for admin
    password = State()
