#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import csv
import random
from PyQt5 import QtGui, QtWidgets, QtCore, QtMultimedia


class ExperimentRecorder(QtWidgets.QWidget):
    def __init__(self, participant, experiments, delay, app):
        super().__init__()
        self.app = app
        self.participant = participant
        self.experiments = experiments
        self.delay = int(delay)
        self.counter = -1
        self.cleanwindow = False
        self.timer = QtCore.QElapsedTimer()
        self.timer.start()
        self.player = QtMultimedia.QSound("whitenoise.wav")
        self.initUI()

        self.colours = ["Red", "Green"]
        self.englishWords = ["tree", "egg", "file", "mushroom", "list", "example", "rectangle", "holy", "adventure",
                             "chair", "mouth", "bottle", "keyboard"]
        self.germanWords = ["baum", "ei", "datei", "pilz", "liste", "beispiel", "rechteck", "heilig", "abenteuer",
                            "stuhl", "mund", "flasche", "tastatur"]
        self.log = [
            ["PID", "Stimulus", "Attentive", "Distraction", "Key", "Correct", "Timestamp", "Reactiontime"]]

        self.stimulus = "Experiment start"
        self.attentive = False
        self.distraction = False

    def log_time(self, buttonPressed):
        time_pressed_ms = QtCore.QTime.currentTime().msec()
        time_pressed_s = QtCore.QTime.currentTime().second()
        time_pressed_m = QtCore.QTime.currentTime().minute()
        time_pressed_h = QtCore.QTime.currentTime().hour()
        timestamp = time_pressed_h * 3600000 + time_pressed_m * 60000 + time_pressed_s * 1000 + time_pressed_ms
        if not self.attentive:
            if self.stimulus == 'Green' and buttonPressed == 'P':
                correct = True
            elif self.stimulus == 'Red' and buttonPressed == 'Q':
                correct = True
            else:
                correct = False
        else:
            if self.stimulus in self.englishWords and buttonPressed == 'Q':
                correct = True
            elif self.stimulus in self.germanWords and buttonPressed == 'P':
                correct = True
            else:
                correct = False
        self.log.append(
            [self.participant, self.stimulus, self.attentive, self.distraction, buttonPressed, correct, timestamp,
             self.timer.elapsed()])

    def output_log(self):
        with open("output.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.log)
        sys.exit(self.app.exec_())

    def initUI(self):
        # set the text property of the widget we are inheriting
        self.setGeometry(0, 0, 600, 600)
        self.setWindowTitle('ExperimentRecorder')
        # widget should accept focus by click and tab key
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show()

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Q:
            self.log_time('Q')
        elif ev.key() == QtCore.Qt.Key_P:
            self.log_time('P')
        self.cleanwindow = True
        self.update()

        QtCore.QTimer.singleShot(self.delay, self.nextExperiment)

    def nextExperiment(self):
        print("Hi?")
        self.counter += 1
        self.cleanwindow = False
        self.timer.start()
        if self.counter == len(self.experiments):
            self.output_log()
        else:
            if self.experiments[self.counter][1] == 'D':
                self.distraction = True
                self.player.play()
            else:
                self.distraction = False
                self.player.stop()
            self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRect(event, qp)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        if not self.cleanwindow:
            if self.counter == -1:
                qp.setPen(QtGui.QColor("Black"))
                qp.setFont(QtGui.QFont('Decorative', 24))
                qp.drawText(event.rect(), QtCore.Qt.AlignHCenter, "Press Q or P to start!")
            elif self.experiments[self.counter][0] == 'A':
                self.attentive = True
                qp.setPen(QtGui.QColor("Black"))
                qp.setFont(QtGui.QFont('Decorative', 24))
                qp.drawText(event.rect(), QtCore.Qt.AlignHCenter, "Press Q for english, or P for german.")
                qp.setPen(QtGui.QColor("Black"))
                qp.setFont(QtGui.QFont('Decorative', 32))
                if random.randint(0, 1):
                    random_word = random.choice(self.englishWords)
                    self.stimulus = random_word
                    qp.drawText(event.rect(), QtCore.Qt.AlignCenter, random_word)
                else:
                    random_word = random.choice(self.germanWords)
                    self.stimulus = random_word
                    qp.drawText(event.rect(), QtCore.Qt.AlignCenter, random_word)
            elif self.experiments[self.counter][0] == 'P':
                self.attentive = True
                qp.setPen(QtGui.QColor("Black"))
                qp.setFont(QtGui.QFont('Decorative', 24))
                qp.drawText(event.rect(), QtCore.Qt.AlignHCenter, "Press Q for Red, or P for Green.")
        else:
            qp.setPen(QtGui.QColor("Black"))
            qp.setFont(QtGui.QFont('Decorative', 24))
            qp.drawText(event.rect(), QtCore.Qt.AlignHCenter, "Get ready for the next one...")

    def drawRect(self, event, qp):
        if not self.cleanwindow:
            if self.counter > -1 and self.experiments[self.counter][0] == 'P':
                self.attentive = False
                rect = QtCore.QRect(250, 250, 100, 100)
                if random.randint(0, 1):
                    self.stimulus = "Green"
                    qp.setBrush(QtGui.QColor("Green"))
                else:
                    self.stimulus = "Red"
                    qp.setBrush(QtGui.QColor("Red"))
                qp.drawRoundedRect(rect, 10.0, 10.0)
        else:
            rect = QtCore.QRect(0, 0, 600, 600)
            qp.setBrush(QtGui.QColor("White"))
            qp.drawRect(rect)


def main():
    app = QtWidgets.QApplication(sys.argv)
    input = open(sys.argv[1], "r")
    values = []
    for i in input.readlines():
        values.append(i.split(":", 1)[1].replace('\n', '').replace(' ', ''))
    # variable is never used, class automatically registers itself for Qt main loop:
    space = ExperimentRecorder(values[0], values[1].split(','), values[2], app)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
