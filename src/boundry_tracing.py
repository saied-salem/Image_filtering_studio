from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import cv2
import numpy as np
from viewer import Viewer


class Boundry_tracing(qtw.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi("ui/boundry_tracing_tap.ui", self)

        self.image=None
        self.binary_image = None
        self.image_viewer = Viewer()
        self.org_img_layout.addWidget(self.image_viewer)

        self.binary_viewer = Viewer()
        self.bin_img_layout.addWidget(self.binary_viewer)

        self.bourder_viewer = Viewer()
        self.bourder_img_layout.addWidget(self.bourder_viewer)

        self.applay_boundry_tracing_btn.clicked.connect(self.boundry_tracing)
        self.binary_threshold_slider.sliderReleased.connect(self.change_threshold)
        self.Upload_button.clicked.connect(self.upload_image)

    def upload_image(self):
        image_path = qtw.QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.image=cv2.imread(image_path,0)
        self.image_viewer.draw_image(self.image)


    def change_threshold(self):
        print("slideeeeeeeeeeeeeeeer")
        value=self.binary_threshold_slider.value()
        _, self.binary_image = cv2.threshold(self.image, value, 255, cv2.THRESH_BINARY_INV)
        self.binary_viewer.draw_image(self.binary_image)


    def boundry_tracing(self):
        p0 , p1, dire= self.get_p1_p0(self.binary_image)
        bourder = self.get_boundry(self.binary_image, p0, p1, dire)
        bourder_img= self.make_bourder_img(bourder)
        self.bourder_viewer.draw_image(bourder_img)


    def make_bourder_img(self,bourder):
        new_image = np.zeros(self.image.shape)
        for i in bourder:
            new_image[i[0], i[1]] = 255
        return new_image


    def get_p1_p0(self,image):
        p0 = [0, 0]
        p1 = [0, 0]
        dire = 0
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image[i, j] == 255:
                    p0[0] = i
                    p0[1] = j
                    #                 print(p0)
                    break
            else:
                continue

            break
        dire = (dire + 3) % 4
        curr_p = p0.copy()
        movies = [[curr_p[0], curr_p[1] + 1], [curr_p[0] - 1, curr_p[1]], [curr_p[0], curr_p[1] - 1],
                  [curr_p[0] + 1, curr_p[1]]]
        for i in range(4):
            move = movies[i]
            if (image[move[0], move[1]] == 255):
                p1 = move

        return p0, p1, dire

    def get_boundry(self, image, p0, p1, dire):
        perv_p = []
        boundry = []
        curr_point = p1.copy()
        while (1):
            movies = [[curr_point[0], curr_point[1] + 1], [curr_point[0] - 1, curr_point[1]],
                      [curr_point[0], curr_point[1] - 1],
                      [curr_point[0] + 1, curr_point[1]]]
            dire = (dire + 3) % 4
            for i in range(4):
                move = movies[dire]
                if (image[move[0], move[1]] == 255):
                    perv_p = curr_point.copy()
                    curr_point[0], curr_point[1] = move[0], move[1]
                else:
                    dire = (dire + 1) % 4
            boundry.append(curr_point.copy())
            if (boundry[-1] == p1 and boundry[-2] == p0):
                break
        return boundry