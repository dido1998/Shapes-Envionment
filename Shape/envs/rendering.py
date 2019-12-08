import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QPolygon
from PyQt5.QtCore import QPoint, QSize, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QFrame


class Window(QMainWindow):
    """
    Simple application window to render the environment into
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Shape Gym Environment')

        # Image label to display the rendering
        self.imgLabel = QLabel()
        self.imgLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        # Text box for the mission
        self.missionBox = QTextEdit()
        self.missionBox.setReadOnly(True)
        self.missionBox.setMinimumSize(400, 100)

        # Center the image
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.imgLabel)
        hbox.addStretch(1)

        # Arrange widgets vertically
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.missionBox)

        # Create a main widget for the window
        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)
        mainWidget.setLayout(vbox)

        # Show the application window
        self.show()
        self.setFocus()

        self.closed = False

        # Callback for keyboard events
        self.keyDownCb = None

    def closeEvent(self, event):
        self.closed = True

    def setPixmap(self, pixmap):
        self.imgLabel.setPixmap(pixmap)

    def setText(self, text):
        self.missionBox.setPlainText(text)

    def setKeyDownCb(self, callback):
        self.keyDownCb = callback

    def getKeyName(self, key):
        if key == Qt.Key_Left:
            keyName = 'LEFT'
        elif key == Qt.Key_Right:
            keyName = 'RIGHT'
        elif key == Qt.Key_Up:
            keyName = 'UP'
        elif key == Qt.Key_Down:
            keyName = 'DOWN'
        elif key == Qt.Key_1:
            keyName = 'ONE'
        elif key == Qt.Key_2:
            keyName = 'TWO'
        elif key == Qt.Key_3:
            keyName = 'THREE'
        elif key == Qt.Key_4:
            keyName = 'FOUR'

    def keyPressEvent(self, events):
        if self.keyDownCb == None:
            return

        keyName = None
        assert instanceof(e, list)
        action = [0,0]
        for event in events:
            keyName = getKeyName(event)
            if keyName == 'RIGHT':
                action[1] = 1
            elif keyName == 'DOWN':
                action[1] = 2
            elif keyName == 'LEFT':
                action[1] = 3
            elif keyName == 'UP':
                action[1] = 4
            elif keyName == 'ONE':
                action[0] = 0
            elif keyName == 'TWO':
                action[1] = 1
            elif keyName == 'THREE':
                action[1] = 2
            elif keyName == 'FOUR':
                action[1] = 3 
        
    self.keyDownCb(action)

class Renderer:
    def __init__(self, width, height, ownWindow=False):
        self.width = width
        self.height = height

        self.img = QImage(width, height, QImage.Format_RGB888)
        self.painter = QPainter()

        self.window = None
        if ownWindow:
            self.app = QApplication([])
            self.window = Window()

    def close(self):
        """
        Deallocate resources used
        """
        pass

    def beginFrame(self, shape_map, positions):
        self.bytesPerLine = 3 * self.im_np.shape[1]
        self.img = QImage(shape_map, shape_map.shape[0], shape_map.shape[1], bytesPerLine, QImage.Format_RGB888)
        self.painter.begin(self.img)
        self.painter.setRenderHint(QPainter.Antialiasing, False)
        # Clear the background
        self.qrect = []
        self.painter.setBrush(QColor(1, 1, 1))
        for p in positions:
            self.qrect.append(QRect(p[0], p[1], 5, 5))
            self.painter.drawRect(self.qrect[-1])

    def endFrame(self):
        self.painter.end()

        if self.window:
            if self.window.closed:
                self.window = None
            else:
                self.window.setPixmap(self.getPixmap())
                self.app.processEvents()

    def getPixmap(self):
        return QPixmap.fromImage(self.img)

    def getArray(self):
        """
        Get a numpy array of RGB pixel values.
        The array will have shape (height, width, 3)
        """

        numBytes = self.width * self.height * 3
        buf = self.img.bits().asstring(numBytes)
        output = np.frombuffer(buf, dtype='uint8')
        output = output.reshape((self.height, self.width, 3))

        return output

    def push(self):
        self.painter.save()

    def pop(self):
        self.painter.restore()

    def rotate(self, degrees):
        self.painter.rotate(degrees)

    def translate(self, ind, x, y):
        self.qrect[ind].translate(x, y)
        self.window.update()

    def scale(self, x, y):
        self.painter.scale(x, y)

    def setLineColor(self, r, g, b, a=255):
        self.painter.setPen(QColor(r, g, b, a))

    def setColor(self, r, g, b, a=255):
        self.painter.setBrush(QColor(r, g, b, a))

    def setLineWidth(self, width):
        pen = self.painter.pen()
        pen.setWidthF(width)
        self.painter.setPen(pen)

    def drawLine(self, x0, y0, x1, y1):
        self.painter.drawLine(x0, y0, x1, y1)

    def drawCircle(self, x, y, r):
        center = QPoint(x, y)
        self.painter.drawEllipse(center, r, r)

    def drawPolygon(self, points):
        """Takes a list of points (tuples) as input"""
        points = map(lambda p: QPoint(p[0], p[1]), points)
        self.painter.drawPolygon(QPolygon(points))

    def drawPolyline(self, points):
        """Takes a list of points (tuples) as input"""
        points = map(lambda p: QPoint(p[0], p[1]), points)
        self.painter.drawPolyline(QPolygon(points))

    def fillRect(self, x, y, width, height, r, g, b, a=255):
        self.painter.fillRect(QRect(x, y, width, height), QColor(r, g, b, a))
