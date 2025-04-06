from aiogram.fsm.state import State, StatesGroup


class CatalogStates(StatesGroup):
    waiting_catalog_title = State()
    waiting_catalog_privacy = State()
    waiting_edit_title = State()