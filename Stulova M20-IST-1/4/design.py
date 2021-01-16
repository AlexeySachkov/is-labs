# Реализация формы, сгенерированна из чтения ui-файла 'design.ui'
# c помощью PyQt5 5.13.0
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(540, 59)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(540, 39))
        self.centralwidget.setObjectName("centralwidget")
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(440, 10, 75, 23))
        self.searchButton.setObjectName("searchButton")
        self.pathWidget = QtWidgets.QListWidget(self.centralwidget)
        self.pathWidget.setGeometry(QtCore.QRect(20, 10, 391, 21))
        self.pathWidget.setObjectName("pathWidget")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(20, 40, 451, 21))
        self.nameLabel.setText("")
        self.nameLabel.setObjectName("nameLabel")
        self.imgLabel = QtWidgets.QLabel(self.centralwidget)
        self.imgLabel.setGeometry(QtCore.QRect(20, 70, 721, 831))
        self.imgLabel.setObjectName("imgLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Actor Recognizer"))
        self.searchButton.setText(_translate("MainWindow", "Overview"))
        self.imgLabel.setText(_translate("MainWindow", "Photo"))
