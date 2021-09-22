import sqlite3

from loguru import logger
from xlsxwriter.workbook import Workbook
from pathlib import Path

import main

__connection = None


@logger.catch
def get_connection():
    """Функция подключения к базе данных"""
    global __connection
    if __connection is None:
        __connection = sqlite3.connect("currency.db", check_same_thread=False)
    return __connection


@logger.catch
def init_db(force: bool = False):
    """Функция создания БД"""
    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute("DROP TABLE IF EXISTS currency")

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
    """Функция удаляет имеющиеся коды и имена валют, получает новые
    если такие имеются"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM codes_and_currency")

    values, titles = main.get_currency_code_and_title()
    x = dict(zip(values, titles))
    for value, title in x.items():
        c.execute(
            "INSERT INTO codes_and_currency (code, title)\
            VALUES (?, ?);",
            (str(value), str(title)),
        )
    conn.commit()


@logger.catch
def get_currency_list():
    """Функция отдаёт список существующих валют"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM currency")
    c.execute(
        "SELECT code, title\
        FROM codes_and_currency\
        ORDER BY title"
    )
    choose_data = c.fetchall()
    codes_and_titles = []
    for elem in choose_data:
        codes_and_titles.append((" - ".join(elem)))
    return codes_and_titles


@logger.catch
def add_currency_info(currency):
    """Функция собирает все данные о заданной валюте и заносит в БД"""
    conn = get_connection()
    c = conn.cursor()
    currency_data = main.get_currency_data(currency)

    for elem in currency_data:
        c.execute(
            "INSERT INTO currency (date, units, course)\
                VALUES (?, ?, ?);",
            (elem[0], elem[1], elem[2]),
        )
    conn.commit()


@logger.catch
def export_db_to_excel(currency):
    """Функция создаёт папку и сохраняет в неё таблицу с данными о курсах"""
    conn = get_connection()
    c = conn.cursor()
    Path("Tables").mkdir(parents=True, exist_ok=True)

    title = c.execute(
        "SELECT title\
        FROM codes_and_currency WHERE code = '{}'".format(
            currency
        )
    )
    currency_name = "".join(title.fetchone())
    workbook = Workbook(f"Tables/{currency_name}.xlsx")
    worksheet = workbook.add_worksheet()

    c.execute("SELECT * FROM currency")
    mysel = c.execute("SELECT * FROM currency ")
    for i, row in enumerate(mysel):
        for j, value in enumerate(row):
            worksheet.write(i, j, row[j])
    workbook.close()
    logger.info("The script has completed the work")