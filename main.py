import sys, os, serial, time
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QProgressBar
from PyQt5.QtCore import *
from PyQt5.QtGui import QCursor

if getattr(sys, 'frozen', False):
        curr_path = os.path.dirname(sys.executable)
elif __file__:
        curr_path = os.path.dirname(__file__)

try:
    ser = serial.Serial("COM6", 9600)

    class ProgressBar_(QProgressBar):
        def __init__(self, parent=None):
            super().__init__(parent)
            self._active = False
            self.setOrientation(QtCore.Qt.Vertical)
            self.setFormat("%p")
            self.setGeometry(0,0,25,389)
            self.setStyleSheet("""QProgressBar {background-color: rgb(98, 114, 164);color: rgb(200, 200, 200);border-style: none;border-radius: 10px;text-align: center;}QProgressBar::chunk{border-radius: 10px;background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(254, 121, 199, 255), stop: 1 rgba(170, 85, 255, 255));} QProgressBar:focus{outline: 0;border:none;}""")

        def updateTemp(self, temp, flag):
            if flag==0:
                self.setMaximum(100)
                self.setValue(temp)
            else:
                temp=((temp*(9/5))+32)
                self.setValue(int(temp))
            QApplication.processEvents()

        def updateHum(self, hum):
            self.setValue(hum)
            QApplication.processEvents()

    class Display(QMainWindow):
        def __init__(self):
            super(Display, self).__init__()
            loadUi(os.path.join(curr_path,'display.ui'), self)
            self.label_2.setText("Temperature")
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.label1 = ProgressBar_()
            self.label2 = ProgressBar_()

            scene1 = QtWidgets.QGraphicsScene(self.graphicsView_1)
            self.graphicsView_1.setScene(scene1)
            proxy1 = QtWidgets.QGraphicsProxyWidget()

            scene2 = QtWidgets.QGraphicsScene(self.graphicsView_2)
            self.graphicsView_2.setScene(scene2)
            proxy2 = QtWidgets.QGraphicsProxyWidget()

            proxy1.setWidget(self.label1)
            proxy2.setWidget(self.label2)

            scene1.addItem(proxy1)
            scene2.addItem(proxy2)

            self.timer = QTimer()
            self.timer.timeout.connect(self.update)
            self.timer.start(35)
            self.Celsius.setChecked(True)

        def update(self):
            while 1:
                time.sleep(0.1)
                value = ser.readline().decode()
                print(value)
                if ((value[3:5].isdigit()) and (value[9:11].isdigit())):
                    temp = int(value[9:11])
                    if self.Celsius.isChecked():
                        self.label1.updateTemp(temp,0)
                    elif self.Farenheit.isChecked():
                        self.label1.updateTemp(temp,1)
                    hum = int(value[3:5])
                    self.label2.updateHum(hum)
                else:
                    print("Check your connections and retry!")
                    break
                
            
        def mousePressEvent(self, event):
            if event.button()==Qt.LeftButton:
                self.m_flag=True
                self.m_Position=event.globalPos()-self.pos() #Get the position of the mouse relative to the window
                event.accept()
                self.setCursor(QCursor(Qt.OpenHandCursor)) #Change the mouse icon
                
        def mouseMoveEvent(self, QMouseEvent):
            if Qt.LeftButton and self.m_flag:  
                self.move(QMouseEvent.globalPos()-self.m_Position)#Change window position
                QMouseEvent.accept()
                
        def mouseReleaseEvent(self, QMouseEvent):
            self.m_flag=False
            self.setCursor(QCursor(Qt.ArrowCursor))

    def main():
        global app
        app = QApplication(sys.argv)
        disp = Display()
        disp.show()
        sys.exit(app.exec_())

    if __name__ == '__main__':
        main()

except serial.serialutil.SerialException:
    print("Arduino not connected....")