# Последний релиз программы блокнот ,нет багов ,оптимизированный код,красивый интерфейс.

import customtkinter as ctk
from tkinter import ttk


class Contact:
    def __init__(self, first_name, last_name, phone_number, can_program):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.can_program = can_program


class NotepadApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Записная книжка")
        self.geometry("850x400")

        self.contacts = []
        self.load_contacts()

        self.create_widgets()

    def create_widgets(self):
        self.table = ttk.Treeview(self, columns=("Имя", "Фамилия", "Номер телефона", "Умеет программировать"),
                                  show="headings")
        self.table.heading("Имя", text="Имя")
        self.table.heading("Фамилия", text="Фамилия")
        self.table.heading("Номер телефона", text="Номер телефона")
        self.table.heading("Умеет программировать", text="Умеет программировать")
        self.table.pack(fill="both", expand=True)

        self.display_contacts()

        self.add_button = ctk.CTkButton(self, text="Добавить", command=self.add_contact)
        self.add_button.pack(side="left", padx=70, pady=10)

        self.edit_button = ctk.CTkButton(self, text="Редактировать", command=self.edit_contact)
        self.edit_button.pack(side="left", padx=70, pady=10)

        self.delete_button = ctk.CTkButton(self, text="Удалить", command=self.delete_contact)
        self.delete_button.pack(side="left", padx=70, pady=10)

    def display_contacts(self):
        self.table.delete(*self.table.get_children())
        for contact in self.contacts:
            self.table.insert("", "end", values=(
            contact.first_name, contact.last_name, contact.phone_number, "Да" if contact.can_program else "Нет"))

    def add_contact(self):
        add_window = ctk.CTkToplevel(self)
        add_window.title("Добавить контакт")
        add_window.geometry("400x250")

        first_name_label = ctk.CTkLabel(add_window, text="Имя:")
        first_name_label.pack()
        first_name_entry = ctk.CTkEntry(add_window)
        first_name_entry.pack()

        last_name_label = ctk.CTkLabel(add_window, text="Фамилия:")
        last_name_label.pack()
        last_name_entry = ctk.CTkEntry(add_window)
        last_name_entry.pack()

        phone_label = ctk.CTkLabel(add_window, text="Номер телефона:")
        phone_label.pack()
        phone_entry = ctk.CTkEntry(add_window)
        phone_entry.pack()

        can_program_var = ctk.BooleanVar()
        can_program_checkbox = ctk.CTkCheckBox(add_window, text="Умеет программировать", variable=can_program_var)
        can_program_checkbox.pack()

        def save_contact():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            phone_number = phone_entry.get()
            can_program = can_program_var.get()

            contact = Contact(first_name, last_name, phone_number, can_program)
            self.contacts.append(contact)
            self.save_contacts()
            self.display_contacts()

            add_window.destroy()

        save_button = ctk.CTkButton(add_window, text="Сохранить", command=save_contact)
        save_button.pack(pady=10)

    def edit_contact(self):
        selected_item = self.table.selection()
        if selected_item:
            index = self.table.index(selected_item)
            contact = self.contacts[index]

            edit_window = ctk.CTkToplevel(self)
            edit_window.title("Редактировать контакт")
            edit_window.geometry("400x250")

            first_name_label = ctk.CTkLabel(edit_window, text="Имя:")
            first_name_label.pack()
            first_name_entry = ctk.CTkEntry(edit_window)
            first_name_entry.insert(0, contact.first_name)
            first_name_entry.pack()

            last_name_label = ctk.CTkLabel(edit_window, text="Фамилия:")
            last_name_label.pack()
            last_name_entry = ctk.CTkEntry(edit_window)
            last_name_entry.insert(0, contact.last_name)
            last_name_entry.pack()

            phone_label = ctk.CTkLabel(edit_window, text="Номер телефона:")
            phone_label.pack()
            phone_entry = ctk.CTkEntry(edit_window)
            phone_entry.insert(0, contact.phone_number)
            phone_entry.pack()

            can_program_var = ctk.BooleanVar(value=contact.can_program)
            can_program_checkbox = ctk.CTkCheckBox(edit_window, text="Умеет программировать", variable=can_program_var)
            can_program_checkbox.pack()

            def save_changes():
                contact.first_name = first_name_entry.get()
                contact.last_name = last_name_entry.get()
                contact.phone_number = phone_entry.get()
                contact.can_program = can_program_var.get()

                self.save_contacts()
                self.display_contacts()

                edit_window.destroy()

            save_button = ctk.CTkButton(edit_window, text="Сохранить", command=save_changes)
            save_button.pack(pady=10)

    def delete_contact(self):
        selected_item = self.table.selection()
        if selected_item:
            index = self.table.index(selected_item)
            del self.contacts[index]
            self.save_contacts()
            self.display_contacts()

    def load_contacts(self):
        try:
            with open("contacts.txt", "r",encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(",")
                    first_name, last_name, phone_number, can_program = data
                    contact = Contact(first_name, last_name, phone_number, can_program == "True")
                    self.contacts.append(contact)
        except FileNotFoundError:
            pass

    def save_contacts(self):
        with open("contacts.txt", "w",encoding="utf-8") as file:
            for contact in self.contacts:
                file.write(f"{contact.first_name},{contact.last_name},{contact.phone_number},{contact.can_program}\n")


if __name__ == "__main__":
    app = NotepadApp()
    app.mainloop()