# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication, Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from Ffmpeg import setData

class Stream(QObject):
    newText = pyqtSignal(str) #定义一个发送str的信号
    def write(self, text):
        self.newText.emit(str(text))

class Example(object):

    def setupUi(self, UI):
        UI.setObjectName("UI")
        UI.resize(514, 490)

        # 源文件选择按钮和选择编辑框
        self.source_btn = QtWidgets.QPushButton(UI)
        self.source_btn.setGeometry(QtCore.QRect(20, 40, 93, 28))
        self.source_btn.setObjectName("source_btn")
        self.source_btn.clicked.connect(self.select_source)
        self.source_le = QtWidgets.QLineEdit(UI)
        self.source_le.setGeometry(QtCore.QRect(140, 40, 351, 31))
        self.source_le.setObjectName("source_le")

        # 存储文件选择按钮和选择编辑框
        self.target_btn = QtWidgets.QPushButton(UI)
        self.target_btn.setGeometry(QtCore.QRect(20, 90, 93, 28))
        self.target_btn.setObjectName("target_bth")
        self.target_btn.clicked.connect(self.select_target)
        self.target_le = QtWidgets.QLineEdit(UI)
        self.target_le.setGeometry(QtCore.QRect(140, 90, 351, 31))
        self.target_le.setObjectName("target_le")

        #选择是否开启过程动画按钮
        self.intervals_btn = QtWidgets.QCheckBox(UI)
        self.intervals_btn.setGeometry(QtCore.QRect(320, 140, 111, 31))
        self.intervals_btn.setObjectName("intervals_btn")
        #self.intervals_btn.stateChanged.connect(self.select_intervals)


        #选择处理方法
        self.Method1_btn = QtWidgets.QRadioButton(UI)
        self.Method1_btn.setGeometry(QtCore.QRect(50, 140, 115, 19))
        self.Method1_btn.setObjectName("Method1_btn")
        self.Method2_bth = QtWidgets.QRadioButton(UI)
        self.Method2_bth.setGeometry(QtCore.QRect(50, 170, 115, 19))
        self.Method2_bth.setObjectName("Method2_bth")

        #控制台输出展示
        self.textBrowser = QtWidgets.QTextBrowser(UI)
        self.textBrowser.setGeometry(QtCore.QRect(40, 220, 431, 192))
        self.textBrowser.setObjectName("textBrowser")
        sys.stdout = Stream(newText=self.outputWritten)
        sys.stderr = Stream(newText=self.outputWritten)

        # 执行成功返回值显示位置设置
        self.result_le = QtWidgets.QLabel(UI)
        self.result_le.setGeometry(QtCore.QRect(180, 150, 91, 41))
        self.result_le.setObjectName("result_le")

        # 技术支持框
        self.sourceLabel = QtWidgets.QLabel(UI)
        self.sourceLabel.setGeometry(QtCore.QRect(260, 180, 250, 31))
        self.sourceLabel.setObjectName("sourceLabel")
        self.sourceLabel.setStyleSheet("color:blue;font-size:18px")

        # 保存按钮，调取数据增加函数等
        self.save_btn = QtWidgets.QPushButton(UI)
        self.save_btn.setGeometry(QtCore.QRect(110, 440, 93, 28))
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.addNum)

        # 退出按钮，点击按钮退出整个程序
        self.cancle_btn = QtWidgets.QPushButton(UI)
        self.cancle_btn.setGeometry(QtCore.QRect(290, 440, 93, 28))
        self.cancle_btn.setObjectName("cancle_btn")
        self.cancle_btn.clicked.connect(QCoreApplication.quit)
        self.retranslateUi(UI)
        QtCore.QMetaObject.connectSlotsByName(UI)

    def retranslateUi(self, UI):
        _translate = QtCore.QCoreApplication.translate
        UI.setWindowTitle(_translate("UI", "video binding"))
        self.source_btn.setText(_translate("UI", "source"))
        self.target_btn.setText(_translate("UI", "target"))
        self.intervals_btn.setText(_translate("UI", "intervals"))
        self.Method1_btn.setText(_translate("UI", "method1"))
        self.Method2_bth.setText(_translate("UI", "method2"))
        self.save_btn.setText(_translate("UI", "save"))
        self.cancle_btn.setText(_translate("UI", "cancle"))
        self.sourceLabel.setText(_translate("UI", "Technical support:Bloodkun"))

    # 打开的视频文件路径
    def select_source(self):
        source, sType = QFileDialog.getOpenFileName(self, "select the video directory", "C:/")
        self.source_le.setText(str(source))

    # 保存的视频文件名称，要写上后缀名
    def select_target(self):
        target, fileType = QFileDialog.getSaveFileName(self, "select the save directory", "C:/")
        self.target_le.setText(str(target))

    #将向QtextBrowser中添加信息
    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def addNum(self):
        source = self.source_le.text().strip()  # 获取源视频文件存储地址
        source = source.replace('/', '\\')
        target = self.target_le.text().strip()  # 获取合成视频保存地址
        target = target.replace('/', '\\')
        Intervals = self.intervals_btn.isChecked()
        if Intervals:
            print('choose Intervals')
        else:
            print('no Intervals')
        method = None
        if self.Method1_btn.isChecked():
            method = 1
            print('choose Method1')
        elif self.Method2_bth.isChecked():
            method = 2
            print('choose Method2')
        else:
            exit(-1)

        #视频处理
        setData(source, target, method, Intervals)
        self.result_le.setText("ok!")  # 输出文件后界面返回OK
        self.result_le.setStyleSheet("color:red;font-size:40px")  # 设置OK颜色为红色，大小为四十像素
        self.result_le.setAlignment(Qt.AlignCenter)  # OK在指定框内居中


