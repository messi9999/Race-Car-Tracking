from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(1580, 1000)
        # Dialog.resize(1580, 1080)
        Dialog.move(60, 60)
        font = QtGui.QFont()
        font.setPointSize(9)
        Dialog.setFont(font)
        self.src = QtWidgets.QLabel(parent=Dialog)
        self.src.setGeometry(QtCore.QRect(30, 20, 1280, 720))
        self.src.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.src.setAutoFillBackground(False)
        self.src.setStyleSheet("background-color: #1de9b6;\n" "")
        self.src.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.src.setLineWidth(2)
        self.src.setText("")
        self.src.setObjectName("src")
        self.src.setMouseTracking(True)
        self.import_btn = QtWidgets.QPushButton(parent=Dialog)
        self.import_btn.setGeometry(QtCore.QRect(1360, 900, 141, 61))
        self.ndi_btn = QtWidgets.QPushButton(parent=Dialog)
        self.ndi_btn.setGeometry(QtCore.QRect(1360, 400, 141, 61))
        self.close_btn = QtWidgets.QPushButton(parent=Dialog)
        self.close_btn.setGeometry(QtCore.QRect(1360, 100, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.import_btn.setFont(font)
        self.import_btn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ndi_btn.setFont(font)
        self.ndi_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.close_btn.setFont(font)
        self.close_btn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.import_btn.setObjectName("import_btn")
        self.ndi_btn.setObjectName("ndi_btn")
        self.close_btn.setObjectName("close_btn")
        self.edit_btn = QtWidgets.QPushButton(parent=Dialog)
        self.edit_btn.setGeometry(QtCore.QRect(1360, 830, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_btn.setFont(font)
        self.edit_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.edit_btn.setObjectName("edit_btn")
        self.edit_btn.setStyleSheet(
            "background-color: transparent; color: green; border: 2px solid green;"
        )

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.import_btn.setText(_translate("Dialog", "Import Video"))
        self.ndi_btn.setText(_translate("Dialog", "NDI Video"))
        self.close_btn.setText(_translate("Dialog", "Close"))
        self.edit_btn.setText(_translate("Dialog", "EDIT"))
