__connection = None
import sqlite3
import main
from loguru import logger

@logger.catch
def get_connection():
    """Функция подключения к базе данных"""
    global __connection
    if __connection is None:
        __connection = sqlite3.connect("currency.db", check_same_thread=False)
        __connection = sqlite3.connect("codes_and_currency.db", check_same_thread=False)
    return __connection


@logger.catch
def init_db(force: bool = False):
    """Функция создания БД"""
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute("DROP TABLE IF EXISTS currency")
        c.execute("DROP TABLE IF EXISTS codes_and_currency")

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS currency (
        id INTEGER PRIMARY KEY,
        date TEXT,
        units INTEGER,
        course REAL
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS codes_and_currency (
        id INTEGER PRIMARY KEY,
        code TEXT,
        title TEXT
        )
        """
    )

    conn.commit()


@logger.catch
def add_currency_data():
    """ Функция удаляет имеющиеся коды и имена валют, получает новые
    если такие имеются """
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM codes_and_currency")

    values, titles = main.get_currency_code_and_title()
    x = dict(zip(values, titles))
    for value, title in x.items():
        c.execute(
            "INSERT INTO codes_and_currency (code, title)\
            VALUES (?, ?);", (str(value), str(title))
        )
    conn.commit()


@logger.catch
def get_currency_list():
    """ Функция отдаёт список существующих валют """
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT code, title\
        FROM codes_and_currency\
        ORDER BY title"
    )
    (choose) = c.fetchall()
    return choose


@logger.catch
def add_currency_info(currency):
    """ Функция  """
    conn = get_connection()
    c = conn.cursor()
    currency_data = main.get_currency_data(currency)
    
    # for i in currency_data:
    #     print(i)

    # c.execute(
    #     "SELECT code, title\
    #     FROM codes_and_currency\
    #     ORDER BY title"
    # )



