from PyQt5 import QtWidgets, QtGui, Qt
import random
import numpy as np


from PyQt5.Qt import QFrame


def compare(icircle, circles):
    for i in range(len(circles)):
        z1 = complex(icircle['real'],icircle['img'])
        z2 = complex(circles[i]['real'],circles[i]['img'])
        if abs(z1-z2) < (icircle['r'] + circles[i]['r']):
            return False
    else:
        return True

def incircle(icicle, x, y, d):
    point0 = complex(x,y)
    point1 = complex(icicle['real'],icicle['img'])
    if abs(point0-point1) <= d:
        return True
    else:
        return False

class RandomDots(QtWidgets.QLabel):
    '''
    Create random dots
    '''
    def __init__(self, parent=None, n=15, color = QtGui.QColor(100,100,100) , size = 10, std = 0):
        QtWidgets.QLabel.__init__(self, parent)
        self.setGeometry(100,100,300,300)
        self.size = size
        self.number = n
        self.deviation = std  # self.size/4
        self.color = color
        self.position()
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet("border: 0px solid rgb(100,100,100)")

    def position(self):
        isize = np.random.normal(self.size, self.deviation, self.number)
        self.positions = []
        ix = random.randint(self.size * 2, self.width() - self.size * 2)
        iy = random.randint(self.size * 2, self.height() - self.size * 2)
        r = isize[0]
        ipos = {'real': ix, 'img': iy, 'r': r}

        self.positions.append(ipos)
        #print("number: {}, ipos = {}".format(0, ipos))

        for i in range(self.number - 1):
            times = 0
            while True:
                ix = random.randint(self.size * 2, self.width() - self.size * 2)
                iy = random.randint(self.size * 2, self.height() - self.size * 2)
                r = isize[i + 1]
                ipos = {'real': ix, 'img': iy, 'r': r}
                #print("number: {}, ipos = {}".format(i + 1, ipos))
                if incircle(ipos, self.width() / 2, self.height() / 2, self.width() / 2 - ipos['r']):
                    if compare(ipos, self.positions):
                        self.positions.append(ipos)
                        break
                    times += 1
                    if times > 1000:
                        print(times)
                        break

    def resizeEvent(self, event):
        QtWidgets.QLabel.resizeEvent(self,event)
        self.position()

    def setColor(self, color=QtGui.QColor(0, 255, 0)):
        self.color = color
        # self.position()
        self.update()

    def setSize(self, size):
        self.size = size
        # self.position()
        self.update()

    def setNumber(self, number):
        self.number = number
        # self.position()
        self.update()

    def setDeviation(self, dev):
        self.deviation = dev
        # self.position()
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawdots(qp, self.color, self.size, self.deviation, self.number)
        qp.end()

    def drawdots(self, qp, color, size, dev, number):
        qp.setPen(color)
        qp.setBrush(color)
        for i in range(number):
            qp.drawEllipse(self.positions[i]['real'], self.positions[i]['img'], self.positions[i]['r'], self.positions[i]['r'])


if __name__ == '__main__':
    import sys
    import time

    app = 0
    app = QtWidgets.QApplication(sys.argv)
    Desktop = QtWidgets.QApplication.desktop().screenGeometry(1)

    rd = RandomDots()
    rd.move(Desktop.left(),Desktop.top())
    rd.setSize(20)
    rd.setNumber(20)
    rd.setColor(QtGui.QColor(255, 0, 0))
    rd.show()
    # app.exec_()
    sys.exit(app.exec_())
