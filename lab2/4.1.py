import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class InputDialog(QDialog):
    def __init__(self):
        super().__init__()

        # устанавливаем вертикальный лейаут
        layout = QVBoxLayout()

        self.type_label = QLabel("Тип объекта:")
        self.type_edit = QLineEdit()
        self.type_edit.setReadOnly(True)
        # self.type_button = QPushButton("Выбрать тип")
        # self.type_button.clicked.connect(self.select_type)

        # Вводим координаты, ширину и высоту
        self.x_label = QLabel("X:")
        self.x_edit = QLineEdit()
        self.y_label = QLabel("Y:")
        self.y_edit = QLineEdit()
        self.width_label = QLabel("Ширина:")
        self.width_edit = QLineEdit()
        self.height_label = QLabel("Высота:")
        self.height_edit = QLineEdit()

        # добавляем все виджеты в главное окно приложения
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_edit)
        # layout.addWidget(self.type_button)
        layout.addWidget(self.x_label)
        layout.addWidget(self.x_edit)
        layout.addWidget(self.y_label)
        layout.addWidget(self.y_edit)
        layout.addWidget(self.width_label)
        layout.addWidget(self.width_edit)
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_edit)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    # метод подтверждения выбора типа
    # def select_type(self):
    #     types = ["Точка", "Линия", "Прямоугольник", "Эллипс"]
    #     type_item, ok = QInputDialog.getItem(self, "Выбор типа объекта", "Выберите тип объекта:", types, 0, False)
    #     if ok and type_item:
    #         self.type_edit.setText(type_item)


# Создаем класс для отрисовки графических элементов
class GraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()

        # создаем область для управления объектами, которые будут отображаться
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)  # добавляем сглаживание

    # метод для изображения точки
    def draw_point(self, x, y):
        self.scene.addEllipse(x - 2, y - 2, 4, 4, pen=QPen())

    # метод для изображения линии
    def draw_line(self, x1, y1, x2, y2):
        self.scene.addLine(x1, y1, x2, y2)

    # метод для изображения прямоугольника
    def draw_rectangle(self, x, y, width, height):
        self.scene.addRect(x, y, width, height)

    # метод для изображения окружности
    def draw_ellipse(self, x, y, width, height):
        self.scene.addEllipse(x, y, width, height)


class MainWindow(QMainWindow):
    def __init__(self):
        # вызов конструктора базового класса
        super().__init__()

        self.view = GraphicsView()
        self.setCentralWidget(self.view)

        self.create_actions()
        self.create_menus()

    # метод для создания действий "создать" и "выход"
    def create_actions(self):
        self.create_action = QAction("Создать", self)
        self.create_action.triggered.connect(self.create_object)

        self.exit_action = QAction("Выход", self)
        self.exit_action.triggered.connect(self.close)

    # метод для создания меню
    def create_menus(self):
        # с подменю
        file_menu = self.menuBar().addMenu("Файл")
        create_submenu = QMenu("Создать", self)
        file_menu.addMenu(create_submenu)

        # используем лямбда-функции для вызова соответствующих методов создания объектов
        point_action = QAction("Точка", self)
        point_action.triggered.connect(lambda: self.create_object("Точка"))
        create_submenu.addAction(point_action)

        line_action = QAction("Линия", self)
        line_action.triggered.connect(lambda: self.create_object("Линия"))
        create_submenu.addAction(line_action)

        rectangle_action = QAction("Прямоугольник", self)
        rectangle_action.triggered.connect(lambda: self.create_object("Прямоугольник"))
        create_submenu.addAction(rectangle_action)

        ellipse_action = QAction("Эллипс", self)
        ellipse_action.triggered.connect(lambda: self.create_object("Эллипс"))
        create_submenu.addAction(ellipse_action)

        file_menu.addAction(self.exit_action)

    # метод для создания геометрических объектов
    def create_object(self, type=None):
        dialog = InputDialog()

        # Определяем тип создаваемого объекта
        if type:
            dialog.type_edit.setText(type)
            dialog.type_edit.setReadOnly(True)

        # Если аргумент type был передан, он устанавливает тип объекта в соответствующее
        # поле диалогового окна и блокирует его для редактирования.
        if dialog.exec() == QDialog.Accepted:
            x = int(dialog.x_edit.text())
            y = int(dialog.y_edit.text())
            width = int(dialog.width_edit.text())
            height = int(dialog.height_edit.text())

            if dialog.type_edit.text() == "Точка":
                self.view.draw_point(x, y)
            elif dialog.type_edit.text() == "Линия":
                self.view.draw_line(x, y, x + width, y + height)
            elif dialog.type_edit.text() == "Прямоугольник":
                self.view.draw_rectangle(x, y, width, height)
            elif dialog.type_edit.text() == "Эллипс":
                self.view.draw_ellipse(x, y, width, height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Лабораторная работа 4')
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())
