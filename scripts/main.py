import sys
import time
import cv2
import torch

from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel, QSlider
import screen_brightness_control as sbc

from predict import predict_image, CNN

model = CNN(out_channels=2)
weight_path = '../checkpoint/' + 'Weight3.ckpt'
model.load_state_dict(torch.load(weight_path))
model.eval()

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Webcam GUI")
        self.setGeometry(100, 100, 640, 480)
        self.layout = QVBoxLayout()

        self.camera = Camera()
        self.camera.start()
        self.camera.imageUpdate.connect(self.imageUpdateSlot)

        self.feedLabel = QLabel()
        self.layout.addWidget(self.feedLabel)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.setValue(sbc.get_brightness()[0])
        self.slider.valueChanged.connect(self.adjustBrightness)

        self.brightness = QLabel("<h1>Current Brightness: {}%</h1>".format(str(self.slider.value())))
        self.layout.addWidget(self.brightness)

        self.layout.addWidget(self.slider)
        self.btn = QPushButton("Enable Auto Adjust")
        self.btn.clicked.connect(self.btnClicked)
        self.layout.addWidget(self.btn)

        self.setLayout(self.layout)

    def imageUpdateSlot(self, image):
        self.feedLabel.setPixmap(QPixmap.fromImage(image))

    def cancelFeed(self):
        self.btn.setText("Enable Auto Adjust")
        self.camera.stop()

    def enableFeed(self):
        self.btn.setText("Stop Auto Adjust")
        self.camera.enable()

    def btnClicked(self):
        if self.camera.saveImage:
            self.cancelFeed()
        else:
            self.enableFeed()

    def adjustBrightness(self):
        self.brightness.setText("<h1>Current Brightness: {}%</h1>".format(str(self.slider.value())))
        self.brightness.adjustSize()
        sbc.set_brightness(self.slider.value())


class Camera(QThread):
    imageUpdate = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.ThreadActive = True
        self.saveImage = False
        self.lastSaveTime = time.time()

    def run(self):
        capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            curTime = time.time()
            ret, frame = capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flippedImage = cv2.flip(image, 1)
                convertToQtFormat = QImage(flippedImage.data, flippedImage.shape[1], flippedImage.shape[0],
                                           QImage.Format.Format_RGB888)
                pic = convertToQtFormat.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                self.imageUpdate.emit(pic)
                if self.saveImage and int((curTime - self.lastSaveTime) % 60) >= 1:
                    cv2.imwrite("temp_img.png", frame)
                    result = predict_image(model, "temp_img.png")
                    sbc.set_brightness(result)
                    self.lastSaveTime = time.time()

    def stop(self):
        self.saveImage = False

    def enable(self):
        self.saveImage = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
