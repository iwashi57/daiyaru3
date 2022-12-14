from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt

#from image import Ui_Form
import sys

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import argparse
import cv2 as cv
import numpy as np
import mediapipe as mp
# from utils import CvFpsCalc

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDial, QLabel
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import random
import pyautogui as pyautogui
import time

v= [[] for i in range(11)]
vv = [[] for i in range(3)]
i = 0
a = [1,10,10,10] #桁の前後認証
g1=[125,60,40,80,170,285,370,410,390,330]
g2=[300,235,130,30,-25,-20,35,130,235,300]
x = [10 for i in range (10)] # ダイヤル配置
xx = [10 for i in range (20)] # x逆順
x_2 = [10 for i in range (20)] # x2倍
psw = [6, 2, 3, 5] #パスワード
turn = [1,2,1,2] # 1時計回り 2反時計回り
#dn = random.randint(0,9)
u = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
#ss = [[] for i in range(4)]
s = [2, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10] #周回状況
st = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10] #パスワードスタート地点

style_str = QStyleFactory.keys()[0] #スタイル変更


class Movie(QtWidgets.QDialog):
    def get_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("--device", type=int, default=0)
        parser.add_argument("--width", help='cap width', type=int, default=960)
        parser.add_argument("--height", help='cap height', type=int, default=540)

        parser.add_argument("--model_complexity",
                            help='model_complexity(0,1(default))',
                            type=int,
                            default=1)

        parser.add_argument("--max_num_hands", type=int, default=2)
        parser.add_argument("--min_detection_confidence",
                            help='min_detection_confidence',
                            type=float,
                            default=0.7)
        parser.add_argument("--min_tracking_confidence",
                            help='min_tracking_confidence',
                            type=int,
                            default=0.5)

        parser.add_argument('--use_brect', action='store_true')
        parser.add_argument('--plot_world_landmark', action='store_true')

        args = parser.parse_args()

        return args

    msec = 10  # ms

    def __init__(self, parent=None):
        super(Movie, self).__init__(parent)
        self.setWindowOpacity(0.5)  # ウィンドウ全体を透過
        self.setGeometry(300, 80, 1000, 800) # サイズと位置の固定
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # 最前面

        '''
        self.image_label = QLabel(self)
        # self.setGeometry(0, 0, 850, 500)

        # vboxにQLabelをセット
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        # vboxをレイアウトとして配置
        self.setLayout(vbox)'''
        # self.image_label.setGeometry(10, -200, 900, 1500)
        # self.image_label.setGeometry(0, 0, 0, 0)

        self.capture = cv.VideoCapture(0)
        self.capture.set(cv.CAP_PROP_FRAME_WIDTH, 1500)
        self.capture.set(cv.CAP_PROP_FRAME_HEIGHT, 600)
        if self.capture.isOpened() is False:
            raise ("IO Error")

        '''
        self.scene = QtWidgets.QGraphicsScene()
        self.set()
        '''

        self.setWindowTitle('QDial')  #
        #self.setWindowOpacity(0.5)
        a = 6
        # a = random.randint(0,9)

        self.dial = QDial(self)
        self.dial.setFixedSize(500, 500)  # ダイヤルサイズ
        self.dial.setGeometry(120, 100, 200, 200)  # ダイヤル場所

        self.dial.setRange(0, 9)  # 範囲
        self.dial.setValue(a)  # 始点 = 6

        #self.dial.setStyleSheet('background-color:#0f0d0e; border: 0px;') #色チェンジ
        #self.dial.setStyleSheet('background-color : rgba(255,255,255,128);')  # 色チェンジ
        self.dial.setStyleSheet('opacity:200')  # 色チェンジ

        self.dial.setNotchesVisible(True)  # 目盛り
        self.dial.valueChanged.connect(self.on_change_func)  #
        # self.dial.setSliderPosition(5)

        self.label = QLabel('start', self)
        self.label.setFont(QFont('Arial Black', 20))
        self.label.setGeometry(750, 290, 200, 100)

        self.button_r= QPushButton('Reset', self)
        self.button_r.setFont(QFont('Arial', 20))
        self.button_r.setGeometry(730, 150, 180, 50)

        '''
        self.button_s = QPushButton(' ', self)
        self.button_s.setStyleSheet('background-color : rgba(255,255,255,128);')
        self.button_s.setFont(QFont('Arial Black', 50))
        self.button_s.setGeometry(200, 290, 600, 200) #位置、大きさ
        #最前面に移動したい
        '''


        # self.mutex = QtCore.QMutex()
        # 親ウィンドウ内に対する位置とサイズをそれぞれのボタンに指定
        # ランダム化
        i = 0
        while i != 10:
            a = random.randint(0, 9)
            x[i] = a
            if i >= 1:
                b = i - 1
                for num in range(i):
                    if x[i] == x[b]:
                        i = i - 1
                        break
                    b = b - 1
            i = i + 1
        # print("x", x)
        i = 0
        for i in range(10):
            xx[i] = x[9 - i]
        for i in range(10, 20):
            xx[i] = xx[i - 10]

        for i in range(10):
            x_2[i] = x[i]
        for i in range(10, 20):
            x_2[i] = x[i - 10]

        for k in range(3):
            for i in range(20):
                if turn[k + 1] == 2 and xx[i] == psw[k]:
                    while xx[i] != psw[k + 1]:
                        vv[k].append(xx[i])
                        i = i + 1
                    vv[k].append(xx[i])
                    break
                elif turn[k + 1] == 1 and x_2[i] == psw[k]:
                    while x_2[i] != psw[k + 1]:
                        vv[k].append(x_2[i])
                        i = i + 1
                    vv[k].append(x_2[i])
                    break
        # print("vv", vv)

        # 親ウィジェットを指定して並べるボタンを作成
        self.button0 = QPushButton(str(x[0]), self)
        self.button1 = QPushButton(str(x[1]), self)
        self.button2 = QPushButton(str(x[2]), self)
        self.button3 = QPushButton(str(x[3]), self)
        self.button4 = QPushButton(str(x[4]), self)
        self.button5 = QPushButton(str(x[5]), self)
        self.button6 = QPushButton(str(x[6]), self)
        self.button7 = QPushButton(str(x[7]), self)
        self.button8 = QPushButton(str(x[8]), self)
        self.button9 = QPushButton(str(x[9]), self)

        self.button0.setFont(QFont('Arial', 20))
        self.button1.setFont(QFont('Arial', 20))
        self.button2.setFont(QFont('Arial', 20))
        self.button3.setFont(QFont('Arial', 20))
        self.button4.setFont(QFont('Arial', 20))
        self.button5.setFont(QFont('Arial', 20))
        self.button6.setFont(QFont('Arial', 20))
        self.button7.setFont(QFont('Arial', 20))
        self.button8.setFont(QFont('Arial', 20))
        self.button9.setFont(QFont('Arial', 20))

        self.button0.setGeometry(190, 580, 80, 50)
        self.button1.setGeometry(50, 450, 80, 50)
        self.button2.setGeometry(20, 300, 80, 50)
        self.button3.setGeometry(90, 120, 80, 50)
        self.button4.setGeometry(220, 40, 80, 50)
        self.button5.setGeometry(430, 40, 80, 50)
        self.button6.setGeometry(550, 130, 80, 50)
        self.button7.setGeometry(640, 290, 80, 50)
        self.button8.setGeometry(610, 450, 80, 50)
        self.button9.setGeometry(470, 580, 80, 50)


        #self.button0.setStyleSheet('opacity:200')  # 色チェンジ

        # ボタンをクリック（）内は動作
        '''self.button0.clicked.connect(self.clickCallback_0)'''

        # ラベル作戦
        '''
        self.label_0 = QLabel(str(x[0]), self)
        self.label_1 = QLabel(str(x[1]), self)
        self.label_2 = QLabel(str(x[2]), self)
        self.label_3 = QLabel(str(x[3]), self)
        self.label_4 = QLabel(str(x[4]), self)
        self.label_5 = QLabel(str(x[5]), self)
        self.label_6 = QLabel(str(x[6]), self)
        self.label_7 = QLabel(str(x[7]), self)
        self.label_8 = QLabel(str(x[8]), self)
        self.label_9 = QLabel(str(x[9]), self)

        self.label_0.setFont(QFont('Arial', 20))
        self.label_1.setFont(QFont('Arial', 20))
        self.label_2.setFont(QFont('Arial', 20))
        self.label_3.setFont(QFont('Arial', 20))
        self.label_4.setFont(QFont('Arial', 20))
        self.label_5.setFont(QFont('Arial', 20))
        self.label_6.setFont(QFont('Arial', 20))
        self.label_7.setFont(QFont('Arial', 20))
        self.label_8.setFont(QFont('Arial', 20))
        self.label_9.setFont(QFont('Arial', 20))

        self.label_0.setGeometry(g1[0], g2[0], 170, 100)
        self.label_1.setGeometry(g1[1], g2[1], 170, 100)
        self.label_2.setGeometry(g1[2], g2[2], 170, 100)
        self.label_3.setGeometry(g1[3], g2[3], 170, 100)
        self.label_4.setGeometry(g1[4], g2[4], 170, 100)
        self.label_5.setGeometry(g1[5], g2[5], 170, 100)
        self.label_6.setGeometry(g1[6], g2[6], 170, 100)
        self.label_7.setGeometry(g1[7], g2[7], 170, 100)
        self.label_8.setGeometry(g1[8], g2[8], 170, 100)
        self.label_9.setGeometry(g1[9], g2[9], 170, 100)
        '''


        print("psw", psw)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.set)
        timer.start(self.msec)

    def set(self):
        # 引数解析 #################################################################
        args = self.get_args()

        cap_device = args.device
        cap_width = args.width
        cap_height = args.height

        model_complexity = args.model_complexity

        max_num_hands = args.max_num_hands
        min_detection_confidence = args.min_detection_confidence
        min_tracking_confidence = args.min_tracking_confidence

        use_brect = args.use_brect
        plot_world_landmark = args.plot_world_landmark
        # カメラ準備 ###############################################################
        cap = cv.VideoCapture(cap_device)
        '''
        cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)
        '''
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 5000)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 3000)


        # モデルロード #############################################################
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            # model_complexity=model_complexity,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        # World座標プロット ########################################################
        if plot_world_landmark:
            import matplotlib.pyplot as plt
            fig = plt.figure()
            r_ax = fig.add_subplot(121, projection="3d")
            l_ax = fig.add_subplot(122, projection="3d")
            fig.subplots_adjust(left=0.0, right=1, bottom=0, top=1)

        # FPS計測モジュール ########################################################
        # cvFpsCalc = CvFpsCalc(buffer_len=10)
        while True:
            # カメラキャプチャ #####################################################
            ret, image = self.capture.read()
            if not ret:
                break
            #if ret == False:
            #    return
            #image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            #image = cv.flip(image, 1)  # ミラー表示
            debug_image = copy.deepcopy(image)
            height, width, dim = image.shape

            # 検出実施 #############################################################
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            results = hands.process(image)

            # 描画 ################################################################
            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                      results.multi_handedness):
                    # 手の平重心計算
                    cx, cy = self.calc_palm_moment(debug_image, hand_landmarks)
                    # 外接矩形の計算
                    brect = self.calc_bounding_rect(debug_image, hand_landmarks)
                    # 描画
                    debug_image = self.draw_landmarks(debug_image, cx, cy,
                                                      hand_landmarks, handedness)
                    debug_image = self.draw_bounding_rect(use_brect, debug_image, brect)

            # cv.putText(debug_image, "FPS:" + str(display_fps), (10, 30),
            # cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)

            # キー処理(ESC：終了) #################################################
            key = cv.waitKey(1)
            if key == 27:  # ESC
              #self.QTimer.singleShot(0, window.close)
              exit()
              #break


            # 画面反映 #############################################################
            # img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            # QT側でチャネル順BGRを指定

            qimg = QtGui.QImage(debug_image.tobytes(), debug_image.shape[1], debug_image.shape[0],
                                debug_image.strides[0],
                                QtGui.QImage.Format.Format_BGR888)
            #qimg = qimg.scaled(self.width, self.height, 3000, 2000)
            '''qpix = QPixmap.fromImage(qimg)
            self.image_label.setPixmap(qpix)'''
            cv.imshow('MediaPipe Hand Demo', debug_image)
            '''
            img = cv.cvtColor(debug_image, cv.COLOR_BGR2RGB)
            self.image = QtGui.QImage(img.data, width, height, QtGui.QImage.Format_RGB888)
            self.item = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.image))
            #self.image_label.setPixmap(self,self.item)
            self.scene.clear()
            self.scene.addItem(self.item)
            self.ui.graphicsView.setScene(self.scene)
            cv.imshow('MediaPipe Hand Demo', debug_image)
            '''


        cap.release()
        cv.destroyAllWindows()


    def calc_palm_moment(self,image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        palm_array = np.empty((0, 2), int)

        for index, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            if index == 0:  # 手首1
                palm_array = np.append(palm_array, landmark_point, axis=0)
            if index == 1:  # 手首2
                palm_array = np.append(palm_array, landmark_point, axis=0)
            if index == 5:  # 人差指：付け根
                palm_array = np.append(palm_array, landmark_point, axis=0)
            if index == 9:  # 中指：付け根
                palm_array = np.append(palm_array, landmark_point, axis=0)
            if index == 13:  # 薬指：付け根
                palm_array = np.append(palm_array, landmark_point, axis=0)
            if index == 17:  # 小指：付け根
                palm_array = np.append(palm_array, landmark_point, axis=0)
        M = cv.moments(palm_array)
        cx, cy = 0, 0
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

        return cx, cy

    def calc_bounding_rect(self,image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_array = np.empty((0, 2), int)

        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv.boundingRect(landmark_array)

        return [x, y, x + w, y + h]

    def draw_landmarks(self,image, cx, cy, landmarks, handedness):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # キーポイント
        for index, landmark in enumerate(landmarks.landmark):
            if landmark.visibility < 0 or landmark.presence < 0:
                continue

            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            # landmark_z = landmark.z

            landmark_point.append((landmark_x, landmark_y))

            if index == 8:  # 人差指：指先
                cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
                cv.circle(image, (landmark_x, landmark_y), 12, (0, 255, 0), 2)

        index_finger_pip6_x = int(landmarks.landmark[6].x * image_width)
        index_finger_pip6_y = int(landmarks.landmark[6].y * image_height)
        # 指先の座標
        index_finger_pip8_x = int(landmarks.landmark[8].x * image_width)
        index_finger_pip8_y = int(landmarks.landmark[8].y * image_height)

        # 人差し指の指先が第2関節よりも下に行ったときクリック
        #if index_finger_pip8_y > index_finger_pip6_y:
        # 人差し指の指先が画角に入ったらクリック状態
        if index_finger_pip6_y > 0:
            #pyautogui.mouseDown(index_finger_pip6_x - 7, index_finger_pip6_y + 20) #長押し
            pyautogui.click(index_finger_pip6_x - 7, index_finger_pip6_y + 20) #クリック

            # pyautogui.mouseDown(index_finger_pip8_x - 7, index_finger_pip8_y + 20)
            #pyautogui.click(index_finger_pip6_x, index_finger_pip6_y)

        else:
            # マウスカーソルを中指の動きに合わせて動かす
            pyautogui.moveTo(index_finger_pip6_x - 7, index_finger_pip6_y + 20)
            #pyautogui.moveTo(index_finger_pip8_x - 7, index_finger_pip8_y + 20)
            #pyautogui.moveTo(index_finger_pip6_x, index_finger_pip6_y)

        # 接続線
        if len(landmark_point) > 0:
            # 人差指
            '''
            cv.line(image, landmark_point[5], landmark_point[6], (0, 255, 0), 2)
            cv.line(image, landmark_point[6], landmark_point[7], (0, 255, 0), 2)
            cv.line(image, landmark_point[7], landmark_point[8], (0, 255, 0), 2)
            '''

        # 重心 + 左右
        if len(landmark_point) > 0:
            # handedness.classification[0].index
            # handedness.classification[0].score

            cv.circle(image, (cx, cy), 12, (0, 255, 0), 2)
            cv.putText(image, handedness.classification[0].label[0],
                       (cx - 6, cy + 6), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0),
                       2, cv.LINE_AA)  # label[0]:一文字目だけ

        return image

    def draw_bounding_rect(self,use_brect, image, brect):
        if use_brect:
            # 外接矩形
            cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                         (0, 255, 0), 2)
        return image

    def on_change_func(self):
        sdv = self.dial.value()
        # sdvは座標,x[sdv]は数値,jは何周目か
        k = 0
        l = 0
        for j in range(10):
            if j == 4:
                k = 1
            if j == 7:
                k = 2
            if j == 9:
                k = 3
            if s[j] == 2:
                if x[sdv] == psw[k]:  # 仮
                    s[j] = 1
                    st[j] = sdv
                else:
                    v[j].append(x[sdv])
                    # print("s[j]", s[j])
            if s[j] == 1:  # 現在ダイヤルが指している座標
                if x[sdv] == 0:  # 座標上の数値
                    v[j].append(x[sdv])
                    l = len(v[j])
                    self.clickCallback_0(j, l, st[j], k)
                if x[sdv] == 1:
                    v[j].append(x[sdv])
                    l = len(v[j])
                    self.clickCallback_1(j, l, st[j], k)
                if x[sdv] == 2:
                    v[j].append(x[sdv])
                    l = len(v[j])
                    self.clickCallback_2(j, l, st[j], k)
                if x[sdv] == 3:
                    v[j].append(x[sdv])
                    l = len(v[j])
                    self.clickCallback_3(j, l, st[j], k)
                if x[sdv] == 4:
                    v[j].append(x[sdv])
                    l = len(v[j])
                    self.clickCallback_4(j, l, st[j], k)
                if x[sdv] == 5:
                    v[j].append(x[sdv])
                    l = len(v[j])
                    self.clickCallback_5(j, l, st[j], k)
                if x[sdv] == 6:
                    v[j].append(x[sdv])
                    l = len(v[j])
                    self.clickCallback_6(j, l, st[j], k)
                if x[sdv] == 7:
                    v[j].append(x[sdv])
                    l = len(v[j])
                    self.clickCallback_7(j, l, st[j], k)
                if x[sdv] == 8:
                    v[j].append(x[sdv])
                    l = len(v[j])
                    self.clickCallback_8(j, l, st[j], k)
                if x[sdv] == 9:
                    v[j].append(x[sdv])
                    l = len(v[j])
                    self.clickCallback_9(j, l, st[j], k)

    def clickCallback_0(self, j, l, st, k):  # ボタン0が押されたらやること
        self.label.setText("0")
        '''print("v", v[j])
        print("l", l)
        print("st", st)
        print("k", k)'''

        if k > 0 and vv[k - 1] == v[j]:
            print(k + 1, "桁目認証開始")
            a[k] = 1

        if (st != 0 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st - 1] and turn[k] == 1 and a[k] == 1) or (
                st == 0 and v[j][l - 1] == x[0] and v[j][l - 2] == x[9] and turn[k] == 1 and a[k] == 1):
            print("認証 時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 0 and j == 3:
                print("１桁目認証")
            if k == 2 and j == 8:
                print("３桁目認証")
        if (st != 9 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st + 1] and turn[k] == 2 and a[k] == 1) or (
                st == 9 and v[j][l - 1] == x[9] and v[j][l - 2] == x[0] and turn[k] == 2 and a[k] == 1):
            print("認証 反時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 1 and j == 6:
                print("２桁目認証")
            if k == 3 and j == 9:
                self.label.setText("Success")
                print("認証完了")
                #self.QTimer.singleShot(5000, window.close)
                # self.timer()
                # タイマー設定しようとすると途中で終わってしまう


    def clickCallback_1(self, j, l, st, k):  # ボタン0が押されたらやること
        self.label.setText("1")
        '''print("v", v[j])
                print("l", l)
                print("st", st)
                print("k", k)'''

        if k > 0 and vv[k - 1] == v[j]:
            print(k + 1, "桁目認証開始")
            a[k] = 1

        if (st != 0 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st - 1] and turn[k] == 1 and a[k] == 1) or (
                st == 0 and v[j][l - 1] == x[0] and v[j][l - 2] == x[9] and turn[k] == 1 and a[k] == 1):
            print("認証 時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 0 and j == 3:
                print("１桁目認証")
            if k == 2 and j == 8:
                print("３桁目認証")
        if (st != 9 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st + 1] and turn[k] == 2 and a[k] == 1) or (
                st == 9 and v[j][l - 1] == x[9] and v[j][l - 2] == x[0] and turn[k] == 2 and a[k] == 1):
            print("認証 反時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 1 and j == 6:
                print("２桁目認証")
            if k == 3 and j == 9:
                self.label.setText("Success")
                print("認証完了")
                # self.QTimer.singleShot(5000, window.close)
                # self.timer()
                # タイマー設定しようとすると途中で終わってしまう


    def clickCallback_2(self, j, l, st, k):  # ボタン0が押されたらやること
        self.label.setText("2")
        '''print("v", v[j])
                print("l", l)
                print("st", st)
                print("k", k)'''

        if k > 0 and vv[k - 1] == v[j]:
            print(k + 1, "桁目認証開始")
            a[k] = 1

        if (st != 0 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st - 1] and turn[k] == 1 and a[k] == 1) or (
                st == 0 and v[j][l - 1] == x[0] and v[j][l - 2] == x[9] and turn[k] == 1 and a[k] == 1):
            print("認証 時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 0 and j == 3:
                print("１桁目認証")
            if k == 2 and j == 8:
                print("３桁目認証")
        if (st != 9 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st + 1] and turn[k] == 2 and a[k] == 1) or (
                st == 9 and v[j][l - 1] == x[9] and v[j][l - 2] == x[0] and turn[k] == 2 and a[k] == 1):
            print("認証 反時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 1 and j == 6:
                print("２桁目認証")
            if k == 3 and j == 9:
                self.label.setText("Success")
                print("認証完了")
                # self.QTimer.singleShot(5000, window.close)
                # self.timer()
                # タイマー設定しようとすると途中で終わってしまう

    def clickCallback_3(self, j, l, st, k):  # ボタン0が押されたらやること
        self.label.setText("3")
        '''print("v", v[j])
                print("l", l)
                print("st", st)
                print("k", k)'''

        if k > 0 and vv[k - 1] == v[j]:
            print(k + 1, "桁目認証開始")
            a[k] = 1

        if (st != 0 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st - 1] and turn[k] == 1 and a[k] == 1) or (
                st == 0 and v[j][l - 1] == x[0] and v[j][l - 2] == x[9] and turn[k] == 1 and a[k] == 1):
            print("認証 時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 0 and j == 3:
                print("１桁目認証")
            if k == 2 and j == 8:
                print("３桁目認証")
        if (st != 9 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st + 1] and turn[k] == 2 and a[k] == 1) or (
                st == 9 and v[j][l - 1] == x[9] and v[j][l - 2] == x[0] and turn[k] == 2 and a[k] == 1):
            print("認証 反時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 1 and j == 6:
                print("２桁目認証")
            if k == 3 and j == 9:
                self.label.setText("Success")
                print("認証完了")
                # self.QTimer.singleShot(5000, window.close)
                # self.timer()
                # タイマー設定しようとすると途中で終わってしまう


    def clickCallback_4(self, j, l, st, k):  # ボタン0が押されたらやること
        self.label.setText("4")
        '''print("v", v[j])
                print("l", l)
                print("st", st)
                print("k", k)'''

        if k > 0 and vv[k - 1] == v[j]:
            print(k + 1, "桁目認証開始")
            a[k] = 1

        if (st != 0 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st - 1] and turn[k] == 1 and a[k] == 1) or (
                st == 0 and v[j][l - 1] == x[0] and v[j][l - 2] == x[9] and turn[k] == 1 and a[k] == 1):
            print("認証 時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 0 and j == 3:
                print("１桁目認証")
            if k == 2 and j == 8:
                print("３桁目認証")
        if (st != 9 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st + 1] and turn[k] == 2 and a[k] == 1) or (
                st == 9 and v[j][l - 1] == x[9] and v[j][l - 2] == x[0] and turn[k] == 2 and a[k] == 1):
            print("認証 反時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 1 and j == 6:
                print("２桁目認証")
            if k == 3 and j == 9:
                self.label.setText("Success")
                print("認証完了")
                #self.QTimer.singleShot(5000, window.close)
                # self.timer()
                #タイマー設定しようとすると途中で終わってしまう


    def clickCallback_5(self, j, l, st, k):  # ボタン0が押されたらやること
        self.label.setText("5")
        '''print("v", v[j])
                print("l", l)
                print("st", st)
                print("k", k)'''

        if k > 0 and vv[k - 1] == v[j]:
            print(k + 1, "桁目認証開始")
            a[k] = 1

        if (st != 0 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st - 1] and turn[k] == 1 and a[k] == 1) or (
                st == 0 and v[j][l - 1] == x[0] and v[j][l - 2] == x[9] and turn[k] == 1 and a[k] == 1):
            print("認証 時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 0 and j == 3:
                print("１桁目認証")
            if k == 2 and j == 8:
                print("３桁目認証")
        if (st != 9 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st + 1] and turn[k] == 2 and a[k] == 1) or (
                st == 9 and v[j][l - 1] == x[9] and v[j][l - 2] == x[0] and turn[k] == 2 and a[k] == 1):
            print("認証 反時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 1 and j == 6:
                print("２桁目認証")
            if k == 3 and j == 9:
                self.label.setText("Success")
                print("認証完了")
                # self.QTimer.singleShot(5000, window.close)
                # self.timer()
                # タイマー設定しようとすると途中で終わってしまう


    def clickCallback_6(self, j, l, st, k):  # ボタン0が押されたらやること
        self.label.setText("6")
        '''print("v", v[j])
                print("l", l)
                print("st", st)
                print("k", k)'''

        if k > 0 and vv[k - 1] == v[j]:
            print(k + 1, "桁目認証開始")
            a[k] = 1

        if (st != 0 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st - 1] and turn[k] == 1 and a[k] == 1) or (
                st == 0 and v[j][l - 1] == x[0] and v[j][l - 2] == x[9] and turn[k] == 1 and a[k] == 1):
            print("認証 時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 0 and j == 3:
                print("１桁目認証")
            if k == 2 and j == 8:
                print("３桁目認証")
        if (st != 9 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st + 1] and turn[k] == 2 and a[k] == 1) or (
                st == 9 and v[j][l - 1] == x[9] and v[j][l - 2] == x[0] and turn[k] == 2 and a[k] == 1):
            print("認証 反時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 1 and j == 6:
                print("２桁目認証")
            if k == 3 and j == 9:
                self.label.setText("Success")
                print("認証完了")
                # self.QTimer.singleShot(5000, window.close)
                # self.timer()
                # タイマー設定しようとすると途中で終わってしまう


    def clickCallback_7(self, j, l, st, k):  # ボタン0が押されたらやること
        self.label.setText("7")
        '''print("v", v[j])
                        print("l", l)
                        print("st", st)
                        print("k", k)'''

        if k > 0 and vv[k - 1] == v[j]:
            print(k + 1, "桁目認証開始")
            a[k] = 1

        if (st != 0 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st - 1] and turn[k] == 1 and a[k] == 1) or (
                st == 0 and v[j][l - 1] == x[0] and v[j][l - 2] == x[9] and turn[k] == 1 and a[k] == 1):
            print("認証 時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 0 and j == 3:
                print("１桁目認証")
            if k == 2 and j == 8:
                print("３桁目認証")
        if (st != 9 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st + 1] and turn[k] == 2 and a[k] == 1) or (
                st == 9 and v[j][l - 1] == x[9] and v[j][l - 2] == x[0] and turn[k] == 2 and a[k] == 1):
            print("認証 反時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 1 and j == 6:
                print("２桁目認証")
            if k == 3 and j == 9:
                self.label.setText("Success")
                print("認証完了")
                # self.QTimer.singleShot(5000, window.close)
                # self.timer()
                # タイマー設定しようとすると途中で終わってしまう


    def clickCallback_8(self, j, l, st, k):  # ボタンが押されたらやること
        self.label.setText("8")
        '''print("v", v[j])
                        print("l", l)
                        print("st", st)
                        print("k", k)'''

        if k > 0 and vv[k - 1] == v[j]:
            print(k + 1, "桁目認証開始")
            a[k] = 1

        if (st != 0 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st - 1] and turn[k] == 1 and a[k] == 1) or (
                st == 0 and v[j][l - 1] == x[0] and v[j][l - 2] == x[9] and turn[k] == 1 and a[k] == 1):
            print("認証 時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 0 and j == 3:
                print("１桁目認証")
            if k == 2 and j == 8:
                print("３桁目認証")
        if (st != 9 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st + 1] and turn[k] == 2 and a[k] == 1) or (
                st == 9 and v[j][l - 1] == x[9] and v[j][l - 2] == x[0] and turn[k] == 2 and a[k] == 1):
            print("認証 反時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 1 and j == 6:
                print("２桁目認証")
            if k == 3 and j == 9:
                self.label.setText("Success")
                print("認証完了")
                # self.QTimer.singleShot(5000, window.close)
                # self.timer()
                # タイマー設定しようとすると途中で終わってしまう


    def clickCallback_9(self, j, l, st, k):  # ボタン0が押されたらやること
        self.label.setText("9")
        '''print("v", v[j])
                        print("l", l)
                        print("st", st)
                        print("k", k)'''

        if k > 0 and vv[k - 1] == v[j]:
            print(k + 1, "桁目認証開始")
            a[k] = 1

        if (st != 0 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st - 1] and turn[k] == 1 and a[k] == 1) or (
                st == 0 and v[j][l - 1] == x[0] and v[j][l - 2] == x[9] and turn[k] == 1 and a[k] == 1):
            print("認証 時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 0 and j == 3:
                print("１桁目認証")
            if k == 2 and j == 8:
                print("３桁目認証")
        if (st != 9 and v[j][l - 1] == x[st] and v[j][l - 2] == x[st + 1] and turn[k] == 2 and a[k] == 1) or (
                st == 9 and v[j][l - 1] == x[9] and v[j][l - 2] == x[0] and turn[k] == 2 and a[k] == 1):
            print("認証 反時計回り")
            s[j] = 0
            s[j + 1] = 2
            if k == 1 and j == 6:
                print("２桁目認証")
            if k == 3 and j == 9:
                self.label.setText("Success")
                print("認証完了")
                # self.QTimer.singleShot(5000, window.close)
                #self.timer()
                #タイマー設定しようとすると途中で終わってしまう

    def timer(self):
        t = 5
        while t > 0:
            time.sleep(5)
            t = 0
        if t == 0:
            exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(style_str)

    window = Movie()
    window.show()
    sys.exit(app.exec_())