import datetime as dt

from bs4 import BeautifulSoup
from loguru import logger
from requests import get

import db_connect

DATE_FORMAT = DATE_FORMAT = "%d.%m.%Y"
START_DATE = "01.07.1992"
END_DATE = dt.date.today().strftime(DATE_FORMAT)


MAIN_URL = "http://www.cbr.ru/currency_base/dynamics/"
URL_WITH_CURRENCY_DATA = (
    "http://www.cbr.ru/currency_base/dynamics/"
    "?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery."
    "date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ="
)

logger.add(
    "bot_debug.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
)


@logger.catch
def get_currency_data(currency):
    """Получение даты, кол-ва, курса валюты из html страницы"""
    try:
        response = get(
            (
                URL_WITH_CURRENCY_DATA
                + currency
                + "&UniDbQuery.From="
                + START_DATE
                + "&UniDbQuery.To="
                + END_DATE
            )
        )
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find_all("td")  # td - tag in html
        if not data:
            logger.info("There is no data for this period")
        else:
            values = [elem.text for elem in data]
            values.pop(0)

            currency_data = []
            values_len = len(values)
            len_new_arr = values_len // 3
            last_elem = values_len % 3
            counter = 0
            for _ in range(len_new_arr):
                currency_data.append(values[counter:counter + 3])
                counter += 3
            if last_elem != 0:
                currency_data.append(values[-last_elem:])
            return currency_data
    except Exception as error:
        logger.error(error)


@logger.catch
def get_currency_code_and_title():
    """Получение кода валюты и названия валюты из html страницы"""
    response = get(MAIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find_all("div", class_="request_block")
    values = []
    titles = []
    for element in data:  # получаем код и название валюты из html
        div_in_data = element.find_all("div", class_="select")
        for elem in div_in_data:
            elem_in_option = elem.find_all("option")
            for el in elem_in_option:
                value_and_title = el.get("value")
                values.append(value_and_title)
                titles.append("".join(el.text).strip())
    return values, titles


if __name__ == "__main__":
    db_connect.init_db()
    db_connect.add_currency_data()

    print(
        "Добро пожаловать!\n"
        "Выберите номер интересующей Вас валюты и введите его."
    )
    print()
    print("*" * 55)
    choose_currency = db_connect.get_currency_list()
    print(*choose_currency, sep='\n ')
    print("*" * 55)
    print()
    currency = input("Введите номер валюты: ")

    logger.info("Script started work")
    db_connect.add_currency_info(currency)
    db_connect.export_db_to_excel(currency)
