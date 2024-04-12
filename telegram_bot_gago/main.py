import telebot
import sqlite3 as sql
import threading
import time


import sys
import logging

logging.basicConfig(
    filename="error.log", encoding="utf-8", level=logging.ERROR
)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def handle_exception(exc_type, exc_value, exc_traceback):
    logger.error(
        "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
    )


sys.excepthook = handle_exception


#База Данных
con = sql.connect("data.db", check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, phone_number TEXT)")


first_name = None 
last_name = None
phone_number = None
users = None
#fiFILE_PATHle
LinkVideo = "https://www.youtube.com/watch?si=j88qE9HpftDIjsau&v=SyMQpGFc8pY&feature=youtu.be"
message_copy = None

#Ваш бот
token = "6488193207:AAE4RCqR_mBiRriXdoo_SaK83QRRuz9PMq8"
bot = telebot.TeleBot(token)

#ID Вашего канала
chan_id = "-1002107143246"
LINK = "https://t.me/GagikMnatsakanyan"

#Клавиатура для проверки подписки
keyboard = telebot.types.InlineKeyboardMarkup()
subscribe = telebot.types.InlineKeyboardButton(text="Միանալ", url=LINK)
check = telebot.types.InlineKeyboardButton(text="Ստանալ", callback_data="check")
details = telebot.types.InlineKeyboardButton(text="Մանրամասներ", callback_data="details")
continuee = telebot.types.InlineKeyboardButton(text="Շարունակել", callback_data="continuee")
opinions = telebot.types.InlineKeyboardButton(text="Կարծիքներ", callback_data="opinions") 
keyboard.add(subscribe)
keyboard.add(check)

detail_mk = telebot.types.InlineKeyboardMarkup()
details = telebot.types.InlineKeyboardButton(text="մանրամասներ", callback_data="details")
detail_mk.add(details)

continuee_mk = telebot.types.InlineKeyboardMarkup()
continuee = telebot.types.InlineKeyboardButton(text="շարունակել", callback_data="continuee")
continuee_mk.add(continuee)

opinions_mk = telebot.types.InlineKeyboardMarkup()
opinions = telebot.types.InlineKeyboardButton(text="Կարծիքներ", callback_data="opinions")
opinions_mk.add(opinions)

know_lesson_mk = telebot.types.InlineKeyboardMarkup()
know_lesson = telebot.types.InlineKeyboardButton(text="Իմանալ դասընթացի մասին", callback_data="know_lesson")
know_lesson_mk.add(know_lesson)

lesson_mk = telebot.types.InlineKeyboardMarkup()
lesson = telebot.types.InlineKeyboardButton(text="շարունակել", callback_data="lesson")
lesson_mk.add(lesson)

possibility_mk = telebot.types.InlineKeyboardMarkup()
possibility = telebot.types.InlineKeyboardButton(text="շարունակել", callback_data="possibility")
possibility_mk.add(possibility)

end_lesson_mk = telebot.types.InlineKeyboardMarkup()
end_lesson = telebot.types.InlineKeyboardButton(text="շարունակել", callback_data="end_lesson")
end_lesson_mk.add(end_lesson)

price_lesson_mk = telebot.types.InlineKeyboardMarkup()
price_lesson = telebot.types.InlineKeyboardButton(text="հատուկ առաջարկ", callback_data="price_lesson")
price_lesson_mk.add(price_lesson)


register_mk = telebot.types.InlineKeyboardMarkup()
register = telebot.types.InlineKeyboardButton(text="գրանցվել", callback_data="register")
register_mk.add(register)



@bot.message_handler(commands=["start"])
def start(message):
    global message_copy
    message_copy = message
    
    if users == None: #Если юзер ещё не в БД
        try:
            bot.send_message(message.chat.id, f"""Ողջույն, {message.from_user.first_name} 🖐️

❗️վիդեոդասը հասանելի է միայն իմ տելեգրամ ալիքի հետևորդներին

Ընդամենը մեկ քայլ, միացեք ալիքին և անմիջապես կստանաք վիդեոդասը""", reply_markup=keyboard)
        
        except telebot.apihelper.ApiTelegramException as e:
            logger.error(f"Ошибка при starte {e}")
  


def send_delayed_message(chat_id, message, delay=5, reply_markup=None):
    """Отправляет задержанное сообщение с задержкой."""
    def task():
        time.sleep(delay)  # Задержка
        try:
            bot.send_message(chat_id, message, reply_markup=reply_markup)
        except telebot.apihelper.ApiTelegramException as e:
            logger.error(f"Ошибка при отправке задержанного сообщения: {e}")

    thread = threading.Thread(target=task)
    thread.start()



@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    global message_copy
    try:
        if call.data == "check":
                x = bot.get_chat_member(chan_id, call.message.chat.id)
                if x.status == "member" or x.status == "creator" or x.status == "administrator":
                    bot.send_message(call.message.chat.id, "Բարի գալուստ!")
                    # bot.send_document(call.message.chat.id, document=open(LinkVideo, 'rb'))
                    bot.send_message(call.message.chat.id, LinkVideo)
                    send_delayed_message(call.message.chat.id, f"""
                                        Սիրելի {message_copy.from_user.first_name} այժմ դուք գիտեք ինչպես են աշխատում ինստագրամի ալգորիթմները րիլսերի վրա

❗️Բայց պրոֆեսիոնալ րիլսեր ստանալու համար, ձեզ խորը պրակտիկա է հարկավոր 🔥

✔️ Ես կսովորեցնեմ ձեզ նկարահանել րիլսեր և կազմել էջի այնպիսի վիզուալ, որը կզարմացնի բոլորին

« դուք ինքներդ կզարմանաք ձեր նկարահանած րիլսերի և կազմած վիզուալի վրա »

Դուք կսովորեք այս ամենը, բայց նախ մի փոքր ներածություն

👇 Սեղմեք ստորին կոճակը
                                                            """, delay=271, reply_markup=detail_mk)


                else:
                    bot.send_message(call.message.chat.id, "Դուք բաժանորդագրված չեք!")
        elif call.data == 'details':
            bot.send_message(call.message.chat.id, f"""Ես Գագիկ Մնացականյանն եմ։
Ես պրոֆեսիոնալ մարքեթոլոգ եմ, ով խորապես զբաղվում է SMM - ով

SMM - ը կարճ ժամանակահատվածում փոխեց իմ կյանքը և այսօր ❌ չեմ կարող պատկերացնել հետագա կյանքս, առանց իմ սիրած աշխատանքի

✅ Ես համոզվեցի, որ ցանկության դեպքում ամսական 200 հազարը, կարելի է դարձնել 2 մլն, SMM - ի շնորհիվ

😱 և նրանք ովքեր այսօր բաց են թողնում սովորելու հնարավորությունը, վաղը շատ են ափսոսելու

Իմ ուսանողները աշխարհի տարբեր ծայրերում գտնվող հայերն են, այդ թվում ԱՄՆ, Շրի Լանկա, Բելգիա և ՌԴ

✔️ Իմ հիմնած Full SMM 0-ից դասընթացը շատ լավ հնարավորություն է ձեռք բերել դարի ամենապահանջված մասնագիտություներից մեկը

✔️ Կամ եթե ունեք բիզնես, բաց մի թողեք այս հնարավորությունը ստեղծել կայուն վաճառող էջ ինստագրամում

❗️ Իսկ հիմա կարող եք տեսնել արդեն դասընթացն ավարտած ուսանողների կարծիքները

Սեղմեք 👇

""", reply_markup=opinions_mk)
        elif call.data == "opinions":
            # Отправка фото
            for i in range(1,7):
                if i >= 6:
                    bot.send_photo(call.message.chat.id, photo=open(f'photo{i}', 'rb'))
                    send_delayed_message(call.message.chat.id, f"""❗️ Սրանք կարծիքների շատ փոքր մասն է, մնացած մասով ես կիսվել եմ իմ էջի « դասընթաց » ակտուալ ալբոմում""", delay=2)
                    send_delayed_message(call.message.chat.id, f"""Ես մտածել եմ ձեր հետագա աշխատանքի համար դասընթացը ավարտելուց հետո

✅ Գուցե ինչ-որ բան մոռանաք և չկարողանաք գործի դնել

Այդ պատճառով պատրաստել եմ հավելյալ ՎԻԴԵՈԴԱՍԵՐ

✅ Եթե հետագայում ինչ-որ բան մոռանաք, կարող եք բացել այդ թեմայի վիդեոդասը և վերհիշել գիտելիքը

❗️ Ես կտամ ձեզ նաև աշխատանքային պորտֆոլիո, ըստ ձեր կատարած աշխատանքների դասընթացի ընթացքում, որը շատ կօգնի մասնագետներին աշխատանք գտնելու հարցում

ԵՎ այս պահին գործում է հատուկ առաջարկ դասընթացի գնառաջարկի վերաբերյալ

👇 Սեղմեք ստորին կոճակը
 """, delay=3, reply_markup=price_lesson_mk)
                else: 
                    bot.send_photo(call.message.chat.id, photo=open(f'photo{i}', 'rb'))

    
    
        elif  call.data == "price_lesson":
            bot.send_message(call.message.chat.id, f"""
ՊՐՈՄՈ ԿՈԴ ՁԵԶ ՀԱՄԱՐ

Դասընթացը արժե 63 հզր դրամ, բայց այս պահին կա հատուկ գին՝ օգտագործելով LIST պրոմոկոդը

🔥 Ընդամենը 55 հզր դրամ SMM մասնագիտություն ձեռք բերելու համար, որը կօգնի թե ձեր բիզնեսի վաճառքները բազմապատկել ինստագրամում, թե ձեր վաճառքները որպես մասնագետ ( ցանկացած ոլորտի )

‼️ Առաջարկը սահմանափակ է և կարող է սառեցվել ցանկացած պահի

Գրանցվելու համար, սեղմեք այստեղ 👇
""", reply_markup=register_mk)
        
        elif  call.data == "register":
            bot.send_message(call.message.chat.id, "Գրեք ձեր անունը")
            bot.register_next_step_handler(call.message, get_first_name)

    except telebot.apihelper.ApiTelegramException as e:
            logger.error(f"Ошибка при отправке фото: {e}")

def get_first_name(message):
    global first_name
    try:
        first_name = message.text.strip()
        bot.send_message(message.chat.id, "Գրեք պրոմոկոդը")
        bot.register_next_step_handler(message, get_last_name)
    except telebot.apihelper.ApiTelegramException as e:
        logger.error(f"Ошибка при отправке имени: {e}")

def get_last_name(message):
    global last_name
    try:
        last_name = message.text.strip()
        bot.send_message(message.chat.id, "Գրեք ձեր հեռ․ համարը")
        bot.register_next_step_handler(message, phone)
    except telebot.apihelper.ApiTelegramException as e:
        logger.error(f"Ошибка при отправке фамили: {e}")

    


def phone(message):
    global phone_number
    try:
        phone_number = message.text.strip()
        
        conn = sql.connect('data.db')
        cur = conn.cursor()
    
        # Параметризированный запрос для предотвращения SQL инъекций
        cur.execute("INSERT INTO users (first_name, last_name, phone_number) VALUES (?, ?, ?)", (first_name, last_name, phone_number))
        conn.commit()
    
        cur.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
        last_record = cur.fetchone()  # Получаем последнюю запись
    
        # Закрываем курсор и соединение
        cur.close()
        conn.close()
    
    # Проверяем, что запись не пустая
        if last_record:
            # Получаем данные из последней записи

            last_first_name=last_record[1]
            last_last_name=last_record[2]
            last_phone_number=last_record[3]

            # Отправляем сообщение с данными последней записи в определенный чат
            bot.send_message("6066680903", f"Նոր գրանցում:\nԱնուն: {last_first_name}\nԱզգանուն: {last_last_name}\nՀեռ: {last_phone_number}")
        else:
            # Если база данных пуста, отправляем сообщение об этом
            bot.send_message("6066680903", "База данных пуста")


        bot.send_message(message.chat.id, """🔥 Գրանցումը հաջողությամբ կատարվեց, ես հնարավորինս շուտ կկապվեմ ձեզ հետ ☺️""")

    except telebot.apihelper.ApiTelegramException as e:
        logger.error(f"Ошибка при отправке номера: {e}")




@bot.message_handler()
def get_data(message):
    try:
        if message.text.lower() == "get_all_data":

            conn = sql.connect('data.db')
            cur = conn.cursor()

            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            info = ''

            for el in users:
                info += f"Անուն: {el[1]}, Ազգանուն: {el[2]}, Հեռ: {el[3]}\n"


            cur.close()
            conn.close()

            bot.send_message(message.chat.id, info)

    except telebot.apihelper.ApiTelegramException as e:
        logger.error(f"Ошибка при отправке фото: {e}")


if __name__ == "__main__":
    bot.polling()