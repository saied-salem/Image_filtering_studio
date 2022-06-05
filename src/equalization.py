from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import cv2
import numpy as np
from viewer import Viewer


class Equalizer(qtw.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi("ui/equalization.ui", self)

        self.init_gui()

        self.image_viewer = Viewer()
        self.image_layout.addWidget(self.image_viewer)

        self.equalized_viewer = Viewer()
        self.equalized_layout.addWidget(self.equalized_viewer)

        self.histogram_viewer = Viewer()
        self.histogram_layout.addWidget(self.histogram_viewer)

        self.equalized_histogram = Viewer()
        self.equalized_histogram_layout.addWidget(self.equalized_histogram)

        self.equalizer_btn.clicked.connect(self.equalization)
        self.histogram_btn.clicked.connect(self.view_histogram)

    def init_gui(self):
        self.img = [[]]
        self.equalized_image = [[]]

    def load_original_image(self, image_path):
        self.img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.view_original_image()
        self.equalized_viewer.clear_canvans()
        self.histogram_viewer.clear_canvans()
        self.equalized_histogram.clear_canvans()

    def equalization(self):
        _, indices, counts = np.unique(
            self.img, return_counts=True, return_inverse=True)

        # equalization factor: pixel depth divided by number of pixels of image.
        equalization_factor = 2**8/(self.img.shape[0]*self.img.shape[1])

        commulative_density_function = []

        # to calculate commulative density function (cdf)
        commulative_density_function = np.cumsum(counts)

        Sx = commulative_density_function*equalization_factor-1

        # after equalization --> pixels intensity may have float number ---> this reason for calculate ceiling of number
        Sx = np.ceil(Sx)

        image_1D = Sx

        # to reverse the origin 1d array after equalization
        image_1D = image_1D[indices]

        # to return to original image
        self.equalized_image = np.reshape(
            image_1D, (self.img.shape[0], self.img.shape[1]))

        self.view_equalized_image()

    def view_original_image(self):
        self.image_viewer.draw_image(self.img)

    def view_equalized_image(self):
        self.equalized_viewer.draw_image(self.equalized_image)
        self.equalized_histogram.draw_histogram(self.equalized_image)

    def view_histogram(self):
        self.histogram_viewer.draw_histogram(self.img)

