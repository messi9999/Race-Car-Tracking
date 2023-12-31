from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QLabel,
    QLineEdit,
    QDialog,
    QVBoxLayout,
    QDialogButtonBox,
    QPushButton,
)
from ui_main import Ui_Dialog
from PyQt6.QtGui import QImage, QPixmap
from qt_material import apply_stylesheet
import sys, cv2, json
from PyQt6 import QtCore, QtGui

from PyQt6.QtCore import Qt

from track import CarTrack

import ndi

import time


class ConfirmationDialog(QDialog):
    data_updated = QtCore.pyqtSignal(str, str)

    def __init__(self, car_num, driver_name, index, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Label Text")
        layout = QVBoxLayout(self)
        self.car_num_edit = QLineEdit(self)
        self.car_num_edit.setText(car_num)
        layout.addWidget(self.car_num_edit)
        self.driver_name_edit = QLineEdit(self)
        self.driver_name_edit.setText(driver_name)
        layout.addWidget(self.driver_name_edit)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        # delete_button = QPushButton("Delete", self)
        # delete_button.clicked.connect(self.delete_label)
        # button_box.addButton(delete_button, QDialogButtonBox.ButtonRole.RejectRole)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Index of the QLabel to delete
        self.index_to_delete = None

        # Set the current index of the QLabel
        self.current_index = index

        self.scaleX = 1
        self.scaleY = 1

    # def delete_label(self):
    #     self.accept()

    def accept(self):
        updated_car_num = self.car_num_edit.text()
        updated_driver_name = self.driver_name_edit.text()
        self.data_updated.emit(updated_car_num, updated_driver_name)
        super().accept()


class Main_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.import_btn.clicked.connect(self.main)
        self.ui.close_btn.clicked.connect(self.handle_close)
        self.index = -1
        self.ui.edit_btn.clicked.connect(self.open_confirmation_dialog)
        self.width_source, self.height_source = (
            self.ui.src.width(),
            self.ui.src.height(),
        )
        self.labels = []
        self.sort_cars()
        self.show()
        self.saved_car_num = None
        self.saved_driver_name = None
        self.saved_index = None

        self.isClick = False
        self.mouse = [-1000, -1000]
        self.isMouseOver = False

        self.ui.src.mousePressEvent = lambda event: self.get_cursor_coordinates(event)
        self.cap = None
        self.setMouseTracking(True)

        self.carids = []

        self.bg_im = cv2.imread("./img/background.PNG")

        self.tracker = CarTrack()

    def handle_close(self):
        if self.cap:
            self.cap.release()
        self.close()

    def change_car_data(self):
        json_object = json.dumps(self.car_dict, indent=4)
        with open("car.json", "w") as outfile:
            outfile.write(json_object)

    def get_cursor_coordinates(self, event):
        self.x_pos, self.y_pos = event.pos().x(), event.pos().y()
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse = [self.x_pos - 30, self.y_pos - 30]
            self.isClick = True

    def mouseMoveEvent(self, event):
        self.x_pos, self.y_pos = event.pos().x(), event.pos().y()
        self.mouse = [self.x_pos - 30, self.y_pos - 30]

    def sort_cars(self):
        with open("car.json") as fp:
            elements = json.loads(fp.read())
            sorted_data = sorted(elements.items(), key=lambda x: x[0])
            self.car_dict = dict(sorted_data)
            for i, key in enumerate(self.car_dict):
                label = QLabel(self)
                label.setGeometry(
                    QtCore.QRect(40 + (i % 8) * 130, 750 + int(i / 8) * 55, 110, 40)
                )
                font = QtGui.QFont()
                font.setBold(True)
                font.setWeight(75)
                label.setFont(font)
                label.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                label.setStyleSheet(
                    "border: 2px solid green;\n"
                    "background-color: black;\n"
                    "color: white;\n"
                    "border-radius: 5px;\n"
                    "font-weight: bold;\n"
                    ""
                )
                label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                label.setObjectName(f"label{i}")
                label.setText(key + "\n" + self.car_dict[key])
                label.mousePressEvent = lambda event, index=i: self.select_label_text(
                    index
                )  # Connect the clicked event to edit_label_text
                self.labels.append(label)

    def main(self):
        ndi.initialize()
        sources = ndi.find_sources()
        if not sources:
            print("No NDI sources found!")
            ndi.destroy()
            exit()

        source = sources[0]
        receiver = ndi.Receiver(
            source_name=source.ndi_name,
            color_format=ndi.NDIlib_recv_color_format_e_BGRX_BGRA,
        )

        try:
            while self.isVideo:
                frame = receiver.capture_video()

                height, width, channel = frame.shape
                scaleX = width / self.width_source
                scaleY = height / self.height_source

                self.tracker.mouse = [
                    int(self.mouse[0] * scaleX),
                    int(self.mouse[1] * scaleY),
                ]

                self.tracker.isClick = self.isClick
                frame, self.isMouseOver = self.tracker.run(frame=frame)
                if self.isMouseOver:
                    self.ui.src.setCursor(
                        QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                    )
                else:
                    self.ui.src.setCursor(
                        QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor)
                    )
                self.isClick = False

                src_img = cv2.resize(frame, (self.width_source, self.height_source))
                src_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
                temp_img = QImage(
                    src_img,
                    self.width_source,
                    self.height_source,
                    src_img.strides[0],
                    QImage.Format.Format_RGB888,
                )
                self.ui.src.setPixmap(QPixmap.fromImage(temp_img))

                cv2.waitKey(1)

        finally:
            receiver.destroy()
            ndi.destroy()

    def save_label_data(self, index):
        # Save the data from the QLabel that was clicked
        if len(self.tracker.carids) > 0:
            self.saved_car_num = list(self.car_dict.keys())[self.tracker.carids[0]]
            self.saved_driver_name = self.car_dict[self.saved_car_num]
            print(self.saved_car_num)
            print(self.saved_driver_name)
            self.saved_index = self.tracker.carids[0]

    def set_label_checked(self, index):
        self.labels[index].setStyleSheet(
            "border: 2px solid black;\n"
            "background-color: green;\n"
            "color: white;\n"
            "border-radius: 5px;\n"
            "font-weight: bold;\n"
            ""
        )

    def set_label_unchecked(self, index):
        self.labels[index].setStyleSheet(
            "border: 2px solid green;\n"
            "background-color: black;\n"
            "color: white;\n"
            "border-radius: 5px;\n"
            "font-weight: bold;\n"
            ""
        )

    def select_label_text(self, index):
        if index in self.tracker.carids:
            self.set_label_unchecked(index)
            self.tracker.carids.remove(index)
            index_to_remove = next(
                (
                    i
                    for i, obj in enumerate(self.tracker.titles)
                    if obj["index"] == index
                ),
                None,
            )
            if index_to_remove is not None:
                self.tracker.titles.pop(index_to_remove)

        else:
            # if (
            #     len(self.tracker.targetID) == 0
            #     or len(self.tracker.titles) - len(self.tracker.targetID) == 1
            # ):
            if len(self.tracker.titles) < 3:
                self.set_label_checked(index)
                self.tracker.carids.append(index)
                title = {
                    "index": index,
                    "trackid": 0,
                    "number": list(self.car_dict.keys())[index],
                    "name": self.car_dict[list(self.car_dict.keys())[index]],
                }
                self.tracker.titles.append(title)
            # else:
            #     print("Select the title!")
        self.save_label_data(index)

        if len(self.tracker.carids) == 1:
            self.ui.edit_btn.setEnabled(True)
            self.ui.edit_btn.setStyleSheet(
                "background-color: green; color: white; border: 2px solid green;"
            )
        else:
            self.ui.edit_btn.setEnabled(False)
            self.ui.edit_btn.setStyleSheet(
                "background-color: transparent; color: green; border: 2px solid green;"
            )

    def open_confirmation_dialog(self):
        # Open the confirmation dialog with the saved data
        if self.saved_car_num is not None:
            confirm_dialog = ConfirmationDialog(
                self.saved_car_num, self.saved_driver_name, self.saved_index, self
            )
            confirm_dialog.data_updated.connect(
                self.on_data_updated
            )  # Connect the signal to the slot
            confirm_dialog.exec()

    def on_data_updated(self, updated_car_num, updated_driver_name):
        index = (
            self.sender().current_index
        )  # Get the index from the sender (ConfirmationDialog)
        if updated_car_num != list(self.car_dict.keys())[index]:
            self.car_dict[updated_car_num] = self.car_dict.pop(
                list(self.car_dict.keys())[index]
            )
            self.change_car_data()
        self.labels[index].setText(updated_car_num + "\n" + updated_driver_name)
        self.sort_cars()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Main_Window()
    apply_stylesheet(app, theme="dark_teal.xml")
    sys.exit(app.exec())
