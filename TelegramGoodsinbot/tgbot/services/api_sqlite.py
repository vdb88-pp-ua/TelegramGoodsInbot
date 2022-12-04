# - *- coding: utf- 8 - *-
import math
import random
import sqlite3
import json
import datetime

from tgbot.data.config import PATH_DATABASE
from tgbot.utils.const_functions import get_unix, get_date, clear_html


# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict

####################################################################################################
##################################### ФОРМАТИРОВАНИЕ ЗАПРОСА #######################################
# Форматирование запроса без аргументов
def update_format(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


# Форматирование запроса с аргументами
def update_format_args(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())


########################################### ЗАПРОСЫ НА ПРОДАВЦА ########################
########################################################################################
def create_seller_request(user_id, requesttxt):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_requests "
                    "(requester, datetime, state, requesttxt) "
                    "VALUES (?, ?, ?, ?)",
                    [user_id, get_unix(), 'created', requesttxt])
        con.commit()

# Получение всех запросов продавцов
def get_all_randtgaccounts():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT * FROM storage_tgaccounts"
        return con.execute(sql).fetchall()

#Проыерка на дубли username
def check_dbfor_invited_username(username):
    print(f'Проверка на существование записи username api_sqlite.py  67')
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = f"SELECT count(*) FROM storage_tgparse "
        #sql, parameters = update_format_args(sql, kwargs)
        #return con.execute(sql, parameters).fetchone()
        #sql, parameters = update_format(sql, kwargs)
        #parameters.append(user_id)
        dbrow = []
        #count = 0
        dbrow = con.execute(sql + "WHERE state='invited' AND username = ?", [username]).fetchone()[0]
        #print(len(dbrow))
        print(dbrow)
        #count = len(dbrow)
        #print(str(dbrow['username']))
        #dbrow=dbrow.strip("(")
        #dbrow=dbrow.strip(")")
        #dbrow=dbrow.strip(",")
        #con.commit()
        print(f'Проверяем {username} в БД')
        if(dbrow>=1):
            return True
        else:
            return False

# Удаление корзины
def remove_ordersx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_orders"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

# Удаление позиций корзины
def remove_orders_itemx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_orders_items"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

#Проыерка на дубли username
def check_dbfor_username(username):
    print(f'Проверка на существование записи username api_sqlite.py  67')
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = f"SELECT count(*) FROM storage_tgparse "
        #sql, parameters = update_format_args(sql, kwargs)
        #return con.execute(sql, parameters).fetchone()
        #sql, parameters = update_format(sql, kwargs)
        #parameters.append(user_id)
        dbrow = []
        #count = 0
        dbrow = con.execute(sql + "WHERE username = ?", [username]).fetchone()[0]
        #print(len(dbrow))
        print(dbrow)
        #count = len(dbrow)
        #print(str(dbrow['username']))
        #dbrow=dbrow.strip("(")
        #dbrow=dbrow.strip(")")
        #dbrow=dbrow.strip(",")
        #con.commit()
        print(f'Проверяем {username} в БД')
        if(dbrow>=1):
            return True
        else:
            return False

# Удаление аккаунта ТГ
def remove_accountx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_tgaccounts"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

#Пользователи по статусам
def get_all_tgaccounts_states():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT source, groupname, state, count(username) FROM storage_tgparse GROUP BY source, groupname, state"
        return con.execute(sql).fetchall()


# Получение всех запросов продавцов
def get_all_avtgaccounts():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT * FROM storage_tgaccounts WHERE state='available'"
        return con.execute(sql).fetchall()

# Получение номеров по статусам
def get_all_tgaccounts_time():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT * FROM storage_tgaccounts ORDER BY date(waitfor24) ASC"
        return con.execute(sql).fetchall()

# Получение номеров по статусам
def get_all_tgaccounts():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT * FROM storage_tgaccounts"
        return con.execute(sql).fetchall()

# Получение всех запросов продавцов
def get_tgaccount_statecounts(account_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        #sql = "SELECT state, invited24, last FROM storage_tgaccounts "
        sql = "SELECT invited24 FROM storage_tgaccounts "
        return con.execute(sql + "WHERE account_id = ?", [account_id]).fetchone()

# Добавление аккаунта ТГ в БД
def add_tgacc_todb(username, user_id, access_hash, name, source, groupname, group_id, tag, state='created'):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_tgparse "
                    "(username, user_id, access_hash, name, source, groupname, group_id, tag, state) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [username, user_id, access_hash, name, source, groupname, group_id, tag, state])
        print("addok")
        con.commit()

#есть ли магазин у пользователя
def check_user_shop_exist(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT admin FROM storage_shop "
        shopadmin = con.execute(sql + "WHERE admin = ?", [user_id]).fetchone()

    return shopadmin['admin']

# Добавление аккаунта ТГ в БД
def add_account_todb(xid, xhash, xphone, invited24, state='created'):
    with sqlite3.connect(PATH_DATABASE) as con:
        datenow = datetime.datetime.now()
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_tgaccounts "
                    "(tg_api_id, tg_api_hash, phone, invited24, date, state) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    [xid, xhash, xphone, invited24, datenow, state])
        con.commit()
        #print(con.lastrowid)

# Получение всех запросов продавцов
def get_lasttgaccount():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        #sql = "SELECT state, invited24, last FROM storage_tgaccounts "
        sql = "SELECT MAX(account_id) as acc FROM storage_tgaccounts GROUP BY account_id"
        return con.execute(sql).fetchone()[0]

# Группы в ТГ
def groups_telegram():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = f"SELECT distinct group_id, groupname FROM storage_tgparse WHERE groupname != '' AND source = 'groups' ORDER BY group_id ASC" # LIMIT {start},{count}
        return con.execute(sql).fetchall()

# Пользователи группы для инвайта
def first_grouptoinvite(groupname, start, count):
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_tgparse WHERE state = 'created' AND source = 'groups' AND groupname=? ORDER BY acc_id ASC LIMIT {start},{count}"
        return con.execute(sql, [groupname]).fetchall()

# Последние 10 покупок
def first_toinvite(state, start, count):
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_tgparse WHERE state = ? AND source = 'groups' ORDER BY acc_id ASC LIMIT {start},{count}"
        return con.execute(sql, [state]).fetchall()

def firstgeo_toinvite(state, start, count):
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_tgparse WHERE state = ? AND source = 'geoparse' ORDER BY acc_id ASC LIMIT {start},{count}"
        return con.execute(sql, [state]).fetchall()
        #return con.execute(sql).fetchall()

# Редактирование запроса
def update_tgparsex(acc_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_tgparse SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(acc_id)
        con.execute(sql + "WHERE acc_id = ?", parameters)
        con.commit()

# Редактирование запроса
def update_tgaccounts(account_id, pole):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        inc = ""
        if pole == 'invited24': inc = " invited24 = invited24 + 1, last = datetime('now') "
        if pole == 'waitfor24': inc = " state = 'wait', waitfor24 = datetime('now', '+1 day') "
        if pole == 'banned': inc = " state = 'banned' "
        if pole == 'available': inc = " state = 'available', invited24 = 0 "
        sql = f"UPDATE storage_tgaccounts SET " + inc
        #sql, parameters = update_format(sql, kwargs)
        #parameters.append(account_id)
        con.execute(sql + "WHERE account_id = ?", [account_id])
        con.commit()

#удаление аккаунта
def delete_tgacc(acc_id):
    print(f"Удаляем аккаунт{acc_id}")
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_tgaccounts "
        #sql, parameters = update_format_args(sql, kwargs)
        #sql, user_id = update_format(sql, user_id)
        con.execute(sql + "WHERE account_id = ?", [acc_id])
        con.commit()

# Получение всех запросов продавцов
def get_all_requestx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT DISTINCT requester as user_id FROM storage_requests ORDER BY datetime ASC"
        return con.execute(sql).fetchall()

# Удаление запроса
def delete_requests_userx(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_requests "
        #sql, parameters = update_format_args(sql, kwargs)
        #sql, user_id = update_format(sql, user_id)
        con.execute(sql + "WHERE requester = ?", [user_id])
        con.commit()

# Редактирование запроса
def update_requestx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_requests SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + "WHERE user_id = ?", parameters)
        con.commit()


# Проверка принадлежности позиции в каталоге
def check_position_owner(user_id, position_id):
    print(f'Проверка принадлежности позиции api_sqlite.py  86')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT position_user_id FROM storage_position "
        #sql, parameters = update_format_args(sql, kwargs)
        #return con.execute(sql, parameters).fetchone()

        #sql, parameters = update_format(sql, kwargs)
        #parameters.append(user_id)
        dbuser_id = con.execute(sql + "WHERE position_id = ?", [position_id]).fetchone()
        #con.commit()
        print(f'Лот пользователя {dbuser_id} проверяем для {user_id} 97')
        if(user_id==dbuser_id['position_user_id'] or user_id==919148970): #['position_user_id']
            return True
        else:
            return False

#create_seller_request('919148970')
####################################################################################################
########################################### ЗАПРОСЫ К БД ###########################################

# Добавление пользователя
def add_userx(user_id, user_login, user_name):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_users "
                    "(user_id, user_login, user_name, user_balance, user_refill, user_date, user_unix) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, 0, 0, get_date(), get_unix()])
        con.commit()

# Получение пользователя
def get_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение админов магазинов
def get_shopadmins():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users WHERE user_role='ShopAdmin"
        return con.execute(sql).fetchall()

# Получение пользователей
def get_usersx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех пользователей
def get_all_usersx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        return con.execute(sql).fetchall()

# Получение всех пользователей
def get_top_sellersx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users WHERE user_role='ShopAdmin' AND user_balance >0 ORDER BY user_balance DESC LIMIT 0,15"
        return con.execute(sql).fetchall()



# Редактирование пользователя
def update_userx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_users SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + "WHERE user_id = ?", parameters)
        con.commit()

# Редактирование пользователя
def update_holdx(order_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_money_holds SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(order_id)
        con.execute(sql + "WHERE order_id = ?", parameters)
        con.commit()

# Удаление пользователя
def delete_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

# Получение платежных реквизитов продавца
def get_upaymentx(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        #print("|||uyo|||")
        return con.execute("SELECT * FROM storage_payment WHERE user_id = ?", [user_id]).fetchone()

def get_upaycount(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT COUNT(*) as paycount FROM storage_payment WHERE user_id = ?", [user_id]).fetchone()


def create_upayments_row(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_payment "
                    "(qiwi_login, qiwi_token, qiwi_secret, qiwi_nickname, way_form, way_number, way_nickname, user_id, yoo_token, yoo_client_id, yoo_redirect_url, yoo_acc_number, way_formy)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    ['', '', '', '', 'False', 'False', 'False', user_id, '', 0, '', 0, 'False'])
        con.commit()

# Получение платежных систем
def get_paymentx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_payment WHERE user_id=919148970"
        return con.execute(sql).fetchone()


# Редактирование платежных систем
def update_paymentx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_payment SET"
        sql, parameters = update_format(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

# Редактирование платежных систем
def update_upaymentx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_payment SET "
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + " WHERE user_id = ?", parameters)
        con.commit()

# Получение настроек
def get_settingsx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_settings"
        return con.execute(sql).fetchone()


# Редактирование настроек
def update_settingsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_settings SET"
        sql, parameters = update_format(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Добавление пополнения
def add_refillx(user_id, user_login, user_name, refill_comment, refill_amount, refill_receipt,
                refill_way, refill_date, refill_unix):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_refill "
                    "(user_id, user_login, user_name, refill_comment, refill_amount, refill_receipt, refill_way, refill_date, refill_unix) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, refill_comment, refill_amount, refill_receipt, refill_way,
                     refill_date, refill_unix])
        con.commit()


# Получение пополнения
def get_refillx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_refill"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение пополнений
def get_refillsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_refill"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех пополнений
def get_all_refillx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_refill"
        return con.execute(sql).fetchall()


# Добавление категории
def add_categoryx(category_name):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_category (category_id, category_name) VALUES (?, ?)",
                    [random.randint(1000000000, 9999999999), category_name])
        con.commit()


# Изменение категории
def update_categoryx(category_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_category SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(category_id)
        con.execute(sql + "WHERE category_id = ?", parameters)
        con.commit()


# Получение категории
def get_categoryx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_category"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение категорий
def get_categoriesx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_category"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех категорий
def get_all_shopx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_shop"
        return con.execute(sql).fetchall()

# Получение платежных реквизитов продавца
def get_my_shopx(admin):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_shop "
        #sql, parameters = update_format(sql, kwargs)
        return con.execute(sql, "WHERE admin = ?", [admin]).fetchone()

# Получение всех категорий
def get_all_categoriesx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_category"
        return con.execute(sql).fetchall()


# Удаление всех категорий
def clear_categoryx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_category"
        con.execute(sql)
        con.commit()


# Удаление категории
def remove_categoryx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_category"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Добавление категории ? позиции
def add_positionx(position_city, position_city_id, position_name, position_price, position_description, position_photo, category_id, position_user_id):
    print(f'Добавление позиции   api_sqlite_shop.py  294')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_position "
                    "(position_id, position_name, position_price, position_description, position_photo, position_date, category_id, position_city, position_city_id, position_user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [random.randint(1000000000, 9999999999), position_name, position_price, position_description,
                     position_photo, get_date(), category_id, position_city, position_city_id, position_user_id])
        con.commit()


# Изменение позиции
def update_positionx(position_id, **kwargs):
    print('Изменение позиции api_sqlite.py 306')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_position SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(position_id)
        con.execute(sql + "WHERE position_id = ?", parameters)
        con.commit()

# Получение магазина
def get_shopx(**kwargs):
    print(f'Получение магазина api_sqlite.py 318')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_shop"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение позиции
def get_positionx(**kwargs):
    print(f'Получение позиции api_sqlite.py 318')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение сообщений для пользователя
def get_user_messagesx(**kwargs):
    print(f'Получение сообющений для пользователя api_sqlite.py  367')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_messages"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Обмновление статуса сообщения
def update_orderx(order_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_messages SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(order_id)
        con.execute(sql + "WHERE order_id = ?", parameters)
        con.commit()

# Изменение корзины
def update_orderx(order_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_orders SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(order_id)
        con.execute(sql + "WHERE order_id = ?", parameters)
        con.commit()

# Изменение холда
def update_holdsx(order_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_money_holds SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(order_id)
        con.execute(sql + "WHERE order_id = ?", parameters)
        con.commit()

# Получение продавцов корзины
def get_cart_sellersx(order_id):
    print(f'Получение продавцов корзины api_sqlite.py  777')
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sellers = con.execute(f"SELECT DISTINCT owner_uid FROM storage_orders_items WHERE order_id = ?", [order_id]).fetchall()
        print(len(sellers))
        slss=''
        slsss = ''.join(str(slss) for slss in sellers)
        print(slsss)
        slsss1 = slsss.replace('(', '')
        slsss2 = slsss1.replace(')', '')
        touser_id = slsss2.replace(',', '')
        return touser_id


# Получение позиций корзины
def get_cart_positionsx(order_id):
    print(f'Получение позиций корзины  api_sqlite.py  568')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        positions = con.execute(f"SELECT * FROM storage_orders_items LEFT JOIN storage_position USING(position_id) WHERE order_id = ?", [order_id]).fetchall()
        return positions

# Получение позиций корзины
def get_order_sellers(order_id):
    print(f'Получение позиций корзины  api_sqlite.py  568')
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        positions = con.execute(f"SELECT DISTINCT owner_uid as owner_id FROM storage_orders_items WHERE order_id = ?", [order_id]).fetchall()
        return json.dumps(positions)
        #return positions


# Получение данных холдов заказа
def get_orders_holdsx(order_id):
    print(f'Получение холдов заказа {order_id} 626')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        holds = con.execute(f"SELECT * FROM storage_money_holds WHERE order_id = ?", [order_id]).fetchall()
        #return json.dumps(holds)
        return holds

# Получение позиций
def get_positionsx(**kwargs):
    print(f'Получение позиции (дубль)  api_sqlite.py  328')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение всех категорий
def get_all_positionsidx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT position_id FROM storage_position"
        return con.execute(sql).fetchall()

# Получение всех категорий
def get_all_positionsx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position"
        return con.execute(sql).fetchall()


# Удаление всех позиций
def clear_positionx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_position"
        con.execute(sql)
        con.commit()


# Удаление позиции
def remove_positionx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Добавление товара
def add_itemx(category_id, position_id, get_all_items, user_id, user_name):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory

        for item_data in get_all_items:
            if not item_data.isspace() and item_data != "":
                con.execute("INSERT INTO storage_item "
                            "(item_id, item_data, position_id, category_id, creator_id, creator_name, add_date) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?)",
                            [random.randint(1000000000, 9999999999), clear_html(item_data.strip()), position_id, category_id,
                             user_id, user_name, get_date()])
        con.commit()


# Изменение товара
def update_itemx(item_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_item SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(item_id)
        con.execute(sql + "WHERE item_id = ?", parameters)
        con.commit()

# Получение продавца заказа
def get_ordersellerx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение товара
def get_itemx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение товаров
def get_itemsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение всех товаров
def get_all_itemsx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_item"
        return con.execute(sql).fetchall()

# Получение всех моих позиций
def get_all_my_positionsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql + "WHERE position_user_id = ?", [user_id]).fetchall()

# Получение всех моих позиций
def get_all_my_positionsnx(position_user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position"
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql + " WHERE position_user_id = ?", [position_user_id]).fetchall()

# Получение всех моих товаров
def get_all_my_itemsnx(creator_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_item"
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql + " WHERE creator_id = ?", [creator_id]).fetchall()

# Получение всех моих товаров
def get_all_my_itemsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql + "WHERE creator_id = ?", [user_id]).fetchall()


# Очистка товаров
def clear_itemx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_item"
        con.execute(sql)
        con.commit()


# Удаление товаров
def remove_itemx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Покупка товаров
def buy_itemx(get_items, get_count):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        split_len, send_count, save_items = 0, 0, []

        for select_send_item in get_items:
            if send_count != get_count:
                send_count += 1
                if get_count >= 2:
                    select_data = f"{send_count}. {select_send_item['item_data']}"
                else:
                    select_data = select_send_item['item_data']

                save_items.append(select_data)
                sql, parameters = update_format_args("DELETE FROM storage_item",
                                                     {"item_id": select_send_item['item_id']})
                con.execute(sql, parameters)

                if len(select_data) >= split_len: split_len = len(select_data)
            else:
                break
        con.commit()

        split_len += 1
        get_len = math.ceil(3500 / split_len)

    return save_items, send_count, get_len

# Проверка существования заказа
def get_orderx(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        orders = con.execute(f"SELECT * FROM storage_orders WHERE user_id = ?", [user_id]).fetchone()
        return orders

# Последние 10 покупок
def get_params_orderx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_orders"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Проверка существования заказа
def get_userc_orderx(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT order_state FROM storage_orders WHERE order_state='created' AND user_id = ?"
        order = con.execute(sql, [user_id]).fetchone()
        order=json.dumps(order)
        print(order)
        return order

# Проверка существования заказа
def get_user_orderx(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        order = con.execute(f"SELECT * FROM storage_orders WHERE user_id = ?", [user_id]).fetchone()
        return order


# Создание заказа
def create_orderx(user_id, user_login, user_name, order_state, order_date, order_unix):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_orders "
                "(user_id, user_login, user_name, order_state, order_date, order_unix) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                [user_id, user_login, user_name, order_state, order_date, order_unix])
        con.commit()

# Создание холда
def create_holdx(order_id, buyer, seller, amount, validity, state):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_money_holds "
                    "(order_id, buyer, seller, amount, validity, state) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    [order_id, buyer, seller, amount, validity, state])
        con.commit()

# Добавление товара в заказ
def add_order_itemx(order_id, position_id, count, price, receipt, owner_uid):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_orders_items "
                    "(order_id, position_id, count, price, receipt, owner_uid) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    [order_id, position_id, count, price, receipt, owner_uid])
        con.commit()


# Добавление сообщения
def add_messagex(from_id, to_id, order_id, txtmessage, photo, state):
    print(f'Добавление позиции api_sqlite_shop.py  294')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_messages "
                    "(message_id, from_uid, to_uid, order_id, message, photo, state) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [random.randint(1000000000, 9999999999), from_id, to_id, order_id, txtmessage, photo, state])
        con.commit()

def get_params_messagesx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_messages"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Добавление покупки
def add_purchasex(user_id, user_login, user_name, purchase_receipt, purchase_count, purchase_price, purchase_price_one,
                  purchase_position_id, purchase_position_name, purchase_item, purchase_date, purchase_unix,
                  balance_before, balance_after):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_purchases "
                    "(user_id, user_login, user_name, purchase_receipt, purchase_count, purchase_price, purchase_price_one, purchase_position_id, "
                    "purchase_position_name, purchase_item, purchase_date, purchase_unix, balance_before, balance_after) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, purchase_receipt, purchase_count, purchase_price,
                     purchase_price_one, purchase_position_id, purchase_position_name, purchase_item, purchase_date,
                     purchase_unix, balance_before, balance_after])
        con.commit()



# Получение покупок
def get_purchasesbysellers():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT DISTINCT c.user_id FROM storage_purchases a LEFT JOIN storage_position b ON(a.purchase_position_id=b.position_id) LEFT JOIN storage_users c ON(c.user_id=b.position_user_id) WHERE c.user_id NOT NULL GROUP BY a.user_id, a.purchase_position_name"
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql).fetchall()


# Получение покупок
def get_purchasesxx2(user_id):
    #with sqlite3.connect(PATH_DATABASE) as con:
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query= f"SELECT c.user_id, a.purchase_position_name, SUM(a.purchase_count) as counts, SUM(a.purchase_price) as price FROM storage_purchases a LEFT JOIN storage_position b ON(a.purchase_position_id=b.position_id) LEFT JOIN storage_users c ON(c.user_id=b.position_user_id) WHERE c.user_id=? GROUP BY a.user_id, a.purchase_position_name"
    #result = cur.execute(query, (user_id,)).fetchall()
    result = cur.execute(query, [user_id]).fetchall()
    cur.close()
    return result

def get_purchasesx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_purchases"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

    # Получение покупок
def get_purchasesxx3(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
         #cur = conn.cursor()
        sql= f"SELECT c.user_id, a.purchase_position_name, SUM(a.purchase_count) as counts, SUM(a.purchase_price) as price FROM storage_purchases a LEFT JOIN storage_position b ON(a.purchase_position_id=b.position_id) LEFT JOIN storage_users c ON(c.user_id=b.position_user_id) WHERE c.user_id=? GROUP BY a.user_id, a.purchase_position_name"
        sql, parameters = update_format_args(sql, [user_id])
        return con.execute(sql, parameters).fetchall()


def get_purchasesxx(user_id):
    print(f'возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    #cur = conn.cursor()
    query = '''SELECT c.user_id, a.purchase_position_name, SUM(a.purchase_count) as counts, SUM(a.purchase_price) as price FROM storage_purchases a LEFT JOIN storage_position b ON(a.purchase_position_id=b.position_id) LEFT JOIN storage_users c ON(c.user_id=b.position_user_id) WHERE c.user_id=? GROUP BY a.user_id, a.purchase_position_name'''
    result = conn.execute(query, (user_id,)).fetchall()
    #cur.close()
    return result

# Получение запросов
def get_requestx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_requests"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение всех покупок
def get_all_purchasesx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_purchases"
        return con.execute(sql).fetchall()

# Получение всех покупок
def getpurchasesbysellersx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_purchases LEFT JOIN storage_position USING(user_id)"
        return con.execute(sql).fetchall()


# Последние 10 покупок
def last_purchasesx(user_id, count):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_purchases WHERE user_id = ? ORDER BY increment DESC LIMIT {count}"
        return con.execute(sql, [user_id]).fetchall()


# Создание всех таблиц для БД
def create_dbx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory

        # Создание БД с хранением данных пользователей
        if len(con.execute("PRAGMA table_info(storage_users)").fetchall()) == 12:
            print("DB was found(1/12)")
        else:
            con.execute("CREATE TABLE IF NOT EXISTS storage_users("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_login TEXT,"
                        "user_name TEXT,"
                        "user_address TEXT,"
                        "user_phone TEXT,"
                        "user_balance INTEGER,"
                        "user_refill INTEGER,"
                        "user_date TIMESTAMP,"
                        "user_unix INTEGER,"
                        "user_city TEXT,"
                        "user_geocode TEXT,"
                        "user_role TEXT,"
                        "user_city_id INTEGER)")  # Добавил город
            print("DB was not found(1/12) | Creating...")

        # Создание БД с хранением данных платежных систем
        if len(con.execute("PRAGMA table_info(storage_payment)").fetchall()) == 13:
            print("DB was found(2/12)")
        else:
            con.execute("CREATE TABLE storage_payment("
                        "qiwi_login TEXT,"
                        "qiwi_token TEXT,"
                        "qiwi_secret TEXT,"
                        "qiwi_nickname TEXT,"
                        "way_form TEXT,"
                        "way_number TEXT,"
                        "way_nickname TEXT,"
                        "way_formy TEXT,"
                        "user_id INTEGER,"
                        "yoo_token TEXT,"
                        "yoo_client_id TEXT,"
                        "yoo_redirect_url TEXT,"
                        "yoo_acc_number INTEGER)")

            con.execute("INSERT INTO storage_payment("
                        "qiwi_login, qiwi_token, qiwi_secret, qiwi_nickname, way_form, way_number, way_nickname, way_formy, yoo_token, yoo_client_id, yoo_redirect_url, yoo_acc_number) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        ['None', 'None', 'None', 'None', 'False', 'False', 'False', 'False', 'None', 'None', 'None', 'None'])
            print("DB was not found(2/12) | Creating...")

        # Создание БД с хранением настроек
        if len(con.execute("PRAGMA table_info(storage_settings)").fetchall()) == 10:
            print("DB was found(3/12)")
        else:
            con.execute("CREATE TABLE storage_settings("
                        "status_work TEXT,"
                        "status_refill TEXT,"
                        "status_buy TEXT,"
                        "misc_faq TEXT,"
                        "misc_support TEXT,"
                        "misc_bot TEXT,"
                        "misc_update TEXT,"
                        "misc_profit_day INTEGER,"
                        "misc_profit_week INTEGER,"
                        "type_trade TEXT)")

            con.execute("INSERT INTO storage_settings("
                        "status_work, status_refill, status_buy, misc_faq, misc_support, misc_bot, misc_update, misc_profit_day, misc_profit_week)"
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        ["True", "False", "False", "None", "None", "None", "False", get_unix(), get_unix()])
            print("DB was not found(3/12) | Creating...")

        # Создание БД с хранением пополнений пользователей
        if len(con.execute("PRAGMA table_info(storage_refill)").fetchall()) == 10:
            print("DB was found(4/12)")
        else:
            con.execute("CREATE TABLE storage_refill("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_login TEXT,"
                        "user_name TEXT,"
                        "refill_comment TEXT,"
                        "refill_amount INTEGER,"
                        "refill_receipt TEXT,"
                        "refill_way TEXT,"
                        "refill_date TIMESTAMP,"
                        "refill_unix INTEGER)")
            print("DB was not found(4/12) | Creating...")

        # Создание БД с хранением категорий
        if len(con.execute("PRAGMA table_info(storage_category)").fetchall()) == 3:
            print("DB was found(5/8)")
        else:
            con.execute("CREATE TABLE storage_category("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "category_id INTEGER,"
                        "category_name TEXT)")
            print("DB was not found(5/12) | Creating...")



        # Создание БД с хранением позиций
        if len(con.execute("PRAGMA table_info(storage_position)").fetchall()) == 11:
            print("DB was found(6/12)")
        else:
            con.execute("CREATE TABLE IF NOT EXISTS storage_position("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "position_id INTEGER,"
                        "position_name TEXT,"
                        "position_price INTEGER,"
                        "position_description TEXT,"
                        "position_photo TEXT,"
                        "position_date TIMESTAMP,"
                        "category_id INTEGER,"
                        "store_id INTEGER,"
                        "position_city TEXT,"
                        "position_city_id INTEGER)")
            print("DB was not found(6/12) | Creating...")

        # Создание БД с хранением товаров
        if len(con.execute("PRAGMA table_info(storage_item)").fetchall()) == 9:
            print("DB was found(7/12)")
        else:
            con.execute("CREATE TABLE IF NOT EXISTS storage_item("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "item_id INTEGER,"
                        "item_data TEXT,"
                        "position_id INTEGER,"
                        "category_id INTEGER,"
                        "shop_id INTEGER,"
                        "creator_id INTEGER,"
                        "creator_name TEXT,"
                        "add_date TIMESTAMP)")
            print("DB was not found(7/12) | Creating...")

        # # Создание БД с хранением покупок
        if len(con.execute("PRAGMA table_info(storage_purchases)").fetchall()) == 15:
            print("DB was found(8/12)")
        else:
            con.execute("CREATE TABLE IF NOT EXISTS storage_purchases("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_login TEXT,"
                        "user_name TEXT,"
                        "purchase_receipt TEXT,"
                        "purchase_count INTEGER,"
                        "purchase_price INTEGER,"
                        "purchase_price_one INTEGER,"
                        "purchase_position_id INTEGER,"
                        "purchase_position_name TEXT,"
                        "purchase_item TEXT,"
                        "purchase_date TIMESTAMP,"
                        "purchase_unix INTEGER,"
                        "balance_before INTEGER,"
                        "balance_after INTEGER)")
            print("DB was not found(8/12) | Creating...")

            if len(con.execute("PRAGMA table_info(storage_shop)").fetchall()) == 3:
                print("DB was not found(9/12) | Creating...")
            else:
            # Создание БД с хранением магазинов
                con.execute("CREATE TABLE IF NOT EXISTS storage_shop("
                            "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "shop_id INTEGER,"
                            "shop_name TEXT)")

            # # Создание БД с хранением покупок
            if len(con.execute("PRAGMA table_info(storage_purchases)").fetchall()) == 15:
                print("DB was found(10/12)")
            else:
                con.execute("CREATE TABLE IF NOT EXISTS storage_purchases("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_login TEXT,"
                        "user_name TEXT,"
                        "purchase_receipt TEXT,"
                        "purchase_count INTEGER,"
                        "purchase_price INTEGER,"
                        "purchase_price_one INTEGER,"
                        "purchase_position_id INTEGER,"
                        "purchase_position_name TEXT,"
                        "purchase_item TEXT,"
                        "purchase_date TIMESTAMP,"
                        "purchase_unix INTEGER,"
                        "balance_before INTEGER,"
                        "balance_after INTEGER)")
            print("DB was not found(10/12) | Creating...")

            if len(con.execute("PRAGMA table_info(storage_orders)").fetchall()) == 15:
                print("DB was found(11/12)")
            else:
                con.execute("CREATE TABLE IF NOT EXISTS storage_orders("
                        "order_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_login TEXT,"
                        "user_name TEXT,"
                        "order_date TEXT,"
                        "order_state INTEGER,"
                        "order_unix INTEGER,"
                        "phone TEXT,"
                        "address TEXT)")

            print("DB was not found(11/12) | Creating...")

            if len(con.execute("PRAGMA table_info(storage_orders_items)").fetchall()) == 7:
                print("DB was found(12/12)")
            else:
                con.execute("CREATE TABLE IF NOT EXISTS storage_orders_items("
                        "order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "order_id INTEGER,"
                        "position_id INTEGER,"
                        "user_name TEXT,"
                        "count INTEGER,"
                        "price INTEGER,"
                        "receipt INTEGER)")

            print("DB was not found(12/12) | Creating...")


        con.commit()


# ================================================================================================================
# ==========                  Новые функции 11.08.22                            ==================================

# возвращает город пользователя и координаты
def get_city_user(user_id):
    print(f'возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select user_city_id from storage_users where user_id = ?'''
    result = cur.execute(query, (user_id,)).fetchone()
    cur.close()
    return result

# возвращает город пользователя и координаты
def get_city_user2(user_id):
    print(f'возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select user_city, user_geocode, user_city_id from storage_users where user_id = ?'''
    result = cur.execute(query, (user_id,)).fetchone()
    cur.close()
    return result


# возвращает город пользователя и координаты
def get_citytext_user(user_id):
    print(f'возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select user_city from storage_users where user_id = ?'''
    result = cur.execute(query, (user_id,)).fetchone()
    cur.close()
    return result

# позиции по городу и категории
def get_position_on_city(category_id, city):
    print(f'позиции по городу и категории api_sqlite.py 686')
    if city is None:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position where category_id = ?'''
        result = cur.execute(query, (category_id,)).fetchall()
        cur.close()
        return result
    else:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position where category_id = ? and position_city_id = ?'''
        items = [category_id, city]
        result = cur.execute(query, items).fetchall()
        cur.close()
        return result


# категории в городе
def get_category_in_city(city_id):
    if city_id is None:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select distinct c.category_id, c.category_name
            from storage_category c join storage_position p on c.category_id=p.category_id order by c.category_name asc'''
        result = cur.execute(query).fetchall()
        return result

    else:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select distinct c.category_id, c.category_name
                from storage_category c join storage_position p on c.category_id=p.category_id where position_city_id = ? order by c.category_name asc'''
        result = cur.execute(query, (city_id,)).fetchall()
        return result

