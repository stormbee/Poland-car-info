from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    EnterPlate = State()
    EnterVIN = State()
    EnterDate = State()
    Results = State()