from PyQt5 import QtWidgets,Qt,QtCore,QtGui,QtMultimedia
from randomdots import RandomDots
import time
import numpy as np
import pandas as pd
import datetime


class StimGen(QtWidgets.QLabel):
    def __init__(self,parent = None,dots = [10,15]):
        QtWidgets.QLabel.__init__(self,parent)
        self.setFixedSize(900,300)
        self.leftdots = RandomDots(self)
        self.rightdots = RandomDots(self)
        self.leftdots.setNumber(dots[0])
        self.rightdots.setNumber(dots[1])
        self.leftdots.hide()
        self.rightdots.hide()

        self.mosaic = QtWidgets.QLabel(self)
        self.mosaic.setStyleSheet("border: 2px solid rgb(150,150,150);background-color: rgb(150,150,150)")

        self.timerleft = QtCore.QTimer(self)
        self.timerleft.timeout.connect(self.moveleftdots)

        self.timerright = QtCore.QTimer(self)
        self.timerright.timeout.connect(self.moverightdots)

        self.timertarget = QtCore.QTimer(self)
        self.starttime = time.time()
        self.answer = 0



        self.Arith = 1  # 1 subtraction, 0 addition
        #self.bFinished = False

    def start(self):
        self.leftdots.show()
        self.show()
        #print(self.totalnumber)
        self.timerleft.start(1000)

    def showEvent(self, event):
        self.leftdots.setGeometry(Qt.QRect(0,0,self.width()/3,self.height()))
        if self.Arith == 0:
            self.rightdots.setGeometry(Qt.QRect(self.width()*2/3,0,self.width()/3,self.height()))
        else:
            self.rightdots.setGeometry(Qt.QRect(self.width()/3,0,self.width()/3,self.height()))
        self.mosaic.setGeometry(self.width()/3,0,self.width()/3,self.height())



    def setArtic(self, n=0):
        self.Arith = n
        self.update()

    def moveleftdots(self):
        if self.leftdots.pos().x() < self.width()/3:
            x = self.leftdots.pos().x()
            self.leftdots.move(x+10,0)
            #print("left x = ",x)
            self.timerleft.start(10)
            #print("left :", time.time() - self.starttime)
        else:
            self.timerleft.stop()
            self.leftdots.hide()
            self.rightdots.show()
            if self.Arith == 0:
                self.timerright.start(1000)
            else:
                self.timerright.start(0)
            #print("left done")

    def moverightdots(self):
        if self.Arith == 0:
            if self.rightdots.pos().x() > self.width()/3:
                x = self.rightdots.pos().x()
                self.rightdots.move(x-10,0)
                #print("right x = ", x)
                self.timerright.start(10)
                #print("right :", time.time() - self.starttime)
            else:
                self.timerright.stop()
                self.rightdots.hide()
                #self.bFinished = True
                self.timertarget.start(100)
                #print("right done")
        else:
            if self.rightdots.pos().x() < self.width()*2/3:
                x = self.rightdots.pos().x()
                self.rightdots.move(x+10,0)
                #print("right x = ", x)
                self.timerright.start(10)
                #print("right :", time.time() - self.starttime)
            else:
                self.timerright.stop()
                time.sleep(1)
                self.rightdots.hide()
                #self.bFinished = True
                self.timertarget.start(100)
                #print("right done")


# Training Approximate Number System with dots addition and subtraction
class Exp(QtWidgets.QWidget):
    def __init__(self,parent = None, difficulty = 1.5, practice = 10):
        QtWidgets.QWidget.__init__(self,parent)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, 900, 700)
        self.move(screen.width() / 2 - self.width() / 2, screen.height() / 2 - self.height() / 2)

        self.genStim(practice)
        self.tmStim = QtCore.QTimer(self)
        self.tmStim.timeout.connect(self.StimShow)

        self.tmCue = QtCore.QTimer(self)
        self.tmCue.timeout.connect(self.CueShow)

        self.tmBlank = QtCore.QTimer(self)
        self.tmBlank.timeout.connect(self.BlankShow)

        self.lbCue = QtWidgets.QLabel(self)
        self.lbCue.setFixedSize(300, 300)
        self.lbCue.move((self.width() - self.lbCue.width()) / 2, (150 - self.lbCue.height() / 2))
        self.lbCue.setText("+")
        self.lbCue.setAlignment(Qt.Qt.AlignCenter)
        self.lbCue.setFont(QtGui.QFont("Arial", 20))

        self.lbCue.hide()

        self.sounds = {"C": QtMultimedia.QSound("highpitch.wav"), "W": QtMultimedia.QSound("lowpitch.wav")}
        #self.tmTarget = QtCore.QTimer(self)
        #self.tmTarget.timeout.connect(self.TargetShow)

        self.lbIntro = QtWidgets.QLabel(self)
        self.lbIntro.setTextFormat(Qt.Qt.RichText)
        self.lbIntro.setText('<pre>            <font size=18>欢迎参加数量计算练习实验</font><br /> <br />'
                             '    计算练习包括了加法和减法，每次练习开始时会提示<span style="color: #ff0000;">加法</span>还是'
                             '<span style="color: #ff0000;">减法</span>计算。<br />    加法计算时，首先在左侧呈现一组散点，'
                             '随后移动至中间区域，之后再右侧呈现一组<br />散点，随后也移动到中间区域。<br />    减法计算时，'
                             '首先在左侧呈现一组散点，随后移动至中央区域，之后从该区域移出若<br />干散点。<br />'
                             '    两者均要求判断在中间区域的<span style="color: #ff0000;">散点数量(目标)</span>。在散点呈现之后，'
                             '会在下方出现备选答案。<br />分成两种条件，如只出现一组散点，则要求判断数量的多少，如比目标少，'
                             '则按<span style="color: #ff0000;">"F"键</span>，<br />多则按<span style="color: #ff0000;">"J"键</span>。'
                             '如出现两组散点，怎要求判断那一侧与目标相同，左侧按"F"键，右侧按"J"键。<br /><br />    理解无误后,按回车键开始"</pre>')
        self.lbIntro.setFont(QtGui.QFont("Arial",20))
        self.lbIntro.setGeometry(0,0,800,600)
        self.lbIntro.move(self.width()/2-self.lbIntro.width()/2,self.height()/2 - self.lbIntro.height()/2)
        self.lbIntro.show()
        self.round = 0
        self.bStart = False
        self.bResponse = False
        self.difficulty = difficulty  #设置任务难度，即目标散点和备选散点之间的比率，数值越高难度越小



        self.ResponseData = []
        self.iData={}
        self.Rt = QtCore.QElapsedTimer()

    def setDiffcuty(self,n):
        self.difficulty = n


    def showEvent(self, event):
        while True:
            text, ok = QtWidgets.QInputDialog.getText(self, ("数量练习"), ("输入第几轮练习"), QtWidgets.QLineEdit.Normal, "")
            if not ok:
                continue
            try:
                self.filename = text
                if self.filename:
                    break
            except:
                print("wrong")

    def genStim(self, num = 10):
        self.stimlist = []
        n = int(num/2)
        dots = np.random.randint(5, 20, size=[n, 2])
        for i in range(n):
            self.stimlist.append(StimGen(self, dots[i]))
            self.stimlist[i].move((self.width()-self.stimlist[i].width())/2,0)
            self.stimlist[i].setArtic(0)
            self.stimlist[i].answer = dots[i][0] + dots[i][1]
            self.stimlist[i].hide()
        ldot = np.random.randint(9,20, size = n)
        rdot = []
        for i in ldot:
            rdot.append(np.random.randint(4,i-4))
        rdot = np.array(rdot)
        dots = np.stack([ldot,rdot],axis=1)
        for i in range(n):
            self.stimlist.append(StimGen(self, dots[i]))
            self.stimlist[i+n].move((self.width() - self.stimlist[i].width()) / 2, 0)
            # print(int(i%2))
            self.stimlist[i+n].setArtic(1)
            self.stimlist[i+n].answer = dots[i][0] - dots[i][1]
            #print(self.stimlist[i].Artic)
            self.stimlist[i+n].hide()
        np.random.shuffle(self.stimlist)
        self.type = ['more','less'] * n
        np.random.shuffle(self.type)
        self.targettype = ['one','two'] * n


    def CueShow(self):
        if self.stimlist[self.round].Arith == 0:
            self.lbCue.setText("加法")
        else:
            self.lbCue.setText("减法")
        self.lbCue.show()
        self.tmStim.start(500)
        self.tmCue.stop()


    def StimShow(self):
        print("round = ",self.round)
        self.iData['round'] = self.round
        self.iData['type'] = self.stimlist[self.round].Arith # 0 for addition; 1 for subtraction
        self.lbCue.hide()
        self.stimlist[self.round].start()
        if self.stimlist[self.round].Arith == 0:
            print(self.stimlist[self.round].leftdots.number, " + " , self.stimlist[self.round].rightdots.number,
               " = ", self.stimlist[self.round].answer)
        else:
            print(self.stimlist[self.round].leftdots.number, " - ", self.stimlist[self.round].rightdots.number,
                  " = ", self.stimlist[self.round].answer)

        self.stimlist[self.round].timertarget.timeout.connect(self.TargetShow)
        #self.tmTarget.start(200)
        self.tmStim.stop()

    def TargetShow(self):
        self.stimlist[self.round].timertarget.stop()
        self.bResponse = True
        self.Distract = RandomDots(self)
        if self.targettype[self.round] == "one":
            self.iData['targettype'] = 'one'
            self.Target = RandomDots(self)
            if self.type[self.round] == 'more':
                self.Target.setNumber(int(self.stimlist[self.round].answer * self.difficulty))
                self.iData['condition'] = 'more'

                print('more')
            else:
                self.Target.setNumber(int(self.stimlist[self.round].answer/self.difficulty))
                self.iData['condition'] = 'less'
                print('less')
            print('Target number: ',self.Target.number)
            self.iData['targettype'] = 'one'
            self.Target.setGeometry(Qt.QRect(0,0,300,300))
            self.Target.move(self.width() / 2 - self.Target.width() / 2, self.height() - self.Target.height())
            self.Target.show()
            if self.Rt.isValid():
                self.Rt.restart()
            else:
                self.Rt.start()
        else:
            self.iData['targettype'] = 'two'
            self.Target = RandomDots(self,self.stimlist[self.round].answer)
            self.Distract = RandomDots(self)
            if self.type[self.round] == "more":
                self.Distract.setNumber(int(self.stimlist[self.round].answer * self.difficulty))
                self.iData['condition'] = 'more'
                print("more")
            else:
                self.Distract.setNumber(int(self.stimlist[self.round].answer/self.difficulty))
                self.iData['condition'] = 'less'
                print('less')
            self.targetpos = np.random.choice(["left","right"])

            if self.targetpos == 'left':
                self.Target.setGeometry(0,0,300,300)
                self.Target.move(0,self.height()-300)
                self.Distract.setGeometry(0,0,300,300)
                self.Distract.move(self.width()-300, self.height()-300)
            else:
                self.Target.setGeometry(0,0,300,300)
                self.Target.move(self.width()-300,self.height()-300)
                self.Distract.setGeometry(0,0,300,300)
                self.Distract.move(0,self.height()-300)
            print('Target number: ', self.Target.number)
            self.Target.show()
            self.Distract.show()
            if self.Rt.isValid():
                self.Rt.restart()
            else:
                self.Rt.start()


    def BlankShow(self):
        print(self.iData)
        self.ResponseData.append(self.iData)
        self.iData = {}
        self.round += 1
        if self.round < len(self.stimlist):
            self.tmCue.start(500)
        else:
            self.lbCue.setText("练习结束，谢谢")
            output = pd.DataFrame(self.ResponseData)
            output = output.set_index('round')
            now = datetime.datetime.now()
            output.to_csv(now.strftime("%Y-%m-%d-") + self.filename + "-round.csv")
            diff = self.difficulty
            if "T" not in np.array(output.loc[:,"isCorrect"]):
                diff += 0.2
            else:
                freq = output.groupby("isCorrect").count()
                corpert = freq.loc['T'].iloc[1] / len(output)
                if corpert >= 0.85:
                    diff = diff - 0.1
                elif corpert < 0.75:
                    diff = diff + 0.1

            with open("difficuty.txt","a") as f:
                f.write(str(diff) + '\n')

            self.lbCue.show()
        self.tmBlank.stop()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            if not self.bStart:
                self.tmCue.start(0)
                self.lbIntro.hide()
                self.bStart = True

        if event.key() == QtCore.Qt.Key_F:
            if self.round < len(self.stimlist):
                if self.bResponse:
                    self.bResponse = False
                    self.stimlist[self.round].hide()
                    if self.Distract:
                        self.Distract.hide()
                    self.Target.hide()
                    self.tmBlank.start(0)
                    self.iData["RT"] = self.Rt.elapsed()
                    if self.targettype[self.round] == 'one':
                        if self.type[self.round] == 'more':
                            self.iData['isCorrect'] = 'F'
                            self.sounds["W"].play()
                        else:
                            self.iData['isCorrect'] = 'T'
                            self.sounds["C"].play()
                    elif self.targettype[self.round] == 'two':
                        if self.targetpos == 'left':
                            self.iData['isCorrect'] = "T"
                            self.sounds["C"].play()
                        elif self.targetpos == 'right':
                            self.iData['isCorrect'] = 'F'
                            self.sounds["W"].play()
                        else:
                            print('wrong in target position')
                else:
                    print("Response is not allowed")

        if event.key() == QtCore.Qt.Key_J:
            if self.round < len(self.stimlist):
                if self.bResponse:
                    self.bResponse = False
                    if self.Distract:
                        self.Distract.hide()
                    self.stimlist[self.round].hide()
                    self.Target.hide()
                    self.iData["RT"] = self.Rt.elapsed()
                    self.tmBlank.start(0)

                    if self.targettype[self.round] == 'one':
                        if self.type[self.round] == 'less':
                            self.iData['isCorrect'] = 'F'
                            self.sounds["W"].play()
                        else:
                            self.iData['isCorrect'] = 'T'
                            self.sounds["C"].play()
                    elif self.targettype[self.round] == 'two':
                        if self.targetpos == 'left':
                            self.iData['isCorrect'] = "F"
                            self.sounds["W"].play()
                        elif self.targetpos == 'right':
                            self.iData['isCorrect'] = 'T'
                            self.sounds["C"].play()
                        else:
                            print('wrong in target position')
                else:
                    print("Response is not allowed")

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    import sys
    import os

    app = QtWidgets.QApplication(sys.argv)
    path = os.getcwd()
    with open(os.path.join(path,"difficuty.txt"),'r') as f:
        data = f.read()
        dif = float(data.strip('\n').strip().split('\n')[-1])
        print(dif)
    with open(os.path.join(path,"parameters"),'r') as f:
        data = f.read()
        numbers = float(data)
        print(numbers)
    win = Exp(difficulty=dif,practice=numbers)

    win.show()
    sys.exit(app.exec_())