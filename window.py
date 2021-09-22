from tkinter import *

import db_connect

window = Tk()
window.title("Добро пожаловать в приложение 'CER parser'")
window.geometry("800x400+600+300")
window.resizable()
window.iconbitmap("idid.ico")

title = Label(
    window,
    text=(
        "Выберите код валюты из списка и введите его.\n"
        "После нажатия на кнопку, будет сформирована "
        "таблица с данными в папке 'Tables'"
    ),
    bg="white",
    font=40,
)
title.pack()

frame_bottom = Frame(window, bg="#ffb700", bd=3)
frame_bottom.place(relx=0.15, rely=0.55, relwidth=0.7, relheight=0.25)

help_text = Label(frame_bottom, text="Введите код", bg="white")
help_text.pack()

entry = Entry(frame_bottom, bg="white", font=30, width=15)
entry.pack()

choose_currency = db_connect.get_currency_list()
frame_top = Frame(window, bg="#ffb700", bd=5)
frame_top.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.3)

scrollbar = Scrollbar(frame_top)
scrollbar.pack(side=RIGHT, fill=Y)

choose_currency_box = Listbox(
    frame_top, yscrollcommand=scrollbar.set, width=50
)
choose_currency_box.pack(side=TOP, fill=Y)
scrollbar.config(command=choose_currency_box.yview)


for code_and_title in choose_currency:
    choose_currency_box.insert(END, code_and_title)


def run():
    db_connect.init_db()
    db_connect.add_currency_data()
    code = entry.get()
    db_connect.add_currency_info(code)
    db_connect.export_db_to_excel(code)


btn = Button(
    frame_bottom, text="Получить данные и создать таблицу", command=run, bd=5
)
btn.pack()

window.mainloop()
