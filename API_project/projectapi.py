# импортируем нужные нам библиотеки
import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

SCREEN_SIZE_MAIN = [1600, 500]  # размер главного окна
SCREEN_SIZE_HELP = [512, 354]  # размер окна помощи


class Example(QWidget):  # класс, отвечающий за главное окно
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def get_coords(self, address):  # получение координат
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode="
        geocoder_request += address + "&format=json"
        response = requests.get(geocoder_request)  # формирование запрса
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            return toponym_coodrinates  # возвращение нужных нам координат

    def getImage(self):  # Получение начального изображения
        map_request = "http://static-maps.yandex.ru/1.x/?ll=37.53,55.7&spn=0.002,0.0022&l=map"
        response = requests.get(map_request)  # формирование запроса
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"  # файл, в котором хранится изображение во время выполнения программы
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def draw(self):  # обновление изображения
        type_map = 'map'
        if self.map.isChecked():
            type_map = 'map'
        elif self.satellite.isChecked():
            type_map = 'sat'
        elif self.hybrid.isChecked():
            type_map = 'skl'
        if self.plug.checkState():
            type_map += ',trf'
        if self.stop.checkState():
            type_map += ',skl'
        coords = '{},{}'.format(self.v_lat.value(), self.v_long.value())
        scale = '{},{}'.format(self.d_lat.value(), self.d_long.value())
        map_request = "http://static-maps.yandex.ru/1.x/?ll={}&spn={}&l={}".format(coords, scale,
                                                                                   type_map)  # формирование запроса
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"  # файл, в котором хранится изображение во время выполнения программы
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def initUI(self):  # загрузка интерфейса
        self.setGeometry(100, 300, *SCREEN_SIZE_MAIN)
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        self.setFont(font)
        self.setting_panel = QtWidgets.QLabel(self)  # метка панели
        self.setting_panel.setGeometry(QtCore.QRect(930, -55, 500, 150))
        font = QtGui.QFont()
        font.setFamily("Viner Hand ITC")
        self.setting_panel.setFont(font)
        self.setting_panel.setObjectName("setting_panel")
        self.help = QtWidgets.QPushButton(self)  # кнопка помощи
        self.help.setGeometry(QtCore.QRect(650, 20, 221, 51))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        self.help.setFont(font)
        self.help.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.help.setObjectName("help")
        self.update = QtWidgets.QPushButton(self)  # кнопка для обновления карты
        self.update.setGeometry(QtCore.QRect(650, 360, 231, 61))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        self.update.setFont(font)
        self.update.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.update.setObjectName("update")
        self.label_coords = QtWidgets.QLabel(self)  # метка координат
        self.label_coords.setGeometry(QtCore.QRect(1050, 60, 241, 61))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setItalic(True)
        self.label_coords.setFont(font)
        self.label_coords.setObjectName("label_coords")
        self.label_scale = QtWidgets.QLabel(self)  # метка масштаба
        self.label_scale.setGeometry(QtCore.QRect(1080, 160, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setItalic(True)
        self.label_scale.setFont(font)
        self.label_scale.setObjectName("label_scale")
        self.label_lat_long = QtWidgets.QLabel(self)
        self.label_lat_long.setGeometry(QtCore.QRect(1320, 20, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setItalic(True)
        self.label_lat_long.setFont(font)  # метка широта, длгота
        self.label_lat_long.setObjectName("label_lat_long")
        self.label_show_district = QtWidgets.QLabel(self)
        self.label_show_district.setGeometry(QtCore.QRect(1090, 240, 231, 91))
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setItalic(True)
        self.label_show_district.setFont(font)  # метка осмотра местности
        self.label_show_district.setObjectName("label_show_district")
        self.up = QtWidgets.QPushButton(self)  # кнопка для движения вверх
        self.up.setGeometry(QtCore.QRect(1390, 230, 61, 41))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.up.setFont(font)
        self.up.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.up.setObjectName("up")
        self.left = QtWidgets.QPushButton(self)  # кнопка для движения влево
        self.left.setGeometry(QtCore.QRect(1320, 280, 56, 41))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.left.setFont(font)
        self.left.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.left.setObjectName("left")
        self.down = QtWidgets.QPushButton(self)  # кнопка для движения вниз
        self.down.setGeometry(QtCore.QRect(1390, 280, 61, 41))
        self.down.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.down.setObjectName("down")
        self.right = QtWidgets.QPushButton(self)  # кнопка для движения вправо
        self.right.setGeometry(QtCore.QRect(1470, 280, 56, 41))
        self.right.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.right.setObjectName("right")
        self.label_d_lat_long = QtWidgets.QLabel(self)  # метка разница долгот и широт
        self.label_d_lat_long.setGeometry(QtCore.QRect(1210, 140, 300, 21))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setItalic(True)
        self.label_d_lat_long.setFont(font)
        self.label_d_lat_long.setObjectName("label_d_lat_long")
        self.name = QtWidgets.QLineEdit(self)  # название места, которое вы хотите найти
        self.name.setGeometry(QtCore.QRect(1160, 360, 231, 51))
        self.name.setObjectName("name")
        self.find = QtWidgets.QPushButton(self)  # кнопка поиска места
        self.find.setGeometry(QtCore.QRect(1160, 430, 231, 51))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        self.find.setFont(font)
        self.find.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.find.setObjectName("find")
        self.label_place = QtWidgets.QLabel(self)  # метка найти место
        self.label_place.setGeometry(QtCore.QRect(940, 350, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setItalic(True)
        self.label_place.setFont(font)
        self.label_place.setObjectName("label_place")
        self.label_error = QtWidgets.QLabel(self)  # метка ошибки
        self.label_error.setGeometry(QtCore.QRect(940, 430, 231, 31))
        self.label_error.setText("")
        self.label_error.setObjectName("label_error")
        self.v_lat = QtWidgets.QDoubleSpinBox(self)  # долгота
        self.v_lat.setGeometry(QtCore.QRect(1270, 60, 121, 41))
        self.v_lat.setDecimals(3)
        self.v_lat.setMaximum(360.0)
        self.v_lat.setSingleStep(0.001)
        self.v_lat.setProperty("value", 37.53)
        self.v_lat.setObjectName("v_lat")
        self.v_long = QtWidgets.QDoubleSpinBox(self)  # широта
        self.v_long.setGeometry(QtCore.QRect(1420, 60, 121, 41))
        self.v_long.setDecimals(3)
        self.v_long.setMaximum(180.0)
        self.v_long.setSingleStep(0.001)
        self.v_long.setProperty("value", 55.7)
        self.v_long.setObjectName("v_long")
        self.d_lat = QtWidgets.QDoubleSpinBox(self)  # разница долготы
        self.d_lat.setGeometry(QtCore.QRect(1270, 170, 121, 41))
        self.d_lat.setDecimals(3)
        self.d_lat.setMaximum(1.0)
        self.d_lat.setSingleStep(0.001)
        self.d_lat.setProperty("value", 0.002)
        self.d_lat.setObjectName("d_lat")
        self.d_long = QtWidgets.QDoubleSpinBox(self)  # разница широты
        self.d_long.setGeometry(QtCore.QRect(1420, 170, 121, 41))
        self.d_long.setDecimals(3)
        self.d_long.setMaximum(1.0)
        self.d_long.setSingleStep(0.001)
        self.d_long.setProperty("value", 0.002)
        self.d_long.setObjectName("d_long")
        self.verticalLayoutWidget = QtWidgets.QWidget(self)  # здесь находится первая группа pushbutton-ов
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(650, 90, 211, 251))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.map = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        self.map.setFont(font)  # тип карта
        self.map.setCheckable(True)
        self.map.setChecked(True)
        self.map.setAutoRepeat(False)
        self.map.setAutoExclusive(True)
        self.map.setObjectName("map")
        self.verticalLayout.addWidget(self.map)
        self.satellite = QtWidgets.QRadioButton(self.verticalLayoutWidget)  # тип спутник
        self.satellite.setObjectName("satellite")
        self.verticalLayout.addWidget(self.satellite)
        self.hybrid = QtWidgets.QRadioButton(self.verticalLayoutWidget)  # тип гибрид
        self.hybrid.setAutoRepeat(False)
        self.hybrid.setObjectName("hybrid")
        self.verticalLayout.addWidget(self.hybrid)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self)  # здесь находится вторая группа pushbutton-ов
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(1410, 360, 160, 111))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.big = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)  # увеличенное изображение
        self.big.setChecked(True)
        self.big.setObjectName("big")
        self.verticalLayout_2.addWidget(self.big)
        self.little = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)  # уменьшенное изображение
        self.little.setObjectName("little")
        self.verticalLayout_2.addWidget(self.little)
        self.plug = QtWidgets.QCheckBox(self)  # пробки
        self.plug.setGeometry(QtCore.QRect(880, 120, 131, 51))
        self.plug.setObjectName("plug")
        self.stop = QtWidgets.QCheckBox(self)  # названия объектов
        self.stop.setGeometry(QtCore.QRect(880, 190, 201, 111))
        self.stop.setObjectName("stop")
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(20, 20)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)
        self.update.clicked.connect(self.draw)
        self.up.clicked.connect(self.move_up)
        self.down.clicked.connect(self.move_down)
        self.left.clicked.connect(self.move_left)
        self.right.clicked.connect(self.move_right)
        self.find.clicked.connect(self.find_place)
        self.help.clicked.connect(self.h)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Отображение карты"))
        self.setting_panel.setText(_translate("Form",
                                              "<html><head/><body><p><span style=\" font-size:16pt;\""
                                              ">панель управления</span></p></body></html>"))
        self.help.setText(_translate("Form", "Помощь"))
        self.update.setText(_translate("Form", "Обновить карту"))
        self.label_coords.setText(_translate("Form",
                                             "<html><head/><body><p>Введите координаты места,"
                                             " </p><p>которое вы хотите увидеть</p></body></html>"))
        self.label_scale.setText(_translate("Form", "Введите масштаб"))
        self.label_lat_long.setText(_translate("Form", "Долгота        Широта"))
        self.label_show_district.setText(_translate("Form",
                                                    "<html><head/><body><p>Осмотрите окрестности,"
                                                    "</p><p>используя эти кнопки или</p><p>кнопки"
                                                    " клавиатуры(w,a,s,d)</p></body></html>"))
        self.up.setText(_translate("Form", "↑"))
        self.left.setText(_translate("Form", "← "))
        self.down.setText(_translate("Form", "↓"))
        self.right.setText(_translate("Form", "→"))
        self.label_d_lat_long.setText(_translate("Form", "Разница       долгот                   широт"))
        self.find.setText(_translate("Form", "Поиск"))
        self.label_place.setText(_translate("Form",
                                            "<html><head/><body><p>Введите место, которое"
                                            " </p><p>хотели бы увидеть</p></body></html>"))
        self.map.setText(_translate("Form", "Карта"))
        self.satellite.setText(_translate("Form", "Вид со спутника"))
        self.hybrid.setText(_translate("Form", "Гибрид"))
        self.big.setText(_translate("Form", "Крупным планом"))
        self.little.setText(_translate("Form", "Мелким планом"))
        self.plug.setText(_translate("Form", "Посмотреть\n"
                                             "пробки"))
        self.stop.setText(_translate("Form", "Посмотреть\n"
                                             "названия объектов"))

    def find_place(self):  # нахождение места
        try:
            lat, long = self.get_coords(self.name.text()).split()  # долгота широта
            self.v_lat.setValue(round(float(lat), 3))
            self.v_long.setValue(round(float(long), 3))
            if self.little.isChecked():
                self.d_lat.setValue(0.01)
                self.d_long.setValue(0.01)
            elif self.big.isChecked():
                self.d_lat.setValue(0.002)
                self.d_long.setValue(0.002)
            self.draw()
            self.label_error.setText('')
        except:
            self.label_error.setText('<h3 style="color: rgb(250, 55, 55);"'
                                     '>Что-то пошло не так.</h3>')

    def h(self):  # вызов окна помощи
        self.help_form = HelpForm()
        self.help_form.show()

    def move_up(self):  # движение вверх
        long = self.v_long.value()
        long += 0.001
        self.v_long.setValue(long)
        self.draw()

    def move_right(self):  # движение вправо
        lat = self.v_lat.value()
        lat += 0.001
        self.v_lat.setValue(lat)
        self.draw()

    def move_left(self):  # движение влево
        lat = self.v_lat.value()
        lat -= 0.001
        self.v_lat.setValue(lat)
        self.draw()

    def move_down(self):  # движение вниз
        long = self.v_long.value()
        long -= 0.001
        self.v_long.setValue(long)
        self.draw()

    def keyPressEvent(self, event):  # обработка клавиш
        if event.key() == Qt.Key_W:
            self.move_up()
        elif event.key() == Qt.Key_S:
            self.move_down()
        elif event.key() == Qt.Key_A:
            self.move_left()
        elif event.key() == Qt.Key_D:
            self.move_right()

    def closeEvent(self, event):  # при закрытии приложения файл удаляется
        os.remove(self.map_file)


class HelpForm(QWidget):  # класс помощи
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 250, *SCREEN_SIZE_HELP)
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(20, 10, 471, 331))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Помощь"))
        self.textBrowser.setHtml(_translate("Form",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\""
                                            " \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\""
                                            " /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\';"
                                            " font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;"
                                            " margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\""
                                            " font-size:9pt;\">                   Доброго времени суток.</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;"
                                            " margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\""
                                            " font-size:9pt;\">Это программа предназначена для работы с картой."
                                            "</span></p>\n""<p style=\" margin-top:0px; margin-bottom:0px;"" margin"
                                            "-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\""
                                            "><span style=\" font-size:9pt;\">Слева находится сама карта, справа - "
                                            "панель"" управления.</span></p>\n""<p style=\" margin-top:0px; margin-"
                                            "bottom:0px;"" margin-left:0px; margin-right:0px; -qt-block-indent:0;"
                                            " text-indent:0px;\"""><span style=\" font-size:9pt;\">Можно менять "
                                            "координаты и масштаб"" местности.</span></p>\n" "<p style=\""
                                            " margin-top:0px; margin-bottom:0px;"
                                            " margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\""
                                            "><span style=\" font-size:9pt;\">Также можно найти место по названию."
                                            "</span></p>\n""<p style=\" margin-top:0px; margin-bottom:0px;"
                                            " margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\""
                                            "><span style=\" font-size:9pt;\">Можно смтореть наличие пробок, названия"
                                            " объектов.</span></p>\n""<p style=\" margin-top:0px; margin-bottom:0px;"
                                            " margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\""
                                            "><span style=\" font-size:9pt;\">Передвигаться по местности можно,"
                                            " используя кнопки</span></p>\n""<p style=\" margin-top:0px;"
                                            " margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;"
                                            " text-indent:0px;\"><span style=\" font-size:9pt;\">программы или кнопки"
                                            " клавиатуры(A,W,S,D)</span></p></body></html>"))


if __name__ == '__main__':  # запуск программы
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
