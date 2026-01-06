import telebot
from telebot import types

TOKEN = "8559510337:AAFwfFrF45BRTE4PAausnMkvsCLLgnMsVT8"
ADMIN_IDS = [7303568633, 6647482475, 7572540880, 5205986826]

bot = telebot.TeleBot(TOKEN)

CURRENCIES = ["деньги", "часики", "дрели", "осколки_астро", "карандаши"]

users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = {
            "деньги": 0,
            "часики": 0,
            "дрели": 0,
            "осколки_астро": 0,
            "карандаши": 0,
            "items": [],
            "quests_done": []
        }
    return users[uid]

SHOP = {
    "Камерамены": {
        "Камера мен": {"price": {"деньги": 0}},
        "Биг кам": {"price": {"деньги": 500}},
        "Фред": {"price": {"деньги": 1000}},
    },
    "Спец титаны": {
        "UTCM": {"price": {"деньги": 30000}},
        "UTSM": {"price": {"деньги": 40000}},
        "UTTM": {"price": {"деньги": 500000}},
    }
}

QUESTS = {
    "Q1": {
        "name": "Убить Джи 2.0 5 раз",
        "desc": "Победи Джи 2.0 пять раз",
        "reward": {"деньги": 10000, "осколки_астро": 2},
        "unlock": "UTCM"
    },
    "Q2": {
        "name": "Убить Джи 3.0 10 раз",
        "desc": "Победи Джи 3.0 десять раз",
        "reward": {"деньги": 50000, "карандаши": 10},
        "unlock": "UTTM"
    }
}

@bot.message_handler(commands=["start"])
def start(message):
    get_user(message.from_user.id)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💰 Баланс", callback_data="balance"))
    kb.add(types.InlineKeyboardButton("🛒 Магазин", callback_data="shop"))
    kb.add(types.InlineKeyboardButton("📜 Задания", callback_data="quests"))
    kb.add(types.InlineKeyboardButton("🧑‍💻 Админ", callback_data="admin"))
    bot.send_message(message.chat.id, "выбери:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data=="balance")
def balance(c):
    u = get_user(c.from_user.id)
    text = "💰 твой баланс:\n"
    for cur in CURRENCIES:
        text += f"{cur}: {u[cur]}\n"
    bot.send_message(c.message.chat.id, text)

@bot.callback_query_handler(func=lambda c: c.data=="shop")
def shop(c):
    kb = types.InlineKeyboardMarkup()
    for s in SHOP:
        kb.add(types.InlineKeyboardButton(s, callback_data=f"shop_{s}"))
    bot.send_message(c.message.chat.id, "магазин:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("shop_"))
def shop_section(c):
    sec = c.data.replace("shop_","")
    kb = types.InlineKeyboardMarkup()
    for item in SHOP[sec]:
        price = SHOP[sec][item]["price"]
        txt = item + " "
        for k,v in price.items():
            txt += f"{v}{k} "
        kb.add(types.InlineKeyboardButton(txt, callback_data=f"buy_{item}"))
    bot.send_message(c.message.chat.id, sec, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def buy(c):
    item = c.data.replace("buy_","")
    u = get_user(c.from_user.id)
    for sec in SHOP:
        if item in SHOP[sec]:
            price = SHOP[sec][item]["price"]
            for k in price:
                if u[k] < price[k]:
                    bot.answer_callback_query(c.id,"не хватает "+k)
                    return
            for k in price:
                u[k] -= price[k]
            u["items"].append(item)
            bot.answer_callback_query(c.id,"куплено")
            return

@bot.callback_query_handler(func=lambda c: c.data=="quests")
def quests(c):
    kb = types.InlineKeyboardMarkup()
    for q in QUESTS:
        kb.add(types.InlineKeyboardButton(QUESTS[q]["name"], callback_data=f"q_{q}"))
    bot.send_message(c.message.chat.id,"задания:",reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("q_"))
def quest(c):
    q = QUESTS[c.data.replace("q_","")]
    t = f"{q['name']}\n{q['desc']}\nнаграда:\n"
    for k,v in q["reward"].items():
        t+=f"{k}: {v}\n"
    t+=f"открывает: {q['unlock']}"
    bot.send_message(c.message.chat.id,t)

@bot.callback_query_handler(func=lambda c: c.data=="admin")
def admin(c):
    if c.from_user.id not in ADMIN_IDS:
        return
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("выдать валюту", callback_data="admin_info"))
    bot.send_message(c.message.chat.id,"админ панель\nиспользуй /addcurrency и /setcurrency")

@bot.message_handler(commands=["addcurrency"])
def addcur(m):
    if m.from_user.id not in ADMIN_IDS:
        return
    _, uid, cur, amt = m.text.split()
    u = get_user(int(uid))
    u[cur] += int(amt)
    bot.send_message(m.chat.id,"выдано")

@bot.message_handler(commands=["setcurrency"])
def setcur(m):
    if m.from_user.id not in ADMIN_IDS:
        return
    _, uid, cur, amt = m.text.split()
    u = get_user(int(uid))
    u[cur] = int(amt)
    bot.send_message(m.chat.id,"установлено")

bot.infinity_polling()