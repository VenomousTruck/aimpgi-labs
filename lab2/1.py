import sys  # модуль для работы с системными путями
from PySide6.QtWidgets import (
    QApplication,  # управление графическим интерфейсом и основными настройками
    QMainWindow,  # главное окно приложения
    QMenu,  # виджет меню
    QLabel,  # отображение текста или изображений
    QVBoxLayout,  # вертикальное расположение виджета
    QWidget,  # базовый класс для виджетов
    QLineEdit,  # поле ввода текста
    QPushButton,  # кнопка для запуска действия по умолчанию
    QMessageBox  # окно информации для пользователя
)
# создание элементов меню
from PySide6.QtGui import QAction


# Класс с информацией об авторе и версии приложения
class AppInfo:
    author = ""
    version = "1.0.0-alpha"


# Класс главного окна приложения
class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # вызов конструктора родительского класса
        self.init_ui()  # инициализация пользовательского интерфейса

    def init_ui(self):
        menubar = self.menuBar()  # создание строки меню

        # Создание пунктов меню Файл
        file_menu = menubar.addMenu('Файл')
        edit_submenu = QAction('Редактирование', self)
        edit_submenu.triggered.connect(self.toggle_elements_visibility)
        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(edit_submenu)
        file_menu.addAction(exit_action)

        # Создание пунктов меню Справка
        help_menu = menubar.addMenu('Справка')
        author_action = QAction('Автор программы', self)
        author_action.triggered.connect(self.show_author_info)
        about_action = QAction('О программе', self)
        about_action.triggered.connect(self.show_program_info)
        help_menu.addAction(author_action)
        help_menu.addAction(about_action)

        # Создание центрального виджета главного окна
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Основной интерфейс, размещенный по вертикали
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Отображение текста автора программы
        self.author_label = QLabel('Автор программы:', self)
        layout.addWidget(self.author_label)

        # Отображение поля для ввода имени автора
        self.author_input = QLineEdit(self)
        layout.addWidget(self.author_input)

        # Кнопка для сохранения автора программы
        self.save_button = QPushButton('Сохранить', self)
        self.save_button.clicked.connect(self.save_author)
        layout.addWidget(self.save_button)

        # Настройка геометрии и заголовка программы
        self.setGeometry(700, 500, 400, 200)
        self.setWindowTitle('Лабораторная работа 1')

        self.show()

    def show_author_info(self):
        QMessageBox.information(self, 'Информация об авторе', f'Автор программы: {AppInfo.author}')

    def show_program_info(self):
        QMessageBox.information(self, 'О программе', f'Лабораторная работа 1\nВерсия: {AppInfo.version}\n')

    def save_author(self):
        new_author = self.author_input.text()
        AppInfo.author = new_author
        if AppInfo.author == '':
            QMessageBox.information(self, 'Инфо', 'Введите имя')
        else:
            QMessageBox.information(self, 'Инфо', 'Успешно')

    # Итерация по всем дочерним виджетам центрального виджета
    # Проверка, является ли текущий виджет экземпляром одного из следующих классов:
    # QLabel, QLineEdit или QPushButton.
    # Такая проверка позволяет изменять видимость только для этих типов виджетов, игнорируя другие.
    # Если виджет является экземпляром QLabel, QLineEdit или QPushButton,
    # вызывается метод setHidden для этого виджета. Этот метод устанавливает видимость виджета.
    def toggle_elements_visibility(self):
        for widget in self.central_widget.children():
            if isinstance(widget, (QLabel, QLineEdit, QPushButton)):
                widget.setHidden(not widget.isHidden())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = AppMainWindow()

    sys.exit(app.exec())
