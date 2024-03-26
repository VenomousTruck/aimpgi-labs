import math
import sys
import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


class AffineTransformationApp(QMainWindow):
    """
    Класс AffineTransformationApp представляет главное окно приложения.
    """
    def __init__(self):
        """
        Инициализируем основные параметры окна.
        Создаем панель управления с элементами для перемещения, вращения, масштабирования фигуры.
        """
        super().__init__()
        self.setWindowTitle("Аффинные преобразования")
        self.setGeometry(200, 100, 1000, 700)

        # Область для рисования
        self.drawing_area = DrawingArea(self)
        self.setCentralWidget(self.drawing_area)

        # Область управления преобразованиями
        control_dock = QDockWidget("Управление")
        control_widget = QWidget()
        control_layout = QVBoxLayout()

        # Управление перемещением
        translation_layout = QHBoxLayout()
        translation_label = QLabel("Перемещение:")
        self.translation_x_input = QLineEdit()
        self.translation_y_input = QLineEdit()
        translation_button = QPushButton("Переместить")
        translation_button.clicked.connect(self.drawing_area.translate)
        translation_layout.addWidget(translation_label)
        translation_layout.addWidget(self.translation_x_input)
        translation_layout.addWidget(self.translation_y_input)
        translation_layout.addWidget(translation_button)

        # Управление поворотом
        rotation_layout = QHBoxLayout()
        rotation_label = QLabel("Поворот:")
        self.rotation_input = QLineEdit()
        rotation_button = QPushButton("Повернуть")
        rotation_button.clicked.connect(self.drawing_area.rotate)
        rotation_layout.addWidget(rotation_label)
        rotation_layout.addWidget(self.rotation_input)
        rotation_layout.addWidget(rotation_button)

        # Управление масштабированием
        scale_layout = QHBoxLayout()
        scale_label = QLabel("Масштабирование:")
        self.scale_x_input = QLineEdit()
        self.scale_y_input = QLineEdit()
        scale_button = QPushButton("Масштабировать")
        scale_button.clicked.connect(self.drawing_area.scale)
        scale_layout.addWidget(scale_label)
        scale_layout.addWidget(self.scale_x_input)
        scale_layout.addWidget(self.scale_y_input)
        scale_layout.addWidget(scale_button)

        # Добавляем всё в главный лейаут
        control_layout.addLayout(translation_layout)
        control_layout.addLayout(rotation_layout)
        control_layout.addLayout(scale_layout)

        # Затем главный лейаут добавляем в главный виджет
        control_widget.setLayout(control_layout)
        control_dock.setWidget(control_widget)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, control_dock)


class DrawingArea(QWidget):
    """
    Класс DrawingArea представляет область для рисования, на которой
    будет отображаться фигура и выполняться аффинные преобразования.
    """
    def __init__(self, parent):
        """
        В методе генерируются начальные точки фигуры и устанавливается
        пустая матрица преобразования.
        """
        super().__init__(parent)
        self.figure_points = self.generate_figure_points(250, 250)
        self.transform = QTransform()

    def generate_figure_points(self, x, y):
        """
        Метод генерирует список точек, которые определяют форму фигуры. Принимает параметры:
        :param x: координата x центра фигуры
        :param y: координата у центра фигуры
        :param radius: радиус фигуры
        :param num_points: количество точек
        :return: список координат точек фигуры
        """
        points = [
            QPoint(x - 100, y),
            QPoint(x - 5, y - 100),
            QPoint(x + 20, y - 60),
            QPoint(x + 50, y - 80),
            QPoint(x + 100, y)
        ]
        return points

    def paintEvent(self, event):
        """
        Метод paintEvent нужен для обработки события перерисовки фигуры,
        при масштабировании фигуры, изменении ее размеров.
        """

        # - painter -- объект класса QPainter, для рисовки фигуры на виджете
        # - устанавливаем сглаживание с помощью setRenderHint()
        # - устанавливаем кисть для контура с помощью QPen()
        # - устанавливаем кисть для заливки с помощью QBrush()
        # - создаем пустой список для хранения преобразованных точек transformedPoints
        #
        # Затем делаем итерацию по исходным точкам фигуры:
        # - применяем текущее аффинное преобразование к каждой точке фигуры
        # - после этого добавляем преобразованную точку в список transformedPoints.
        #
        # Создаем объект типа QPolygon из списка преобразованных точек, это и будет нашей
        # измененной звездой.

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(Qt.blue))

        transformed_points = []
        for point in self.figure_points:
            transformed_point = self.transform.map(point)
            transformed_points.append(transformed_point)

        polygon = QPolygon(transformed_points)
        painter.drawPolygon(polygon)

    def translate(self):
        """
        Метод translate() перемещает фигуру на заданные параметры dx и dy
        """
        dx = float(self.parent().translation_x_input.text())
        dy = float(self.parent().translation_y_input.text())

        self.figure_points = self.apply_transform(self.figure_points, self.translation_matrix(dx, dy))
        self.update()

    def rotate(self):
        """
        Метод rotate() поворачивает фигуру на заданный параметр угла angle (радианы)
        """
        angle = math.degrees(float(self.parent().rotation_input.text()))
        center_x = sum(point.x() for point in self.figure_points) / len(self.figure_points)
        center_y = sum(point.y() for point in self.figure_points) / len(self.figure_points)

        self.figure_points = self.apply_transform(self.figure_points, self.rotation_matrix(angle, center_x, center_y))
        self.update()

    def scale(self):
        """
        Метод scale() изменяет масштаб фигуры на заданные параметры sx и sy
        """
        sx = float(self.parent().scale_x_input.text())
        sy = float(self.parent().scale_y_input.text())
        center_x = sum(point.x() for point in self.figure_points) / len(self.figure_points)
        center_y = sum(point.y() for point in self.figure_points) / len(self.figure_points)

        self.figure_points = self.apply_transform(self.figure_points, self.scale_matrix(sx, sy, center_x, center_y))
        self.update()

    def translation_matrix(self, dx, dy):
        """
        Матрица преобразования координат фигуры
        :param dx: величина сдвига по х
        :param dy: величина сдвига по y
        :return: матрица преобразования координат
        """
        return np.array([[1, 0, dx],
                         [0, 1, dy],
                         [0, 0, 1]])

    def scale_matrix(self, sx, sy, center_x, center_y):
        """
        Матрица преобразования масштаба
        :param sx: коэффициент масштабирования по х
        :param sy: коэффициент масштабирования по y
        :param center_x: координата x центра объекта
        :param center_y: координата y центра объекта
        :return: матрица преобразования масштаба.
        """
        return np.array([[sx, 0, (1 - sx) * center_x],
                         [0, sy, (1 - sy) * center_y],
                         [0, 0, 1]])

    def rotation_matrix(self, angle, center_x, center_y):
        """
        Матрица преобразования поворота фигуры
        :param angle: угол поворота в радианах
        :param center_x: координата x центра вращения
        :param center_y: координата y центра вращения
        :return: матрица преобразования поворота фигуры.
        """
        c = math.cos(angle)
        s = math.sin(angle)
        return np.array([[c, -s, (1 - c) * center_x + s * center_y],
                         [s, c, -s * center_x + (1 - c) * center_y],
                         [0, 0, 1]])

    def apply_transform(self, points, transform_matrix):
        """
        Применяет матрицу преобразования к списку исходных точек объекта и возвращает список точек,
        преобразованных согласно этой матрице
        :param points: список исходных точек объекта, которые требуется преобразовать
        :param transform_matrix: матрица преобразования, которая будет применена к исходным точкам.
        :return: матрица преобразования бла-бла-бла
        """

        """
        Сначала метод создает массив points_array, содержащий координаты исходных точек объекта, 
        которые преобразованы в двумерный массив. Каждая строка этого массива представляет координаты 
        одной точки объекта.

        Затем к массиву points_array добавляется столбец единиц с помощью np.ones((len(points_array), 1)),
        чтобы преобразовать координаты точек в форму, совместимую с матрицей преобразования.
        Иначе была бы ошибка TypeError.

        После этого выполняется умножение матрицы points_array на транспонированную матрицу 
        transform_matrix. Результат этого умножения содержит координаты преобразованных точек 
        в новом массиве transformed_points.

        Наконец, массив transformed_points преобразуется обратно в список объектов QPoint (точек), 
        где каждая координата округляется до целого числа с помощью функции int(). 
        Этот список точек возвращается как результат работы метода.

        Когда эта функция вызывается вместе с определенной матрицей преобразования, 
        она применяет это преобразование ко всем точкам объекта, что позволяет изменить его положение, 
        размер или ориентацию согласно заданным параметрам.
        """
        points_array = np.array([[point.x(), point.y()] for point in points], dtype=np.float64)
        points_array = np.hstack((points_array, np.ones((len(points_array), 1))))
        transformed_points = np.dot(points_array, transform_matrix.T)[:, :2]
        return [QPoint(int(point[0]), int(point[1])) for point in transformed_points]


if __name__ == "__main__":
    main_app = QApplication()
    main_window = AffineTransformationApp()
    main_window.show()
    sys.exit(main_app.exec())