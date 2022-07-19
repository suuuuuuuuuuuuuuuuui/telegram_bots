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
    print(login,password)
    cur.execute('INSERT INTO accounts VALUES(?, ?)', (login, password))
    base.commit()


async def delete_all_accounts(message):
    pass


async def sql_read_info(message):
    global base, cur
    try:
        acc_count = 0
        accounts = ''

        for info in cur.execute('SELECT * FROM accounts').fetchall():
            acc_count += 1

            acc_count += f'\nАккаунт{acc_count}\nЛогин: {info[0]}\nПароль: {info[1]}'
        await bot.send_message(message.from_user.id, accounts)
    except:
        await bot.send_message(message.from_user.id, 'добавленных аккаунтов нет')




