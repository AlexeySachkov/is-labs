import sys
import os
import design
import classify
from PIL import Image
from PyQt5 import QtWidgets, QtGui
from PIL.ImageQt import ImageQt


class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Инициализируем наш дизайн
        self.setupUi(self)
        # Событие нажатия на кнопку
        self.searchButton.clicked.connect(self.find_file)

    def find_file(self):
        # Очищаем, если там уже были элементы
        self.pathWidget.clear()
        self.imgLabel.clear()
        self.pathWidget.clear()
        # Открываем диалог выбора файла
        # и устанавливаем значение переменной равной пути
        # к выбранному изображению
        file_path, file_type = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "/home", "Images (*.png *.xpm *.jpg)")
        if file_path:
            # Выводим путь к выбранному изображению
            self.pathWidget.addItem(file_path)
            # Открываем изображение
            image = Image.open(file_path)

            # Если размер изображения больше допустимого,
            # пропорционально уменьшим размер изображения
            if image.size[0] > 600 or image.size[1] > 600:
                ratio = min(float(600) / image.size[1], float(600) / image.size[0])
                w = int(image.size[0] * ratio)
                h = int(image.size[1] * ratio)
                image = image.resize((w, h), Image.ANTIALIAS)

            # Конвертируем Image в Pixmap
            qImage = ImageQt(image)
            pixmap = QtGui.QPixmap.fromImage(qImage)
            # Изменим размер imgLabel по размеру изображения
            self.imgLabel.resize(image.size[0], image.size[1])
            # Выводим изображение
            self.imgLabel.setPixmap(pixmap)
            # Увеличиваем размер окна
            # если изображение меньше минимального размера окна
            if image.size[0] < 500:
                h = self.imgLabel.height()
                self.resize(540, h + 90)
            # если изображение больше минимального размера окна
            else:
                self.setFixedSize(self.imgLabel.sizeHint())

            # Отправим путь к изображению для распознавания лица
            name = classify.get_name(file_path)
            # Редактируем полученное имя
            name = name.replace("_", " ").title()
            # Выводим имя
            self.nameLabel.setText('This is %s!' % name)


def main():
    # Новый экземпляр QApplication
    app = QtWidgets.QApplication(sys.argv)
    # Создаём объект класса App
    window = App()
    # Показываем окно
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
