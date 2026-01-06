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
admin_states = {}  # для ввода админа

def get_user(uid):
    if uid not in users:
        users[uid] = {
            "баланс": 0,
            "карандаши": 0,
            "осколки": 0,
            "часики": 0,
            "дрели": 0,
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
        "Астро осколки": {"price": {"деньги": 5000, "осколки": 10}},
        "Карандаши": {"price": {"деньги": 100, "карандаши": 5}},
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
# 4️⃣ Задания
# -----------------------------
QUESTS = {
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
        "desc": "Убить Джи 2.5 двадцать раз",
        "reward": {"деньги": 30000},
        "unlock": "UTCM"
    },
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
    bot.send_message(message.chat.id, "Привет! Выбирай ниже:", reply_markup=kb)

# -----------------------------
# 6️⃣ Баланс
# -----------------------------
@bot.callback_query_handler(func=lambda c: c.data=="balance")
def show_balance(c):
    user = get_user(c.from_user.id)
    text = f"💰 Деньги: {user['баланс']}\n🖍 Карандаши: {user['карандаши']}\n💎 Осколки: {user['осколки']}\n⏰ Часики: {user['часики']}\n🔧 Дрели: {user['дрели']}\n\n🧾 Предметы:\n" + ("\n".join(user["items"]) if user["items"] else "Пусто")
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
    # ищем цену
    price = None
    for section in SHOP.values():
        if item_name in section:
            price = section[item_name]['price']
    if price is None:
        bot.answer_callback_query(c.id, "Ошибка покупки")
        return
    # проверка всех валют
    for k, v in price.items():
        if user.get(k,0) < v:
            bot.answer_callback_query(c.id, f"❌ Недостаточно {k}")
            return
    # списываем
    for k, v in price.items():
        user[k] -= v
    user["items"].append(item_name)
    bot.answer_callback_query(c.id, f"✅ Куплено {item_name}")

# -----------------------------
# 8️⃣ Задания
# -----------------------------
@bot.callback_query_handler(func=lambda c: c.data=="quests")
def quests_menu(c):
    kb = types.InlineKeyboardMarkup()
    for qid in QUESTS.keys():
        kb.add(types.InlineKeyboardButton(QUESTS[qid]['name'], callback_data=f"quest_{qid}"))
    bot.answer_callback_query(c.id)
    bot.send_message(c.message.chat.id, "Выберите задание:", reply_markup=kb)

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
@bot.message_handler(commands=["admin"])
def admin_panel(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "❌ У вас нет доступа")
        return
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💰 Начислить деньги", callback_data="admin_add_money"))
    kb.add(types.InlineKeyboardButton("✅ Подтвердить задание", callback_data="admin_complete_quest"))
    bot.send_message(message.chat.id, "Админ панель:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data == "admin_add_money")
def admin_add_money_btn(c):
    if c.from_user.id not in ADMIN_IDS: return
    admin_states[c.from_user.id] = "add_money"
    bot.send_message(c.message.chat.id,
        "Введите:\nID_Игрока Валюта Сумма\nПример:\n6647482475 деньги 5000\n6647482475 карандаши 10")

@bot.callback_query_handler(func=lambda c: c.data == "admin_complete_quest")
def admin_complete_quest_btn(c):
    if c.from_user.id not in ADMIN_IDS: return
    admin_states[c.from_user.id] = "complete_quest"
    bot.send_message(c.message.chat.id,
        "Введите:\nID_Игрока ID_Задания\nПример:\n6647482475 UTTM_1")

@bot.message_handler(func=lambda m: m.from_user.id in admin_states)
def handle_admin_input(m):
    state = admin_states[m.from_user.id]

    # начисление валюты
    if state == "add_money":
        try:
            uid, currency, amount = m.text.split()
            uid = int(uid)
            amount = int(amount)
            user = get_user(uid)
            if currency not in user:
                user[currency] = 0
            user[currency] += amount
            bot.send_message(m.chat.id, f"✅ Выдано {amount} {currency} игроку {uid}")
        except:
            bot.send_message(m.chat.id, "❌ Ошибка. Пример: 6647482475 деньги 5000")

    # подтверждение квеста
    elif state == "complete_quest":
        try:
            uid, qid = m.text.split()
            uid = int(uid)
            if qid not in QUESTS:
                bot.send_message(m.chat.id, "❌ Нет такого задания")
                return
            user = get_user(uid)
            if qid in user["quests_done"]:
                bot.send_message(m.chat.id, "⚠️ Уже выполнено")
                return
            user["quests_done"].append(qid)
            for k, v in QUESTS[qid]["reward"].items():
                if k not in user:
                    user[k] = 0
                user[k] += v
            bot.send_message(m.chat.id, f"✅ Квест {qid} подтверждён\n🎁 Награда выдана игроку {uid}")
        except:
            bot.send_message(m.chat.id, "❌ Ошибка. Пример: 6647482475 UTTM_1")

    del admin_states[m.from_user.id]

# -----------------------------
# 10️⃣ Запуск
# -----------------------------
bot.infinity_polling()