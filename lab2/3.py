"""
Импортируем необходимые для работы библиотеки.
1) sys - используется для корректного завершения работы программы
2) QtCore:
    - Qt - отвечает за пространство имен, которое содержит различные константы, типы данных и функции
    - QRectF - класс, который предоставляет прямогугольник с вещественными координатами
    - QObject - базовый класс, который обеспечивает механизм сигналов и обработки событий
3) QtGui:
    - QPainter - для рендеринга
    - QPen - класс, определяющий стиль линий
    - QBrush - класс, определяющий стиль заливки фигур
    - QColor - класс для предоставления цветов
4) QtWidgets:
    - QApplication - управление главным циклом событий
    - QGraphicsRectItem - предоставляет прямоугольник на сцене
    - QGraphicsView - отображение графической сцены
    - QGraphicsScene - область для управления объектами, которые будут отображаться
    - QGraphicsItem - базовый класс для графических элементов
    - QMenu - класс для создания контекстных меню
    - QGraphicsSceneContextMenuEvent - событие, генерируемое при вызове контекстного меню на графической сцене
    - QMainWindow - главное окно приложения
    - QVBoxLayout - организация компонентов в вертикальном направлении
    - QWidget - класс для всех объектов пользовательского интерфейса
    - QColorDialog - диалоговое окно для выбора цвета
"""

import sys
from PySide6.QtCore import Qt, QRectF, QObject
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsRectItem,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem,
    QMenu,
    QGraphicsSceneContextMenuEvent,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QColorDialog
)

"""
Создаем класс CustomGraphicsRectItem, который будет расширять функционал QGraphicsRectItem.
Переопределяем метод contextMenuEvent, который вызывается при вызове контекстного меню на объекте. 
Внутри этого метода создается контекстное меню QMenu с различными опциями для изменения свойств прямоугольника
"""


class CustomGraphicsRectItem(QGraphicsRectItem):
    def __init__(self):
        # вызываем конструктор класса
        super(CustomGraphicsRectItem, self).__init__()

        # Начальные значения свойств объекта
        self.setRect(0, 0, 100, 100)
        self.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        self.setBrush(QBrush(Qt.green))

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent):
        # создаем контекстное меню
        context_menu = QMenu()

        # Подменю для толщины линии
        pen_submenu = context_menu.addMenu('Линия контура')
        thickness_submenu = context_menu.addMenu('Толщина')

        # Создаем список действий для выбора толщины линии
        # При выборе какой-либо толщины вызывается лямбда функция,
        # которая вызывает внутри себя метод setPen для установки нового объекта
        # QPen с текущим цветом, толщиной и текущим стилем линии
        # (создать функции с методом sender() не получилось, поэтому используем
        # собственный сигнал для обработки событий контекстного меню

        thickness_actions = [thickness_submenu.addAction(str(i), lambda thickness=i: self.setPen(
            QPen(self.pen().color(), thickness, self.pen().style()))) for i in range(1, 6)]

        # Подменю для типа линии
        style_submenu = pen_submenu.addMenu('Тип')
        styles_dict = {
            'Сплошная линия': Qt.SolidLine,
            'Пунктирная линия': Qt.DashLine,
            'Точечная линия': Qt.DotLine,
            'Пунктирно-точечная линия': Qt.DashDotLine
        }

        # Создаем список действий для выбора стиля линии
        # вызываем метод addAction для подменю, затем вызывается лямбда-функция
        # при выборе соответствующего элемента, т.е. стиля линии.
        # Устанавливаем новый объект QPen с текущим цветом, толщиной линии и выбранным стилем
        style_actions = [style_submenu.addAction(style_name, lambda style=styles_dict[style_name]: self.setPen(
            QPen(self.pen().color(), self.pen().width(), style))) for style_name in styles_dict]

        # Устанавливаем фон
        background_color_action = context_menu.addAction('Цвет фона', lambda: self.setBrush(
            QBrush(QColorDialog.getColor(self.brush().color()))))

        # И цвет линии контура по той же логике, что и выше
        line_color_action = context_menu.addAction('Цвет линии контура', lambda: self.setPen(
            QPen(QColorDialog.getColor(self.pen().color()), self.pen().width(), self.pen().style())))

        # Отображаем контекстное меню
        context_menu.exec(event.screenPos())


class GraphicsView(QGraphicsView):
    def __init__(self):
        super(GraphicsView, self).__init__()

        # Создаем сцену для размещения и управления графическими объектами
        scene = QGraphicsScene(self)
        self.setScene(scene)

        # Создание экземпляра класса CustomGraphicsRectItem и добавление сцены
        rect_item = CustomGraphicsRectItem()
        scene.addItem(rect_item)

        # устанавливаем флаг ItemIsMovable для того, чтобы была возможность
        # перемещать объект мышью внутри сцены
        rect_item.setFlag(QGraphicsItem.ItemIsMovable)
        self.setSceneRect(scene.itemsBoundingRect())

        # белый фон
        self.setStyleSheet('background-color: white;')


# Класс главного окна приложения
class AppMainWindow(QMainWindow):
    def __init__(self):
        super(AppMainWindow, self).__init__()
        self.setWindowTitle('Лабораторная работа 3')
        self.setGeometry(400, 200, 600, 500)
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        graphics_view = GraphicsView()
        layout.addWidget(graphics_view)

        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = AppMainWindow()
    main_window.show()

    sys.exit(app.exec())
