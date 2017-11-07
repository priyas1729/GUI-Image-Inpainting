import sys

from PyQt5.QtCore import QPoint, Qt, QRect, QSize, pyqtSlot, pyqtRemoveInputHook
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QPushButton, QRadioButton, QGridLayout, \
    QRubberBand, QFileDialog


class ImageProcessor(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('image application')

        self.image1 = Image1()
        self.image1.setMinimumSize(300, 300)
        #self.image1.setPixmap(QPixmap('image1.jpeg'))

        self.image2 = QLabel()
        self.image2.setMinimumSize(300, 300)
        #self.image2.setPixmap(QPixmap('image1.jpeg'))

        uploadButton = QPushButton('upload')
        uploadButton.clicked.connect(self.upload)

        transformButton = QPushButton('transform')
        transformButton.clicked.connect(self.transform)

        self.function1 = QRadioButton('function1')
        self.function1.setChecked(True)
        self.function2 = QRadioButton('function2')
        self.function2.toggled.connect(self.rect_select_visibility)

        grid = QGridLayout()
        grid.addWidget(self.image1, 1, 0)
        grid.addWidget(self.function1, 1, 1)
        grid.addWidget(self.function2, 1, 2)
        grid.addWidget(self.image2, 1, 3)
        grid.addWidget(uploadButton, 2, 0)
        grid.addWidget(transformButton, 2, 3)
        self.setLayout(grid)

        self.show()

    def call_function1(self, coordinates):
        print("executing function 1...")
        print("coordinates are {}".format(coordinates))
        return "image1.jpeg"

    def call_function2(self):
        print("executing function 2...")
        return "image1.jpeg"

    def upload(self):
        # taken from https://pythonspot.com/en/pyqt5-file-dialog/
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, 'Open file', options=options)
        if file:
            print(file)
            self.image1.setPixmap(QPixmap(file))
            print("uploading image...")

    def transform(self):
        if self.function1.isChecked():
            if self.image1.selection_origin is None or self.image1.selection_end is None:
                print("please select a rectangular area.")
            else:
                coordinates = self.get_coordinates(self.image1.selection_origin, self.image1.selection_end)
                transformed_image = self.call_function1(coordinates)
                self.image2.setPixmap(QPixmap(transformed_image))
        else:
            transformed_image = self.call_function2()
            self.image2.setPixmap(QPixmap(transformed_image))


    def get_coordinates(self, origin, end):
        origin = (origin.x(), origin.y())
        end = (end.x(), end.y())
        c3 = (origin.x(), end.y())
        c4 = (end.x(), origin.y())

        return origin, end


    def rect_select_visibility(self):
        if self.function1.isChecked():
            self.image1.selection.show()
        else:
            self.image1.selection.hide()

class Image1(QLabel):
    # taken from https://wiki.python.org/moin/PyQt/Selecting%20a%20region%20of%20a%20widget
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.selection = QRubberBand(QRubberBand.Rectangle, self)
        self.selection_origin = None
        self.selection_end = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selection_origin = QPoint(event.pos())
            self.selection.setGeometry(QRect(self.selection_origin, QSize()))
            self.selection.show()

    def mouseMoveEvent(self, event):
        if not self.selection_origin.isNull():
            self.selection.setGeometry(QRect(self.selection_origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selection_end = QPoint(event.pos())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    imageprocessor = ImageProcessor()
    sys.exit(app.exec_())
