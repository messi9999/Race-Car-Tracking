# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1390, 984)
        font = QtGui.QFont()
        font.setPointSize(9)
        Dialog.setFont(font)
        self.src = QtWidgets.QLabel(parent=Dialog)
        self.src.setGeometry(QtCore.QRect(30, 30, 1071, 701))
        self.src.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.src.setAutoFillBackground(False)
        self.src.setStyleSheet("background-color: #1de9b6;\n" "")
        self.src.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.src.setLineWidth(2)
        self.src.setText("")
        self.src.setObjectName("src")
        self.src.setMouseTracking(True)
        self.import_btn = QtWidgets.QPushButton(parent=Dialog)
        self.import_btn.setGeometry(QtCore.QRect(1230, 900, 141, 61))
        self.close_btn = QtWidgets.QPushButton(parent=Dialog)
        self.close_btn.setGeometry(QtCore.QRect(1230, 100, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.import_btn.setFont(font)
        self.import_btn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.close_btn.setFont(font)
        self.close_btn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.import_btn.setObjectName("import_btn")
        self.close_btn.setObjectName("close_btn")
        self.edit_btn = QtWidgets.QPushButton(parent=Dialog)
        self.edit_btn.setGeometry(QtCore.QRect(1230, 830, 141, 61))
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
        self.close_btn.setText(_translate("Dialog", "Close"))
        self.edit_btn.setText(_translate("Dialog", "EDIT"))
