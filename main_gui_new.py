# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_guifAGdVQ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pglive.sources.live_plot_widget import LivePlotWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1080, 650)
        MainWindow.setMinimumSize(QSize(1080, 650))
        icon = QIcon()
        icon.addFile(u"resources/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.action_Connect = QAction(MainWindow)
        self.action_Connect.setObjectName(u"action_Connect")
        self.action_Quit = QAction(MainWindow)
        self.action_Quit.setObjectName(u"action_Quit")
        self.action_Resistor = QAction(MainWindow)
        self.action_Resistor.setObjectName(u"action_Resistor")
        self.action_Voltage = QAction(MainWindow)
        self.action_Voltage.setObjectName(u"action_Voltage")
        self.action_Reset_Recorded_Data = QAction(MainWindow)
        self.action_Reset_Recorded_Data.setObjectName(u"action_Reset_Recorded_Data")
        self.action_All = QAction(MainWindow)
        self.action_All.setObjectName(u"action_All")
        self.action_Resistance = QAction(MainWindow)
        self.action_Resistance.setObjectName(u"action_Resistance")
        self.action_Humidity = QAction(MainWindow)
        self.action_Humidity.setObjectName(u"action_Humidity")
        self.action_Temperature = QAction(MainWindow)
        self.action_Temperature.setObjectName(u"action_Temperature")
        self.action_Amplitude = QAction(MainWindow)
        self.action_Amplitude.setObjectName(u"action_Amplitude")
        self.action_Phase = QAction(MainWindow)
        self.action_Phase.setObjectName(u"action_Phase")
        self.actionDissipation = QAction(MainWindow)
        self.actionDissipation.setObjectName(u"actionDissipation")
        self.actionAbsorption = QAction(MainWindow)
        self.actionAbsorption.setObjectName(u"actionAbsorption")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(1000, 600))
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.splitter_4 = QSplitter(self.centralwidget)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter_4)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.htr_layout = QHBoxLayout()
        self.htr_layout.setObjectName(u"htr_layout")
        self.resist_plot = LivePlotWidget(self.layoutWidget)
        self.resist_plot.setObjectName(u"resist_plot")

        self.htr_layout.addWidget(self.resist_plot)

        self.humd_plot = LivePlotWidget(self.layoutWidget)
        self.humd_plot.setObjectName(u"humd_plot")

        self.htr_layout.addWidget(self.humd_plot)

        self.temp_plot = LivePlotWidget(self.layoutWidget)
        self.temp_plot.setObjectName(u"temp_plot")

        self.htr_layout.addWidget(self.temp_plot)


        self.verticalLayout.addLayout(self.htr_layout)

        self.qcm_layout = QGridLayout()
        self.qcm_layout.setObjectName(u"qcm_layout")
        self.amp_plot = LivePlotWidget(self.layoutWidget)
        self.amp_plot.setObjectName(u"amp_plot")

        self.qcm_layout.addWidget(self.amp_plot, 0, 0, 1, 1)

        self.freq_plot = LivePlotWidget(self.layoutWidget)
        self.freq_plot.setObjectName(u"freq_plot")

        self.qcm_layout.addWidget(self.freq_plot, 1, 0, 1, 1)

        self.dissipate_plot = LivePlotWidget(self.layoutWidget)
        self.dissipate_plot.setObjectName(u"dissipate_plot")

        self.qcm_layout.addWidget(self.dissipate_plot, 1, 1, 1, 1)

        self.phase_plot = LivePlotWidget(self.layoutWidget)
        self.phase_plot.setObjectName(u"phase_plot")

        self.qcm_layout.addWidget(self.phase_plot, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.qcm_layout)

        self.splitter_4.addWidget(self.layoutWidget)
        self.splitter_3 = QSplitter(self.splitter_4)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Vertical)
        self.splitter_3.setHandleWidth(2)
        self.splitter_2 = QSplitter(self.splitter_3)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.layoutWidget1 = QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.gridLayout_15 = QGridLayout(self.layoutWidget1)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.label_21 = QLabel(self.layoutWidget1)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.label_21, 0, 0, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.avg_resist_15 = QLineEdit(self.layoutWidget1)
        self.avg_resist_15.setObjectName(u"avg_resist_15")
        self.avg_resist_15.setReadOnly(True)

        self.gridLayout_11.addWidget(self.avg_resist_15, 1, 2, 1, 1)

        self.resist_avg = QLineEdit(self.layoutWidget1)
        self.resist_avg.setObjectName(u"resist_avg")
        self.resist_avg.setReadOnly(True)

        self.gridLayout_11.addWidget(self.resist_avg, 1, 0, 1, 1)

        self.label_10 = QLabel(self.layoutWidget1)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_11.addWidget(self.label_10, 0, 1, 1, 1)

        self.avg_resist_50 = QLineEdit(self.layoutWidget1)
        self.avg_resist_50.setObjectName(u"avg_resist_50")
        self.avg_resist_50.setReadOnly(True)

        self.gridLayout_11.addWidget(self.avg_resist_50, 1, 1, 1, 1)

        self.label_11 = QLabel(self.layoutWidget1)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_11.addWidget(self.label_11, 0, 2, 1, 1)

        self.label_9 = QLabel(self.layoutWidget1)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_11.addWidget(self.label_9, 0, 0, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_11, 1, 0, 1, 1)

        self.splitter_2.addWidget(self.layoutWidget1)
        self.layoutWidget2 = QWidget(self.splitter_2)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.gridLayout_16 = QGridLayout(self.layoutWidget2)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.label_22 = QLabel(self.layoutWidget2)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setAlignment(Qt.AlignCenter)

        self.gridLayout_16.addWidget(self.label_22, 0, 0, 1, 1)

        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.label_15 = QLabel(self.layoutWidget2)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_13.addWidget(self.label_15, 0, 0, 1, 1)

        self.label_16 = QLabel(self.layoutWidget2)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_13.addWidget(self.label_16, 0, 1, 1, 1)

        self.label_17 = QLabel(self.layoutWidget2)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_13.addWidget(self.label_17, 0, 2, 1, 1)

        self.humd_avg = QLineEdit(self.layoutWidget2)
        self.humd_avg.setObjectName(u"humd_avg")
        self.humd_avg.setReadOnly(True)

        self.gridLayout_13.addWidget(self.humd_avg, 1, 0, 1, 1)

        self.humd_avg_50 = QLineEdit(self.layoutWidget2)
        self.humd_avg_50.setObjectName(u"humd_avg_50")
        self.humd_avg_50.setReadOnly(True)

        self.gridLayout_13.addWidget(self.humd_avg_50, 1, 1, 1, 1)

        self.humd_avg_15 = QLineEdit(self.layoutWidget2)
        self.humd_avg_15.setObjectName(u"humd_avg_15")
        self.humd_avg_15.setReadOnly(True)

        self.gridLayout_13.addWidget(self.humd_avg_15, 1, 2, 1, 1)


        self.gridLayout_16.addLayout(self.gridLayout_13, 1, 0, 1, 1)

        self.splitter_2.addWidget(self.layoutWidget2)
        self.layoutWidget3 = QWidget(self.splitter_2)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.gridLayout_17 = QGridLayout(self.layoutWidget3)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.label_23 = QLabel(self.layoutWidget3)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.label_23, 0, 0, 1, 1)

        self.gridLayout_14 = QGridLayout()
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_18 = QLabel(self.layoutWidget3)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_14.addWidget(self.label_18, 0, 0, 1, 1)

        self.label_20 = QLabel(self.layoutWidget3)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_14.addWidget(self.label_20, 0, 2, 1, 1)

        self.temp_avg = QLineEdit(self.layoutWidget3)
        self.temp_avg.setObjectName(u"temp_avg")
        self.temp_avg.setReadOnly(True)

        self.gridLayout_14.addWidget(self.temp_avg, 1, 0, 1, 1)

        self.temp_avg_50 = QLineEdit(self.layoutWidget3)
        self.temp_avg_50.setObjectName(u"temp_avg_50")
        self.temp_avg_50.setReadOnly(True)

        self.gridLayout_14.addWidget(self.temp_avg_50, 1, 1, 1, 1)

        self.temp_avg_15 = QLineEdit(self.layoutWidget3)
        self.temp_avg_15.setObjectName(u"temp_avg_15")
        self.temp_avg_15.setReadOnly(True)

        self.gridLayout_14.addWidget(self.temp_avg_15, 1, 2, 1, 1)

        self.label_19 = QLabel(self.layoutWidget3)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_14.addWidget(self.label_19, 0, 1, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_14, 1, 0, 1, 1)

        self.splitter_2.addWidget(self.layoutWidget3)
        self.splitter_3.addWidget(self.splitter_2)
        self.splitter = QSplitter(self.splitter_3)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget4 = QWidget(self.splitter)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.gridLayout_20 = QGridLayout(self.layoutWidget4)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.label_34 = QLabel(self.layoutWidget4)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setAlignment(Qt.AlignCenter)

        self.gridLayout_20.addWidget(self.label_34, 0, 0, 1, 1)

        self.gridLayout_18 = QGridLayout()
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.label_24 = QLabel(self.layoutWidget4)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_18.addWidget(self.label_24, 0, 0, 1, 1)

        self.freq_f1 = QLineEdit(self.layoutWidget4)
        self.freq_f1.setObjectName(u"freq_f1")
        self.freq_f1.setReadOnly(True)

        self.gridLayout_18.addWidget(self.freq_f1, 0, 1, 1, 1)

        self.label_25 = QLabel(self.layoutWidget4)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_18.addWidget(self.label_25, 1, 0, 1, 1)

        self.freq_f3 = QLineEdit(self.layoutWidget4)
        self.freq_f3.setObjectName(u"freq_f3")
        self.freq_f3.setReadOnly(True)

        self.gridLayout_18.addWidget(self.freq_f3, 1, 1, 1, 1)

        self.label_26 = QLabel(self.layoutWidget4)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_18.addWidget(self.label_26, 2, 0, 1, 1)

        self.freq_f5 = QLineEdit(self.layoutWidget4)
        self.freq_f5.setObjectName(u"freq_f5")
        self.freq_f5.setReadOnly(True)

        self.gridLayout_18.addWidget(self.freq_f5, 2, 1, 1, 1)

        self.label_27 = QLabel(self.layoutWidget4)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_18.addWidget(self.label_27, 3, 0, 1, 1)

        self.freq_f7 = QLineEdit(self.layoutWidget4)
        self.freq_f7.setObjectName(u"freq_f7")
        self.freq_f7.setReadOnly(True)

        self.gridLayout_18.addWidget(self.freq_f7, 3, 1, 1, 1)

        self.label_28 = QLabel(self.layoutWidget4)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_18.addWidget(self.label_28, 4, 0, 1, 1)

        self.freq_f9 = QLineEdit(self.layoutWidget4)
        self.freq_f9.setObjectName(u"freq_f9")
        self.freq_f9.setReadOnly(True)

        self.gridLayout_18.addWidget(self.freq_f9, 4, 1, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_18, 1, 0, 1, 1)

        self.splitter.addWidget(self.layoutWidget4)
        self.layoutWidget5 = QWidget(self.splitter)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.gridLayout_21 = QGridLayout(self.layoutWidget5)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_19 = QGridLayout()
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.diss_d3 = QLineEdit(self.layoutWidget5)
        self.diss_d3.setObjectName(u"diss_d3")
        self.diss_d3.setReadOnly(True)

        self.gridLayout_19.addWidget(self.diss_d3, 1, 1, 1, 1)

        self.diss_d7 = QLineEdit(self.layoutWidget5)
        self.diss_d7.setObjectName(u"diss_d7")
        self.diss_d7.setReadOnly(True)

        self.gridLayout_19.addWidget(self.diss_d7, 3, 1, 1, 1)

        self.label_33 = QLabel(self.layoutWidget5)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_19.addWidget(self.label_33, 4, 0, 1, 1)

        self.label_32 = QLabel(self.layoutWidget5)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_19.addWidget(self.label_32, 3, 0, 1, 1)

        self.diss_d1 = QLineEdit(self.layoutWidget5)
        self.diss_d1.setObjectName(u"diss_d1")
        self.diss_d1.setReadOnly(True)

        self.gridLayout_19.addWidget(self.diss_d1, 0, 1, 1, 1)

        self.label_30 = QLabel(self.layoutWidget5)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_19.addWidget(self.label_30, 1, 0, 1, 1)

        self.label_31 = QLabel(self.layoutWidget5)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_19.addWidget(self.label_31, 2, 0, 1, 1)

        self.label_29 = QLabel(self.layoutWidget5)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_19.addWidget(self.label_29, 0, 0, 1, 1)

        self.diss_d5 = QLineEdit(self.layoutWidget5)
        self.diss_d5.setObjectName(u"diss_d5")
        self.diss_d5.setReadOnly(True)

        self.gridLayout_19.addWidget(self.diss_d5, 2, 1, 1, 1)

        self.diss_d9 = QLineEdit(self.layoutWidget5)
        self.diss_d9.setObjectName(u"diss_d9")
        self.diss_d9.setReadOnly(True)

        self.gridLayout_19.addWidget(self.diss_d9, 4, 1, 1, 1)


        self.gridLayout_21.addLayout(self.gridLayout_19, 1, 0, 1, 1)

        self.label_35 = QLabel(self.layoutWidget5)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setAlignment(Qt.AlignCenter)

        self.gridLayout_21.addWidget(self.label_35, 0, 0, 1, 1)

        self.splitter.addWidget(self.layoutWidget5)
        self.splitter_3.addWidget(self.splitter)
        self.frame_5 = QFrame(self.splitter_3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 5, 2, 2)
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.label_13 = QLabel(self.frame_5)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_12.addWidget(self.label_13, 0, 0, 1, 1)

        self.htr_serial = QComboBox(self.frame_5)
        self.htr_serial.setObjectName(u"htr_serial")

        self.gridLayout_12.addWidget(self.htr_serial, 0, 1, 1, 1)

        self.label_14 = QLabel(self.frame_5)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_12.addWidget(self.label_14, 0, 2, 1, 1)

        self.qcm_serial = QComboBox(self.frame_5)
        self.qcm_serial.setObjectName(u"qcm_serial")

        self.gridLayout_12.addWidget(self.qcm_serial, 0, 3, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout_12)

        self.splitter_3.addWidget(self.frame_5)
        self.layoutWidget6 = QWidget(self.splitter_3)
        self.layoutWidget6.setObjectName(u"layoutWidget6")
        self.gridLayout_10 = QGridLayout(self.layoutWidget6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame = QFrame(self.layoutWidget6)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.frame.setLineWidth(16)
        self.frame.setMidLineWidth(6)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.qc_type = QComboBox(self.frame)
        self.qc_type.addItem("")
        self.qc_type.addItem("")
        self.qc_type.setObjectName(u"qc_type")

        self.gridLayout_2.addWidget(self.qc_type, 1, 0, 1, 1)

        self.calibrate_btn = QPushButton(self.frame)
        self.calibrate_btn.setObjectName(u"calibrate_btn")

        self.gridLayout_2.addWidget(self.calibrate_btn, 1, 1, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)


        self.gridLayout_3.addWidget(self.frame, 2, 0, 1, 1)

        self.label_4 = QLabel(self.layoutWidget6)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_3, 0, 0, 2, 2)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.label_8 = QLabel(self.layoutWidget6)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_9.addWidget(self.label_8, 0, 0, 1, 1)

        self.frame_4 = QFrame(self.layoutWidget6)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Sunken)
        self.frame_4.setLineWidth(16)
        self.frame_4.setMidLineWidth(6)
        self.verticalLayout_5 = QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.reset_btn = QPushButton(self.frame_4)
        self.reset_btn.setObjectName(u"reset_btn")
        self.reset_btn.setEnabled(False)

        self.gridLayout_8.addWidget(self.reset_btn, 0, 2, 1, 1)

        self.progress_bar = QProgressBar(self.frame_4)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(24)
        self.progress_bar.setOrientation(Qt.Horizontal)
        self.progress_bar.setInvertedAppearance(False)

        self.gridLayout_8.addWidget(self.progress_bar, 2, 0, 1, 3)

        self.start_btn = QPushButton(self.frame_4)
        self.start_btn.setObjectName(u"start_btn")
        icon1 = QIcon()
        icon1.addFile(u"resources/start.png", QSize(), QIcon.Normal, QIcon.Off)
        self.start_btn.setIcon(icon1)
        self.start_btn.setIconSize(QSize(10, 10))

        self.gridLayout_8.addWidget(self.start_btn, 0, 0, 1, 1)

        self.stop_btn = QPushButton(self.frame_4)
        self.stop_btn.setObjectName(u"stop_btn")
        self.stop_btn.setEnabled(False)
        icon2 = QIcon()
        icon2.addFile(u"resources/stop.png", QSize(), QIcon.Normal, QIcon.Off)
        self.stop_btn.setIcon(icon2)
        self.stop_btn.setIconSize(QSize(10, 10))

        self.gridLayout_8.addWidget(self.stop_btn, 0, 1, 1, 1)

        self.perm_status = QLineEdit(self.frame_4)
        self.perm_status.setObjectName(u"perm_status")
        self.perm_status.setReadOnly(True)

        self.gridLayout_8.addWidget(self.perm_status, 1, 0, 1, 3)


        self.verticalLayout_5.addLayout(self.gridLayout_8)


        self.gridLayout_9.addWidget(self.frame_4, 1, 0, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_9, 2, 1, 2, 2)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_5 = QLabel(self.layoutWidget6)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_5.addWidget(self.label_5, 1, 0, 1, 1)

        self.frame_2 = QFrame(self.layoutWidget6)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Sunken)
        self.frame_2.setLineWidth(16)
        self.frame_2.setMidLineWidth(6)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 1, 1, 1)

        self.measure_type = QComboBox(self.frame_2)
        self.measure_type.addItem("")
        self.measure_type.addItem("")
        self.measure_type.setObjectName(u"measure_type")

        self.gridLayout_4.addWidget(self.measure_type, 1, 0, 1, 1)

        self.freq_list = QComboBox(self.frame_2)
        self.freq_list.setObjectName(u"freq_list")
        self.freq_list.setEnabled(False)

        self.gridLayout_4.addWidget(self.freq_list, 1, 1, 1, 1)

        self.qcm_temp_ctrl = QCheckBox(self.frame_2)
        self.qcm_temp_ctrl.setObjectName(u"qcm_temp_ctrl")
        self.qcm_temp_ctrl.setEnabled(False)

        self.gridLayout_4.addWidget(self.qcm_temp_ctrl, 2, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_4)


        self.gridLayout_5.addWidget(self.frame_2, 2, 0, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_5, 0, 2, 2, 1)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_7 = QLabel(self.layoutWidget6)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_7.addWidget(self.label_7, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.layoutWidget6)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Sunken)
        self.frame_3.setLineWidth(16)
        self.frame_3.setMidLineWidth(6)
        self.verticalLayout_4 = QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.file_dest = QLineEdit(self.frame_3)
        self.file_dest.setObjectName(u"file_dest")
        self.file_dest.setEnabled(False)

        self.gridLayout_6.addWidget(self.file_dest, 3, 0, 1, 1)

        self.file_select = QToolButton(self.frame_3)
        self.file_select.setObjectName(u"file_select")
        self.file_select.setEnabled(False)
        icon3 = QIcon()
        icon3.addFile(u"resources/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.file_select.setIcon(icon3)

        self.gridLayout_6.addWidget(self.file_select, 3, 1, 1, 1)

        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_6.addWidget(self.label_6, 1, 0, 1, 1)

        self.auto_export = QCheckBox(self.frame_3)
        self.auto_export.setObjectName(u"auto_export")

        self.gridLayout_6.addWidget(self.auto_export, 0, 0, 1, 2)


        self.verticalLayout_4.addLayout(self.gridLayout_6)


        self.gridLayout_7.addWidget(self.frame_3, 1, 0, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_7, 2, 0, 2, 1)

        self.splitter_3.addWidget(self.layoutWidget6)
        self.splitter_4.addWidget(self.splitter_3)

        self.verticalLayout_6.addWidget(self.splitter_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1080, 22))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        self.menu_Export = QMenu(self.menu_File)
        self.menu_Export.setObjectName(u"menu_Export")
        self.menu_Edit = QMenu(self.menubar)
        self.menu_Edit.setObjectName(u"menu_Edit")
        self.menu_Update = QMenu(self.menu_Edit)
        self.menu_Update.setObjectName(u"menu_Update")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.label_10.setBuddy(self.avg_resist_50)
        self.label_11.setBuddy(self.avg_resist_15)
        self.label_9.setBuddy(self.resist_avg)
        self.label_15.setBuddy(self.humd_avg)
        self.label_16.setBuddy(self.humd_avg_50)
        self.label_17.setBuddy(self.humd_avg_15)
        self.label_18.setBuddy(self.temp_avg)
        self.label_20.setBuddy(self.temp_avg_15)
        self.label_19.setBuddy(self.temp_avg_50)
        self.label_24.setBuddy(self.freq_f1)
        self.label_25.setBuddy(self.freq_f3)
        self.label_26.setBuddy(self.freq_f5)
        self.label_27.setBuddy(self.freq_f7)
        self.label_28.setBuddy(self.freq_f9)
        self.label_33.setBuddy(self.diss_d9)
        self.label_32.setBuddy(self.diss_d7)
        self.label_30.setBuddy(self.diss_d3)
        self.label_31.setBuddy(self.diss_d5)
        self.label_29.setBuddy(self.diss_d1)
        self.label_13.setBuddy(self.htr_serial)
        self.label_14.setBuddy(self.qcm_serial)
        self.label.setBuddy(self.qc_type)
        self.label_2.setBuddy(self.measure_type)
        self.label_3.setBuddy(self.freq_list)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.htr_serial, self.qcm_serial)
        QWidget.setTabOrder(self.qcm_serial, self.qc_type)
        QWidget.setTabOrder(self.qc_type, self.calibrate_btn)
        QWidget.setTabOrder(self.calibrate_btn, self.measure_type)
        QWidget.setTabOrder(self.measure_type, self.freq_list)
        QWidget.setTabOrder(self.freq_list, self.qcm_temp_ctrl)
        QWidget.setTabOrder(self.qcm_temp_ctrl, self.auto_export)
        QWidget.setTabOrder(self.auto_export, self.file_dest)
        QWidget.setTabOrder(self.file_dest, self.start_btn)
        QWidget.setTabOrder(self.start_btn, self.stop_btn)
        QWidget.setTabOrder(self.stop_btn, self.reset_btn)
        QWidget.setTabOrder(self.reset_btn, self.file_select)
        QWidget.setTabOrder(self.file_select, self.resist_avg)
        QWidget.setTabOrder(self.resist_avg, self.avg_resist_50)
        QWidget.setTabOrder(self.avg_resist_50, self.avg_resist_15)
        QWidget.setTabOrder(self.avg_resist_15, self.humd_avg)
        QWidget.setTabOrder(self.humd_avg, self.humd_avg_50)
        QWidget.setTabOrder(self.humd_avg_50, self.humd_avg_15)
        QWidget.setTabOrder(self.humd_avg_15, self.temp_avg)
        QWidget.setTabOrder(self.temp_avg, self.freq_f9)
        QWidget.setTabOrder(self.freq_f9, self.freq_f7)
        QWidget.setTabOrder(self.freq_f7, self.temp_avg_50)
        QWidget.setTabOrder(self.temp_avg_50, self.temp_avg_15)
        QWidget.setTabOrder(self.temp_avg_15, self.freq_f1)
        QWidget.setTabOrder(self.freq_f1, self.freq_f3)
        QWidget.setTabOrder(self.freq_f3, self.freq_f5)
        QWidget.setTabOrder(self.freq_f5, self.diss_d9)
        QWidget.setTabOrder(self.diss_d9, self.diss_d5)
        QWidget.setTabOrder(self.diss_d5, self.diss_d7)
        QWidget.setTabOrder(self.diss_d7, self.perm_status)
        QWidget.setTabOrder(self.perm_status, self.diss_d3)
        QWidget.setTabOrder(self.diss_d3, self.diss_d1)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menu_File.addAction(self.action_Connect)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.menu_Export.menuAction())
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Export.addAction(self.action_All)
        self.menu_Export.addSeparator()
        self.menu_Export.addAction(self.action_Resistance)
        self.menu_Export.addAction(self.action_Humidity)
        self.menu_Export.addAction(self.action_Temperature)
        self.menu_Export.addAction(self.action_Amplitude)
        self.menu_Export.addAction(self.action_Phase)
        self.menu_Export.addAction(self.actionDissipation)
        self.menu_Export.addAction(self.actionAbsorption)
        self.menu_Edit.addAction(self.menu_Update.menuAction())
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Reset_Recorded_Data)
        self.menu_Update.addAction(self.action_Resistor)
        self.menu_Update.addAction(self.action_Voltage)

        self.retranslateUi(MainWindow)
        self.auto_export.toggled.connect(self.file_dest.setEnabled)
        self.auto_export.toggled.connect(self.file_select.setEnabled)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sensor Fusion", None))
        self.action_Connect.setText(QCoreApplication.translate("MainWindow", u"&Connect", None))
        self.action_Quit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
#if QT_CONFIG(tooltip)
        self.action_Quit.setToolTip(QCoreApplication.translate("MainWindow", u"Quit the program", None))
#endif // QT_CONFIG(tooltip)
        self.action_Resistor.setText(QCoreApplication.translate("MainWindow", u"&Resistor", None))
#if QT_CONFIG(tooltip)
        self.action_Resistor.setToolTip(QCoreApplication.translate("MainWindow", u"Update the reference resistor", None))
#endif // QT_CONFIG(tooltip)
        self.action_Voltage.setText(QCoreApplication.translate("MainWindow", u"&Voltage", None))
#if QT_CONFIG(tooltip)
        self.action_Voltage.setToolTip(QCoreApplication.translate("MainWindow", u"Update the reference voltage", None))
#endif // QT_CONFIG(tooltip)
        self.action_Reset_Recorded_Data.setText(QCoreApplication.translate("MainWindow", u"&Reset Recorded Data", None))
#if QT_CONFIG(tooltip)
        self.action_Reset_Recorded_Data.setToolTip(QCoreApplication.translate("MainWindow", u"Reset the recorded data up to this point", None))
#endif // QT_CONFIG(tooltip)
        self.action_All.setText(QCoreApplication.translate("MainWindow", u"&All", None))
#if QT_CONFIG(tooltip)
        self.action_All.setToolTip(QCoreApplication.translate("MainWindow", u"Exports all data", None))
#endif // QT_CONFIG(tooltip)
        self.action_Resistance.setText(QCoreApplication.translate("MainWindow", u"&Resistance", None))
#if QT_CONFIG(tooltip)
        self.action_Resistance.setToolTip(QCoreApplication.translate("MainWindow", u"Exports resistance data only", None))
#endif // QT_CONFIG(tooltip)
        self.action_Humidity.setText(QCoreApplication.translate("MainWindow", u"&Humidity", None))
#if QT_CONFIG(tooltip)
        self.action_Humidity.setToolTip(QCoreApplication.translate("MainWindow", u"Exports humidity data only", None))
#endif // QT_CONFIG(tooltip)
        self.action_Temperature.setText(QCoreApplication.translate("MainWindow", u"&Temperature", None))
#if QT_CONFIG(tooltip)
        self.action_Temperature.setToolTip(QCoreApplication.translate("MainWindow", u"Exports temperature data only", None))
#endif // QT_CONFIG(tooltip)
        self.action_Amplitude.setText(QCoreApplication.translate("MainWindow", u"&Amplitude", None))
        self.action_Phase.setText(QCoreApplication.translate("MainWindow", u"&Phase", None))
        self.actionDissipation.setText(QCoreApplication.translate("MainWindow", u"Dissipation", None))
        self.actionAbsorption.setText(QCoreApplication.translate("MainWindow", u"Resonance &Frequency", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Resistance (Ohm)</span></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Average (<50)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Average (<15)", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Average", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Humidity (%RH)</span></p></body></html>", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Average", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Average (<50)", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Average (<15)", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Temperature (degC)</span></p></body></html>", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Average", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Average (<15)", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Average (<50)", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Frequency (Hz)</span></p></body></html>", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"F1", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"F3", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"F5", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"F7", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"F9", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"D9", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"D7", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"D3", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"D5", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"D1", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Dissipation (ppm)</span></p></body></html>", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"HTR Serial Sensor", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"QCM Serial Sensor", None))
        self.qc_type.setItemText(0, QCoreApplication.translate("MainWindow", u"5 MHz", None))
        self.qc_type.setItemText(1, QCoreApplication.translate("MainWindow", u"10 MHz", None))

        self.calibrate_btn.setText(QCoreApplication.translate("MainWindow", u"Calibrate", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Quartz Crystal Type", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt;\">Step 1. Calibration</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt;\">Step 4. Start</span></p></body></html>", None))
        self.reset_btn.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop_btn.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt;\">Step 2. Setup Measurement</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Measurement Type", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Frequency", None))
        self.measure_type.setItemText(0, QCoreApplication.translate("MainWindow", u"Single Measurement", None))
        self.measure_type.setItemText(1, QCoreApplication.translate("MainWindow", u"Multiple Measurements", None))

        self.qcm_temp_ctrl.setText(QCoreApplication.translate("MainWindow", u"Temperature Control", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt;\">Step 3. Exportation</span></p></body></html>", None))
        self.file_select.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"File Destination", None))
        self.auto_export.setText(QCoreApplication.translate("MainWindow", u"Auto Export Data on Stop", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_Export.setTitle(QCoreApplication.translate("MainWindow", u"&Export", None))
        self.menu_Edit.setTitle(QCoreApplication.translate("MainWindow", u"&Edit", None))
        self.menu_Update.setTitle(QCoreApplication.translate("MainWindow", u"&Update References", None))
    # retranslateUi

