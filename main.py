import telebot
from telebot import types

# -----------------------------
# 1️⃣ Токен и админы
# -----------------------------
TOKEN = "8559510337:AAFwfFrF45BRTE4PAausnMkvsCLLgnMsVT8"
ADMIN_IDS = [7303568633, 6647482475, 7572540880, 5205986826]

bot = telebot.TeleBot(TOKEN)

# -----------------------------
# 2️⃣ Пользователи (баланс, предметы)
# -----------------------------
users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = {
            "баланс": 0,
            "часики": 0,
            "дрели": 0,
            "осколки": 0,
            "карандаши": 0,
            "items": [],
            "quests_done": []
        }
    return users[uid]

# -----------------------------
# 3️⃣ Магазин
# -----------------------------
SHOP = {
    "Камерамены": {
        "Камера мен": {"price": {"деньги": 0}},
        "Биг кам": {"price": {"деньги": 500}},
        "Фред": {"price": {"деньги": 1000}},
        "Камера вумен": {"price": {"деньги": 1250}},
        "Камера вумен 2.0": {"price": {"деньги": 5000}},
    },
    "Спикермены": {
        "Спикер мен": {"price": {"деньги": 150}},
        "Биг спикер": {"price": {"деньги": 950}},
        "Спикер вумен": {"price": {"деньги": 3000}},
        "Дарк спикер мен": {"price": {"деньги": 2250}},
    },
    "ТВмены": {
        "ТВ мен": {"price": {"деньги": 300}},
        "Биг ТВ": {"price": {"деньги": 1250}},
        "ТВ вумен": {"price": {"деньги": 2250}},
        "ТВ учёный": {"price": {"деньги": 2500}},
    },
    "Клоки": {
        "Клок мен": {"price": {"деньги": 2000, "часики": 1}},
        "Клок вумен": {"price": {"деньги": 10000, "часики": 8}},
        "Биг клок": {"price": {"деньги": 11000, "часики": 14}},
    },
    "Дрели": {
        "Дрель мен": {"price": {"деньги": 2000, "дрели": 5}},
        "Дрель вумен": {"price": {"деньги": 20000, "дрели": 15}},
        "Биг дрель": {"price": {"деньги": 8000, "дрели": 11}},
    },
    "Эксклюзивные": {
        "Три титан": {"price": {"деньги": 100000}},
        "Некромант туалет": {"price": {"деньги": 10000}},
        "Годжо камерамен": {"price": {"деньги": 10000}},
    },
    "Титаны": {
        "Титан Камера 1.0": {"price": {"деньги": 5000}},
        "Титан Спикер 1.0": {"price": {"деньги": 4000}},
        "Титан ТВ 1.0": {"price": {"деньги": 7000}},
        "Скибиди диджей": {"price": {"деньги": 4499}},
    },
    "Спец титаны": {
        "UTCM": {"price": {"деньги": 30000}},
        "UTSM": {"price": {"деньги": 40000}},
        "UTTM": {"price": {"деньги": 500000}},
    }
}

# -----------------------------
# 4️⃣ Задания (UTKM и UTTM)
# -----------------------------
QUESTS = {
    # ======== UТKM ========
    "UTKM_1": {
        "name": "Убить скибиди учёного 5 раз",
        "desc": "Убить скибиди учёного 5 раз за Титан Камера Мен",
        "reward": {"деньги": 10000},
        "unlock": "UTCM"
    },
    "UTKM_2": {
        "name": "Убить Джи 2.0 10 раз",
        "desc": "Победить Джи версии 2.0 десять раз",
        "reward": {"деньги": 20000},
        "unlock": "UTCM"
    },
    "UTKM_3": {
        "name": "Убить Джи 2.5 20 раз",
        "desc": "Уничтожить Джи версии 2.5 двадцать раз",
        "reward": {"деньги": 30000},
        "unlock": "UTCM"
    },
    "UTKM_4": {
        "name": "Собрать 10 осколков",
        "desc": "Найди и собери 10 осколков",
        "reward": {"осколки": 10},
        "unlock": "UTCM"
    },
    "UTKM_5": {
        "name": "Собрать 5 карандашей",
        "desc": "Найди и собери 5 карандашей",
        "reward": {"карандаши": 5},
        "unlock": "UTCM"
    },

    # ======== UТTM ========
    "UTTM_1": {
        "name": "Собрать всю расу ТВ",
        "desc": "Иметь всех ТВ менов до 67 серии",
        "reward": {"деньги": 50000},
        "unlock": "UTTM"
    },
    "UTTM_2": {
        "name": "Быть на 80 волне за ТВ титана",
        "desc": "Дойти до 80 волны и выиграть за Титан ТВ",
        "reward": {"деньги": 75000},
        "unlock": "UTTM"
    },
    "UTTM_3": {
        "name": "Убить Джи 3.0 20 раз",
        "desc": "Уничтожить Джи версии 3.0 двадцать раз",
        "reward": {"деньги": 100000},
        "unlock": "UTTM"
    },
    "UTTM_4": {
        "name": "Собрать 20 осколков",
        "desc": "Найди и собери 20 осколков",
        "reward": {"осколки": 20},
        "unlock": "UTTM"
    },
    "UTTM_5": {
        "name": "Собрать 10 карандашей",
        "desc": "Найди и собери 10 карандашей",
        "reward": {"карандаши": 10},
        "unlock": "UTTM"
    }
}

# -----------------------------
# 5️⃣ Команды
# -----------------------------
@bot.message_handler(commands=["start"])
def start(message):
    user = get_user(message.from_user.id)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💰 Баланс", callback_data="balance"))
    kb.add(types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"))
    kb.add(types.InlineKeyboardButton("📜 Задания", callback_data="quests"))
    kb.add(types.InlineKeyboardButton("⚙️ Админ-панель", callback_data="admin_panel"))
    bot.send_message(message.chat.id, "Привет! Выбирай ниже:", reply_markup=kb)

# -----------------------------
# 6️⃣ Баланс
# -----------------------------
@bot.callback_query_handler(func=lambda c: c.data=="balance")
def show_balance(c):
    user = get_user(c.from_user.id)
    text = f"💰 Деньги: {user['баланс']}\n⏱ Часики: {user['часики']}\n🛠 Дрели: {user['дрели']}\n💎 Осколки: {user['осколки']}\n✏ Карандаши: {user['карандаши']}\n"
    text += "🧾 Твои предметы:\n" + "\n".join(user["items"]) if user["items"] else "Пусто"
    bot.answer_callback_query(c.id)
    bot.send_message(c.message.chat.id, text)

# -----------------------------
# 7️⃣ Магазин
# -----------------------------
@bot.callback_query_handler(func=lambda c: c.data=="shop")
def shop_menu(c):
    kb = types.InlineKeyboardMarkup()
    for section in SHOP.keys():
        kb.add(types.InlineKeyboardButton(section, callback_data=f"shop_{section}"))
    bot.answer_callback_query(c.id)
    bot.send_message(c.message.chat.id, "Выберите раздел магазина:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("shop_"))
def shop_section(c):
    section_name = c.data.replace("shop_", "")
    kb = types.InlineKeyboardMarkup()
    for item in SHOP[section_name].keys():
        price_text = ", ".join(f"{v} {k}" for k, v in SHOP[section_name][item]['price'].items())
        kb.add(types.InlineKeyboardButton(f"{item} - {price_text}", callback_data=f"buy_{item}"))
    kb.add(types.InlineKeyboardButton("⬅ Назад", callback_data="shop"))
    bot.answer_callback_query(c.id)
    bot.send_message(c.message.chat.id, f"Раздел: {section_name}", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def buy_item(c):
    item_name = c.data.replace("buy_", "")
    user = get_user(c.from_user.id)
    price = None
    for section in SHOP.values():
        if item_name in section:
            price = section[item_name]['price']
    if not price:
        bot.answer_callback_query(c.id, "Ошибка покупки")
        return

    can_buy = True
    for cur, amount in price.items():
        if user.get(cur, 0) < amount:
            can_buy = False
            break

    if can_buy:
        for cur, amount in price.items():
            user[cur] -= amount
        user["items"].append(item_name)
        bot.answer_callback_query(c.id, f"✅ Куплено {item_name}")
    else:
        bot.answer_callback_query(c.id, "❌ Недостаточно средств")

# -----------------------------
# 8️⃣ Задания
# -----------------------------
@bot.callback_query_handler(func=lambda c: c.data=="quests")
def quests_menu(c):
    kb = types.InlineKeyboardMarkup()
    # выводим по разделам
    kb.add(types.InlineKeyboardButton("UTKM", callback_data="quests_UTKM"))
    kb.add(types.InlineKeyboardButton("UTTM", callback_data="quests_UTTM"))
    bot.answer_callback_query(c.id)
    bot.send_message(c.message.chat.id, "Выберите раздел заданий:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("quests_"))
def quest_section(c):
    section = c.data.replace("quests_", "")
    kb = types.InlineKeyboardMarkup()
    for qid, q in QUESTS.items():
        if section in qid:
            kb.add(types.InlineKeyboardButton(q["name"], callback_data=f"quest_{qid}"))
    kb.add(types.InlineKeyboardButton("⬅ Назад", callback_data="quests"))
    bot.answer_callback_query(c.id)
    bot.send_message(c.message.chat.id, f"Задания раздела {section}:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("quest_"))
def quest_info(c):
    qid = c.data.replace("quest_", "")
    q = QUESTS[qid]
    text = f"📜 {q['name']}\n\n{q['desc']}\n\n🎁 Награда:\n"
    for k, v in q["reward"].items():
        text += f"{k}: {v}\n"
    text += f"\n🔓 Открывает персонажа: {q['unlock']}"
    bot.answer_callback_query(c.id)
    bot.send_message(c.message.chat.id, text)

# -----------------------------
# 9️⃣ Админ панель
# -----------------------------
@bot.callback_query_handler(func=lambda c: c.data=="admin_panel")
def admin_panel(c):
    if c.from_user.id not in ADMIN_IDS:
        bot.answer_callback_query(c.id, "❌ У вас нет доступа")
        return
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💰 Начислить валюту", callback_data="admin_add_currency"))
    kb.add(types.InlineKeyboardButton("✅ Подтвердить задание", callback_data="admin_complete_quest"))
    bot.answer_callback_query(c.id)
    bot.send_message(c.message.chat.id, "Админ панель:", reply_markup=kb)

# -----------------------------
# 10️⃣ Функции для админа
# -----------------------------
def add_currency(uid, currency, amount):
    user = get_user(uid)
    if currency in user:
        user[currency] += amount

def set_currency(uid, currency, amount):
    user = get_user(uid)
    if currency in user:
        user[currency] = amount

# -----------------------------
# 11️⃣ Запуск
# -----------------------------
bot.infinity_polling()