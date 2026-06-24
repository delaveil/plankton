import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
import requests
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token = os.getenv("BOT_TOKEN"))
TRAVEL_TOKEN = os.getenv("TRAVEL_TOKEN")

dp = Dispatcher()

def get_real_price(destination_iata):
    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"

    params = {
        "origin": "MOW",
        "destination": destination_iata,
        "one_way": "true",
        "currency": "rub",
        "limit": 1,
        "sorting": "price"
    }
    headers = {
        "X-Access-Token": TRAVEL_TOKEN
    }
    try:
        response = requests.get(
            url,
            params = params,
            headers = headers,
            timeout = 15
        )
        print(response.status_code)
        print(response.text)
        data = response.json()
        if not data.get("success"):
            return None

        flights = data.get("data", [])
        if not flights:
            return None
        return flights[0]["price"]
    except Exception as e:
        print(e)
        return None

class BudgetState(StatesGroup):
    waiting_for_budget = State()
class DirectionState(StatesGroup):
    waiting_for_city = State()    
    
# создание кнопок
normal_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "🌎 Поиск билета по направлению"),
            KeyboardButton(text = "🎲 Хочу туда, не знаю куда")
        ],
        [
            KeyboardButton(text = "💸 Подбор по бюджету"),
            KeyboardButton(text = "✨ Подбор по настроению")
        ],
        [
            KeyboardButton(text = "🎁 Совет путешественнику"),
            KeyboardButton(text = "👾 Порция дофамина")
        ]
    ],
    resize_keyboard = True
)
mood_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "🏖 Хочу море"),
            KeyboardButton(text = "🏔 Хочу горы")
        ],
        [
            KeyboardButton(text = "🍜 Хочу вкусно поесть"),
            KeyboardButton(text = "💃 Хочу развлечения")
        ],
        [KeyboardButton(text = "🔙 Назад")]
    ],
    resize_keyboard=True
)
search_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "🔙 Назад")]
    ],
    resize_keyboard = True
)

# обработка команды /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        'Добро пожаловать в АвиаБот! ✈️ \n\n'
        'Выберите действие:',
        reply_markup = normal_keyboard
        )
 
# кнопка поиска по направлению
@dp.message(lambda message: message.text == "🌎 Поиск билета по направлению")
async def direction_mode(message: types.Message, state: FSMContext):
    await message.answer(
        "🌍 Отлично! Куда отправимся?\n\n"
        "Введите название города \n"
        "(например: Минск, Тбилиси, Сочи, Стамбул): ",
        reply_markup = search_keyboard
    )
    await state.set_state(DirectionState.waiting_for_city)

# кнопка бюджета
@dp.message(lambda message: message.text == "💸 Подбор по бюджету")
async def budget_mode(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите бюджет в рублях:",
        reply_markup = search_keyboard
    )
    await state.set_state(BudgetState.waiting_for_budget)

# кнопка случайного направления
@dp.message(lambda message: message.text == "🎲 Хочу туда, не знаю куда")
async def buttons(message: types.Message, state: FSMContext):
   if message.text == "🎲 Хочу туда, не знаю куда":
     random_destination = random.choice(destinations)
     random_comment = random.choice(meme_comments)
     await message.answer(
        f"🎲 Колесо судьбы прокрутилось...\n\n"
        f"{random_comment}\n\n"

        f"Сегодня судьба рекомендует:\n\n"
        f"✈️ {random_destination['city']}\n"
        f"{random_destination['text']}\n\n"

        f"Не нравится вариант?\n"
        f"Нажмите кнопку ещё раз и попробуйте договориться со вселенной 😏"
    ) 

# обработка введенного города
@dp.message(DirectionState.waiting_for_city)
async def process_city(message: types.Message, state: FSMContext):
    city = message.text.lower().strip()

    if message.text == "🔙 Назад":
        await state.clear()
        await message.answer(
            "Возвращаемся в главное меню ✈️",
            reply_markup=normal_keyboard
        )
        return
    if city not in IATA_CODES:
        await message.answer(
            "😔 Кажется пока я не могу найти этот город в базе.\n"
            "Попробуйте другой."
        )
        return

    iata = IATA_CODES[city]
    price = get_real_price(iata)
    if price:
       price_text = f"{price:,}".replace(",", " ")

       await message.answer(
        f"🌍 {city.title()}\n\n"
        f"💸 Актуальная цена: от {price_text} ₽\n\n"
        f"🔥 Горячее предложение\n"
        f"🛫 Вылет из Москвы\n\n"
        f"🔎 Смотреть билеты: https://www.aviasales.ru"
        )
    else:
        await message.answer(
        f"😔 Не удалось найти актуальные данные по {city.title()}."
        )

    await message.answer(
    "🌍 Глянем другие города?\n\n"
    "Или вернёмся в главное меню?",
    reply_markup=search_keyboard
    )
    
    
# обработка введенного бюджета
@dp.message(BudgetState.waiting_for_budget)
async def process_budget(message: types.Message, state: FSMContext):
    try:
        if message.text == "🔙 Назад":
            await state.clear()
            await message.answer(
            "Возвращаемся в главное меню ✈️",
            reply_markup = normal_keyboard
        )
            return
        budget = int(message.text)
        if budget < 2000:
            await message.answer(
                "😅 За такой бюджет вариантов немного.\n"
                "Нажмите кнопку заново и попробуйте увеличить сумму."
            )
        elif budget < 7000:
            await message.answer(
                "✈️ За ваш бюджет можно рассмотреть:\n\n"
                "• Казань\n"
                "• Самара\n"
                "• Минск"
            )
        elif budget < 20000:
            await message.answer(
                "✈️ За ваш бюджет можно рассмотреть:\n\n"
                "• Сочи\n"
                "• Калининград\n"
                "• Ереван"
            )
        else:
            await message.answer(
                "😎 Бюджет позволяет путешествовать с размахом!\n"
                "Рекомендуем присмотреться к этим вариантам: \n\n"
                "• Стамбул\n"
                "• Дубай\n"
                "• Баку\n"
                "• Тбилиси"
            )
    except ValueError:
        await message.answer(
            "❌ Пожалуйста, введите число.\n\nНапример: 15000"
        )
    await state.clear()
    await message.answer("Что дальше? Выберите действие:", reply_markup = normal_keyboard)


# обработка остальных кнопок
@dp.message()
async def buttons(message: types.Message, state: FSMContext):

    if message.text == "🎁 Совет путешественнику":
      random_tip = random.choice(travel_tips)
      await message.answer(
        f"🎁 Напоминание для тебя:\n\n{random_tip}"
    )
      
    elif message.text == "👾 Порция дофамина":
         random_meme = random.choice(memes)
         photo = FSInputFile(random_meme)
         await message.answer_photo(
          photo = photo,
          caption = "Всегда на страже вайба🫡"
    )
         
    elif message.text == "✨ Подбор по настроению":
      await message.answer(
      "✈️ Давай подберём направление!\n\n"
      "Выбери настроение путешествия:",
      reply_markup = mood_keyboard
    )
      
    elif message.text == "🏖 Хочу море":
        price = get_real_price("AER")
        if price:
          price = f"{price:,}".replace(",", " ")
        else:
         price = "нет данных"
        await message.answer(
          "Система рекомендует:\n\n"
          "✈️ Сочи\n\n"
          "🏖 Тёплое море\n"
          "🌞 Много солнца\n"
          f"💸 Авиабилеты от {price} ₽\n\n"
          "Пора искать купальник 😎"
    )

    elif message.text == "🏔 Хочу горы":
        price = get_real_price("EVN")
        if price:
          price = f"{price:,}".replace(",", " ")
        else:
          price = "нет данных"
        await message.answer(
          "Система рекомендует:\n\n"
          "✈️ Ереван\n\n"
          "🌄 Расположен на вулканическом плато\n"
          "🍷 Отличная кухня\n"
          f"💸 Авиабилеты от {price} ₽\n\n"
          "Виды захватывают дух, а фотографии будут незабываемыми 📸"
    )

    elif message.text == "🍜 Хочу вкусно поесть":
        price = get_real_price("TBS")
        if price:
          price = f"{price:,}".replace(",", " ")
        else:
          price = "нет данных"
        await message.answer(
          "Система рекомендует:\n\n"
          "✈️ Тбилиси\n\n"
          "🥟 Хинкали\n"
          "🍷 Вино\n"
          "🍖 Шашлык\n"
          f"💸 Авиабилеты от {price} ₽\n\n"
          "Есть риск влюбиться в местную кухню 😋"
    )
        
    elif message.text == "💃 Хочу развлечения":
        price = get_real_price("IST")
        if price:
          price = f"{price:,}".replace(",", " ")
        else:
          price = "нет данных"
        await message.answer(
          "Система рекомендует:\n\n"
          "✈️ Стамбул\n\n"
          "☕ Кофейни\n"
          "🛍 Базары\n"
          "🌃 Ночная жизнь\n"
          f"💸 Авиабилеты от {price} ₽\n\n"
          "Скучать точно не придётся 🔥"
    )
        
    elif message.text == "🔙 Назад":
        await message.answer(
          "Возвращаемся в главное меню ✈️",
          reply_markup = normal_keyboard
    )

# коды городов 
IATA_CODES = {
    "минск": "MSQ",
    "москва": "MOW",
    "санкт-петербург": "LED",
    "сочи": "AER",
    "калининград": "KGD",
    "казань": "KZN",
    "самара": "KUF",
    "екатеринбург": "SVX",
    "новосибирск": "OVB",
    "владивосток": "VVO",
    "ереван": "EVN",
    "тбилиси": "TBS",
    "баку": "GYD",
    "стамбул": "IST",
    "дубай": "DXB",
    "анталья": "AYT",
    "рим": "ROM",
    "париж": "PAR",
    "барселона": "BCN",
    "берлин": "BER",
    "прага": "PRG",
    "будапешт": "BUD",
    "вена": "VIE",
    "лондон": "LON",
    "нью-йорк": "NYC",
    "варшава": "WAW",
    "токио": "TYO",
    "сеул": "SEL",
    "пекин": "BJS",
    "бангкок": "BKK",
    "пхукет": "HKT",
    "мале": "MLE",
    "бали": "DPS",
    "сингапур": "SIN"
}

# рекомендации точек назначения
destinations = [
    {
        "city": "Минск",
        "text": "🏡 Уютные улочки, драники и возможность почувствовать себя почти как дома."
    },
    {
        "city": "Калининград",
        "text": "🌊 Море, янтарь и ощущение, что ты почти в Европе."
    },
    {
        "city": "Казань",
        "text": "🍜 Татарская кухня и один из самых красивых кремлей России."
    },
    {
        "city": "Сочи",
        "text": "🏖 Солнце, море и фотографии для зависти коллег \n"
        "(и все это без загранника!)."
    },
    {
        "city": "Ереван",
        "text": "🍷 Горы, вино и еда, после которой сложно застегнуть джинсы."
    },
    {
        "city": "Стамбул",
        "text": "☕ Коты, чай и желание остаться ещё на пару дней."
    },
    {
        "city": "Тбилиси",
        "text": "🥟 Хинкали, старый город и очень гостеприимные люди."
    }
]

# шуточки
meme_comments = [
    "Работать ты всё равно уже не хочешь 🥱",
    "Чемодан мысленно собран.",
    "Судьба решила всё за тебя.",
    "Отпуск сам себя не отгуляет.",
    "Бухгалтерия пока ничего не подозревает.",
    "Этот вариант одобрен внутренним путешественником.",
    "Если не сейчас, то когда?",
    "Вселенная намекает взять пару дней выходных.",
    "Твой диван против, но его мнение никто не спрашивал.",
    "Жизнь слишком коротка, чтобы всё время сидеть дома."
]

# советы
travel_tips = [
    "🧳 Никогда не клади зарядку, документы и наушники в багаж. Проверено тысячами путешественников.",
    "✈️ Самые выгодные билеты часто появляются за 1–3 месяца до вылета.",
    "🎒 Перед полётом проверь размеры ручной клади. Особенно если летишь лоукостером.",
    "📱 Скачай офлайн-карты заранее. Интернет за границей может неприятно удивить ценами.",
    "💧 Возьми пустую бутылку для воды. После контроля безопасности её можно наполнить бесплатно.",
    "🌍 Сделай фото паспорта и сохрани его в телефоне на всякий случай.",
    "🏨 Адрес отеля лучше сохранить заранее, даже если уверен в навигаторе.",
    "💳 Всегда бери хотя бы одну запасную банковскую карту.",
    "🕶️ Солнцезащитные очки забываются чаще, чем кажется.",
    "😴 Не планируй экскурсию на 7 утра после ночного перелёта. Ты всё равно её проспишь."
]

# мемесы
memes = [f"memes/meme{i}.jpg" for i in range(1, 32)]

# запуск бота
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())