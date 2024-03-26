import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidget,
    QLabel,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QComboBox,
    QSpacerItem,
    QTextBrowser
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setFixedSize(300, 650)

        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # Шрифт
        font = QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(12)

        # Тип линии
        line_type_layout = QVBoxLayout()

        self.line_type_label = QLabel('Тип линии')
        self.line_type_label.setAlignment(Qt.AlignCenter)
        self.line_type_label.setFont(font)
        self.line_type_edit = QLineEdit()
        self.line_type_edit.setPlaceholderText('Введите тип линии')
        self.line_type_button = QPushButton('Добавить')
        self.line_type_button.clicked.connect(self.add_line_type)
        self.line_type_button.setFixedSize(285, 50)
        self.line_type_button.setFont(font)

        line_type_layout.addWidget(self.line_type_label)
        line_type_layout.addWidget(self.line_type_edit)
        line_type_layout.addWidget(self.line_type_button)
        line_type_layout.setAlignment(Qt.AlignCenter)

        main_layout.addLayout(line_type_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 30))  # Это добавляет вертикальный отступ в 20 пикселей

        # Список типов линий
        line_types_layout = QVBoxLayout()

        self.line_types_label = QLabel('Список типов для линии')
        self.line_types_label.setAlignment(Qt.AlignCenter)
        self.line_types_label.setFont(font)
        self.line_types_list = QListWidget()

        line_types_layout.addWidget(self.line_types_label)
        line_types_layout.addWidget(self.line_types_list)

        main_layout.addLayout(line_types_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 30))  # Это добавляет вертикальный отступ в 20 пикселей

        # Список геометрических фигур
        shape_types_layout = QVBoxLayout()

        self.shape_types_label = QLabel('Список видов геометрических фигур')
        self.shape_types_label.setAlignment(Qt.AlignCenter)
        self.shape_types_label.setFont(font)
        self.shape_types_combo = QComboBox(self)
        self.shape_types_combo.insertItems(0, ['Круг', 'Квадрат', 'Прямоугольник'])

        shape_types_layout.addWidget(self.shape_types_label)
        shape_types_layout.addWidget(self.shape_types_combo)

        main_layout.addLayout(shape_types_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 30))  # Еще один вертикальный отступ

        # Выбор
        choice_layout = QVBoxLayout()

        self.choice_label = QLabel('Ваш выбор')
        self.choice_label.setAlignment(Qt.AlignCenter)
        self.choice_label.setFont(font)
        self.choice_edit = QTextBrowser()
        self.choice_edit.setFixedSize(285, 100)
        self.choice_button = QPushButton('Посмотреть')
        self.choice_button.setFont(font)
        self.choice_button.setFixedSize(285, 50)
        self.choice_button.clicked.connect(self.display_selection)

        choice_layout.addWidget(self.choice_label)
        choice_layout.addWidget(self.choice_edit)
        choice_layout.addWidget(self.choice_button)

        main_layout.addLayout(choice_layout)

        self.setGeometry(800, 300, 520, 720)
        self.setWindowTitle('Лабораторная работа 2')
        self.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        rect = self.rect()
        widget_rect = self.central_widget.rect()
        widget_rect.moveCenter(rect.center())
        self.central_widget.setGeometry(widget_rect)

    def add_line_type(self):
        line_type = self.line_type_edit.text()
        if line_type:
            self.line_types_list.addItem(line_type)
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Введите тип линии')
            return

    def display_selection(self):
        selected_line_type = self.line_types_list.currentItem()
        if selected_line_type is None:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите тип линии. Добавьте, если отсутствуют')
            return
        else:
            selected_shape_type = self.shape_types_combo.currentText()
            display_text = (f'Тип линии: {selected_line_type.text()}\n'
                            f'Вид геометрической фигуры: {selected_shape_type}')
            self.choice_edit.setText(display_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = AppMainWindow()

    sys.exit(app.exec())
