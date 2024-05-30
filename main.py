# Устаревшая бета версия программы блокнот .
# Ее разработка была прекращена в связи с устаревшей библиотекой GUI ,
# а так же существенным отличием кода для консольного взаимодействия и для взаимодействия с интерфейсом.


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QInputDialog, QMessageBox, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для заметок")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        buttons = [
            ("Добавить", self.add_note, "#4CAF50"),
            ("Просмотреть", self.list_note, "#2196F3"),
            ("Удалить", self.delete_note, "#f44336"),
            ("Редактировать", self.edit_note, "#FF9800")
        ]

        for text, slot, color in buttons:
            button = QPushButton(text)
            button.clicked.connect(slot)
            button.setStyleSheet(f"QPushButton {{ background-color: {color}; color: white; font-weight: bold; padding: 10px; }}")
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

        self.input_fields = {
            "name": ("Имя:", QLineEdit()),
            "last_name": ("Фамилия:", QLineEdit()),
            "phone": ("Номер телефона:", QLineEdit()),
            "programming": ("Умеет программировать?", QLineEdit())
        }

        input_layout = QGridLayout()
        input_layout.setSpacing(10)

        for i, (field, (label, input_widget)) in enumerate(self.input_fields.items()):
            label_widget = QLabel(label)
            input_layout.addWidget(label_widget, i, 0)
            input_layout.addWidget(input_widget, i, 1)

        layout.addLayout(input_layout)

        self.notes_display = QTextEdit()
        self.notes_display.setReadOnly(True)
        layout.addWidget(self.notes_display)

    def add_note(self):
        num = int(self.get_last_note_number()) + 1
        data = {field: input_widget.text() for field, (_, input_widget) in self.input_fields.items()}
        self.save_note(num=num, **data)
        self.clear_inputs()

    def list_note(self, num=0):
        with open('note.txt', 'r', encoding='utf-8') as file:
            all_notes = file.readlines()
            if num == 0:
                self.notes_display.clear()
                self.notes_display.append("".join(all_notes))
            else:
                note = all_notes[num - 1]
                QMessageBox.information(self, "Удаление записи", f'Строка {note} УДАЛЕНА')
                all_notes.pop(num - 1)
                self.notes_display.clear()
                self.notes_display.append("".join(all_notes))
                return all_notes

    def delete_note(self):
        self.list_note()
        num, ok = QInputDialog.getInt(self, "Удаление записи", "Какую строку удаляем?")
        if ok:
            res = self.list_note(num=num)
            with open("note.txt", "w", encoding='utf-8') as file:
                file.writelines(res)
            self.renum()

    def renum(self, file_name='note.txt'):
        with open(file_name, "r+", encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)
            for i, line in enumerate(lines, start=1):
                parts = line.split(',')
                parts[0] = str(i)
                new_line = ','.join(parts)
                file.write(new_line)
            file.truncate()

    def edit_note(self):
        self.list_note()
        num, ok = QInputDialog.getInt(self, "Редактирование записи", "Какую строку редактируем?")
        if ok:
            with open('note.txt', "r+", encoding='utf-8') as file:
                lines = file.readlines()
                line = lines[num - 1]
                parts = line.strip().split(',')
                for i, (field, (_, input_widget)) in enumerate(self.input_fields.items(), start=1):
                    input_widget.setText(parts[i])
                if QMessageBox.question(self, "Редактирование записи", "Сохранить изменения?") == QMessageBox.Yes:
                    new_data = [input_widget.text() for _, input_widget in self.input_fields.values()]
                    new_line = f"{num},{','.join(new_data)}\n"
                    lines[num - 1] = new_line
                    file.seek(0)
                    file.writelines(lines)
                    file.truncate()
                    self.clear_inputs()

    def save_note(self, num='1', **kwargs):
        data = {field: kwargs.get(field, 'Не указано') for field in self.input_fields}
        with open('note.txt', 'a', encoding='utf-8') as file:
            file.write(f"{num},{','.join(data.values())}\n")

    def get_last_note_number(self):
        with open('note.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return lines[-1].split(',')[0] if lines else '0'

    def clear_inputs(self):
        for _, input_widget in self.input_fields.values():
            input_widget.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    note_app = NoteApp()
    note_app.show()
    sys.exit(app.exec_())
