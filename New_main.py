import customtkinter as ctk
from tkinter import ttk
import sqlite3

# Создание подключения к базе данных
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor() # создаем обьеткт для выполнения SQL запроса

# Создание таблицы
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                phone_number TEXT,
                programming_skill TEXT)''')


def add_user():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    phone_number = entry_phone.get()
    programming_skill = combo_skill.get()

    cursor.execute('''INSERT INTO users (first_name, last_name, phone_number, programming_skill)
                    VALUES (?, ?, ?, ?)''', (first_name, last_name, phone_number, programming_skill))
    conn.commit()  #Подтверждаем внесение изменений

    clear_entries()
    load_data()


def edit_user():
    selected_item = table.focus()
    if selected_item:
        user_id = table.item(selected_item, 'values')[0]
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        phone_number = entry_phone.get()
        programming_skill = combo_skill.get()

        cursor.execute('''UPDATE users SET first_name=?, last_name=?, phone_number=?, programming_skill=?
                          WHERE id=?''', (first_name, last_name, phone_number, programming_skill, user_id))
        conn.commit()

        clear_entries()
        load_data()


def delete_user():
    selected_item = table.focus()
    if selected_item:
        user_id = table.item(selected_item, 'values')[0]

        cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
        conn.commit()

        load_data()


def search_users():
    keyword = entry_search.get()

    cursor.execute('''SELECT * FROM users
                      WHERE first_name LIKE ? OR last_name LIKE ? OR phone_number LIKE ?''',
                   ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    results = cursor.fetchall()

    display_data(results)


def filter_by_skill():
    selected_skill = combo_filter.get()

    if selected_skill == 'Все':
        load_data()
    else:
        cursor.execute('SELECT * FROM users WHERE programming_skill=?', (selected_skill,))
        results = cursor.fetchall()
        display_data(results)

# Загрузка/обновление  данных
def load_data():
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()

    display_data(results)


def display_data(data):
    table.delete(*table.get_children())

    for i, row in enumerate(data, start=1):
        if i % 2 == 0:
            table.insert("", ctk.END, values=row, tags=('evenrow',))
        else:
            table.insert("", ctk.END, values=row, tags=('oddrow',))

# Очистка полей
def clear_entries():
    entry_first_name.delete(0, ctk.END)
    entry_last_name.delete(0, ctk.END)
    entry_phone.delete(0, ctk.END)
    combo_skill.set('')


def on_select(event):
    selected_item = table.focus()
    if selected_item:
        values = table.item(selected_item, 'values')
        entry_first_name.delete(0, ctk.END)
        entry_first_name.insert(0, values[1])
        entry_last_name.delete(0, ctk.END)
        entry_last_name.insert(0, values[2])
        entry_phone.delete(0, ctk.END)
        entry_phone.insert(0, values[3])
        combo_skill.set(values[4])


def toggle_theme():                                                              # Изменение темы (светлая/темная)
    if switch_state.get():
        ctk.set_appearance_mode("Light")
        table.tag_configure('oddrow', background='#F0F0F0')
        table.tag_configure('evenrow', background='#FFFFFF')
        ctk.set_default_color_theme("blue")
    else:
        ctk.set_appearance_mode("Dark")
        table.tag_configure('oddrow', background='#2C2F33')
        table.tag_configure('evenrow', background='#23272A')
        ctk.set_default_color_theme("green")


# Создание главного окна
window = ctk.CTk()
window.title("Пользователи")
window.geometry("1000x600")

# Настройка темы PyDracula
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Создание элементов интерфейса
frame_add = ctk.CTkFrame(window)
frame_add.pack(pady=20)

label_first_name = ctk.CTkLabel(frame_add, text="Имя:")
label_first_name.grid(row=0, column=0, padx=5, pady=5)
entry_first_name = ctk.CTkEntry(frame_add)
entry_first_name.grid(row=0, column=1, padx=5, pady=5)

label_last_name = ctk.CTkLabel(frame_add, text="Фамилия:")
label_last_name.grid(row=0, column=2, padx=5, pady=5)
entry_last_name = ctk.CTkEntry(frame_add)
entry_last_name.grid(row=0, column=3, padx=5, pady=5)

label_phone = ctk.CTkLabel(frame_add, text="Телефон:")
label_phone.grid(row=1, column=0, padx=5, pady=5)
entry_phone = ctk.CTkEntry(frame_add)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

label_skill = ctk.CTkLabel(frame_add, text="Навык программирования:")
label_skill.grid(row=1, column=2, padx=5, pady=5)
combo_skill = ctk.CTkComboBox(frame_add, values=['Python', 'Java', 'C++'])
combo_skill.grid(row=1, column=3, padx=5, pady=5)

button_add = ctk.CTkButton(frame_add, text="Добавить", command=add_user)
button_add.grid(row=2, column=0, padx=5, pady=10)

button_edit = ctk.CTkButton(frame_add, text="Редактировать", command=edit_user)
button_edit.grid(row=2, column=1, padx=5, pady=10)

button_delete = ctk.CTkButton(frame_add, text="Удалить", command=delete_user)
button_delete.grid(row=2, column=2, padx=5, pady=10)

frame_search = ctk.CTkFrame(window)
frame_search.pack(pady=10)

label_search = ctk.CTkLabel(frame_search, text="Поиск (по имени, фамилии или номеру телефона):")
label_search.pack(side=ctk.LEFT, padx=5)
entry_search = ctk.CTkEntry(frame_search)
entry_search.pack(side=ctk.LEFT, padx=5)
button_search = ctk.CTkButton(frame_search, text="Найти", command=search_users)
button_search.pack(side=ctk.LEFT, padx=5)

frame_filter = ctk.CTkFrame(window)
frame_filter.pack(pady=10)

label_filter = ctk.CTkLabel(frame_filter, text="Фильтр по навыку программирования:")
label_filter.pack(side=ctk.LEFT, padx=5)
combo_filter = ctk.CTkComboBox(frame_filter, values=['Все', 'Python', 'Java', 'C++'])
combo_filter.pack(side=ctk.LEFT, padx=5)
combo_filter.set('Все')
button_filter = ctk.CTkButton(frame_filter, text="Применить", command=filter_by_skill)
button_filter.pack(side=ctk.LEFT, padx=5)

table = ttk.Treeview(window, columns=("ID", "Имя", "Фамилия", "Телефон", "Навык программирования"), show="headings")
table.heading("ID", text="ID")
table.heading("Имя", text="Имя")
table.heading("Фамилия", text="Фамилия")
table.heading("Телефон", text="Телефон")
table.heading("Навык программирования", text="Навык программирования")

table.column("ID", width=10)  # Установка ширины столбца "ID" в 50 пикселей
# table.column("Навык программирования",width=100)

table.tag_configure('oddrow', background='#2C2F33')
table.tag_configure('evenrow', background='#23272A')

table.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

table.bind("<<TreeviewSelect>>", on_select)

switch_state = ctk.BooleanVar()

switch_theme = ctk.CTkSwitch(window, text="Сменить тему", variable=switch_state, command=toggle_theme)
switch_theme.pack(pady=10)

load_data()

window.mainloop()

conn.close()