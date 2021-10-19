# CER_parser

### Пасрер валюты с сайта Банка России http://www.cbr.ru/currency_base/dynamics/

### Что умеет:
- Создаёт таблицу, которая сохраняет в себя данные курса валют, начиная с 1992г.(Если данные существуют)
- Создаёт таблицу, которая сохраняет коды валют и названия всех существующих.
- При запросе курса конкретной валюты создаёт таблицу excel в которую добавляет все полученные данные из БД.

### Быстрый запуск:
- Клонировать репозиторий https://github.com/Stevinel/CER_parser
- Запустить файл window.exe

### Установка:
- Клонировать репозиторий https://github.com/Stevinel/CER_parser
- Установить виртуальное оружение
- Установить зависимости (requirements.txt)
- Сделать миграции
- Раскомментить name == main
- Запустить main.py

### Стек:
- Python
- BeautifulSoup
- Loguru
- Tkinter
- Sqlite3
- Xlsxwriter

### Дополнительная информация
- Сделано специально без запроса к API банка в качестве тестового задания

### Изображение
![image](https://user-images.githubusercontent.com/72396348/134424474-6231d6e1-a54f-4571-98a3-07ff90ea8b1f.png)
