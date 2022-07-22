import sqlite3 as sq
from sawe_login_passworld_bot.login_password_bot import dp, bot


def sql_start():
    global base,cur
    base = sq.connect('info.db')
    cur = base.cursor()
    if base:
        print('\nData base connected')
    base.execute('CREATE TABLE IF NOT EXISTS accounts(login PRIMARY KEY, password TEXT)')
    base.commit()


async def sql_add_account(login, password):
    print(login, password)
    cur.execute('INSERT INTO accounts VALUES(?, ?)', (login, password))
    base.commit()


async def delete_all_accounts(message):
    global cur, base
    try:
        sql_update_query = 'DELETE from accounts'
        cur.execute(sql_update_query)
        await bot.send_message(message.from_user.id, 'все аккаунты удалены')
    except sq.Error as erorr:
        await bot.send_message(message.from_user.id, f'произошла ошибка в работе с базой данных:\n{erorr}')



async def sql_read_info(message):
    global base, cur
    try:
        acc_count = 0
        accounts = ''

        for info in cur.execute('SELECT * FROM accounts').fetchall():
            acc_count += 1

            accounts += f'\nАккаунт{acc_count}\nЛогин: {info[0]}\nПароль: {info[1]}'
        await bot.send_message(message.from_user.id, accounts)
    except Exception as ex:
        print(repr(ex))
        await bot.send_message(message.from_user.id, 'добавленных аккаунтов нет')


async def delete_account_db(message, login):
    global cur, base
    try:
        count = 0
        for log in cur.execute('SELECT * FROM accounts').fetchall():
            if log[0] == login:
                sql_update_query = 'DELETE from accounts where login = ?'
                cur.execute(sql_update_query, (login,))
                base.commit()
                await bot.send_message(message.from_user.id, f'аккаунт [{login}] успешно удален')
                count += 1
        if count == 0:
            await bot.send_message(message.from_user.id, f'аккаунт [{login}] не найден')

    except sq.Error as error:
        await bot.send_message(message.from_user.id, f'ошибка при работе с базой данных {error}')

