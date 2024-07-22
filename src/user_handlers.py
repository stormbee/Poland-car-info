import os
import time
from aiogram import Bot, Router, F
from aiogram.filters import CommandStart
from aiogram.filters.base import Filter
from aiogram.types import Message, Update, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from form import Form
from aiogram.filters import StateFilter

from main import find_car_data

class IsAdmin(Filter):
    async def __call__(self, update: Update, *args, **kwargs) -> bool:
        user_id = update.from_user.id
        return user_id in LIST_ID

router = Router()
LIST_ID = [5848825754]

# @router.message(CommandStart(), IsAdmin())
@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Поиск машины",
        callback_data="start_search")
    )
    await message.answer(
        text="Hello, admin!",
        reply_markup=builder.as_markup()
                                            
        )
    
    
@router.callback_query(F.data == 'start_search')
async def get_car_plate(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.EnterPlate)
    await callback.message.answer("Введите номер автомобиля")
    
    
@router.message(StateFilter(Form.EnterPlate))
async def get_car_vin(message: Message, state: FSMContext):
    await state.set_state(Form.EnterVIN)
    await state.update_data(plate=message.text)
    await message.answer("Введите VIN автомобиля")

@router.message(StateFilter(Form.EnterVIN))
async def get_car_date(message: Message, state: FSMContext):
    await state.set_state(Form.EnterDate)
    await state.update_data(vin=message.text)
    await message.answer("Введите дату регистрации автомобиля")
    
@router.message(StateFilter(Form.EnterDate))
async def get_result(message: Message, state: FSMContext, bot: Bot):
    await state.set_state(Form.Results)
    await state.update_data(date=message.text)
    data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Посчитать", callback_data='calculate')).add(InlineKeyboardButton(text="Отменить", callback_data='cancel'))
    await bot.send_message(
        chat_id=message.from_user.id,
        text = f"Номер: {data['plate']}\nVIN: {data['vin']}\nДата: {data['date']}",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == 'calculate')
async def calculate(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    plate = data['plate']
    vin = data['vin']
    date = data['date']
    await find_car_data(plate, vin, date)
    time.sleep(10)
    # TODO: optimize check file if exists also add exception handling for file not found or other errors
    if os.path.exists(f'{plate}.pdf'):
        file = FSInputFile(f'{plate}.pdf')
        await callback.message.answer_document(document=file)
        os.remove(f'{plate}.pdf')
    else:
        await callback.message.answer("Не найдено")
    await callback.answer()
    # await callback.message.answer("Идет поиск...")
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Поиск машины",
        callback_data="start_search")
    )
    await callback.message.answer(
        text="Начнём сначала",
        reply_markup=builder.as_markup()
                                            
        )

    
@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Поиск машины",
        callback_data="start_search")
    )
    await callback.message.answer(
        text="Начнём сначала",
        reply_markup=builder.as_markup()
                                            
        )
    await callback.answer()
     
    
    

    
    
    