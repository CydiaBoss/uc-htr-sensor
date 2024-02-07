# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\andre\Documents\Python\sensor-fusion\uc-htr-sensor\ui\main_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets

from pglive.sources.live_plot_widget import LivePlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 650)
        MainWindow.setMinimumSize(QtCore.QSize(1080, 650))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\resources\\logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1000, 600))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.splitter_4 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")
        self.layoutWidget = QtWidgets.QWidget(self.splitter_4)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.htr_layout = QtWidgets.QHBoxLayout()
        self.htr_layout.setObjectName("htr_layout")
        self.resist_plot = LivePlotWidget(self.layoutWidget)
        self.resist_plot.setObjectName("resist_plot")
        self.htr_layout.addWidget(self.resist_plot)
        self.humd_plot = LivePlotWidget(self.layoutWidget)
        self.humd_plot.setObjectName("humd_plot")
        self.htr_layout.addWidget(self.humd_plot)
        self.temp_plot = LivePlotWidget(self.layoutWidget)
        self.temp_plot.setObjectName("temp_plot")
        self.htr_layout.addWidget(self.temp_plot)
        self.verticalLayout.addLayout(self.htr_layout)
        self.qcm_layout = QtWidgets.QGridLayout()
        self.qcm_layout.setObjectName("qcm_layout")
        self.amp_plot = LivePlotWidget(self.layoutWidget)
        self.amp_plot.setObjectName("amp_plot")
        self.qcm_layout.addWidget(self.amp_plot, 0, 0, 1, 1)
        self.freq_plot = LivePlotWidget(self.layoutWidget)
        self.freq_plot.setObjectName("freq_plot")
        self.qcm_layout.addWidget(self.freq_plot, 1, 0, 1, 1)
        self.dissipate_plot = LivePlotWidget(self.layoutWidget)
        self.dissipate_plot.setObjectName("dissipate_plot")
        self.qcm_layout.addWidget(self.dissipate_plot, 1, 1, 1, 1)
        self.phase_plot = LivePlotWidget(self.layoutWidget)
        self.phase_plot.setObjectName("phase_plot")
        self.qcm_layout.addWidget(self.phase_plot, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.qcm_layout)
        self.splitter_3 = QtWidgets.QSplitter(self.splitter_4)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setHandleWidth(2)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_3)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.label_21 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.gridLayout_15.addWidget(self.label_21, 0, 0, 1, 1)
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.avg_resist_15 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.avg_resist_15.setReadOnly(True)
        self.avg_resist_15.setObjectName("avg_resist_15")
        self.gridLayout_11.addWidget(self.avg_resist_15, 1, 2, 1, 1)
        self.resist_avg = QtWidgets.QLineEdit(self.layoutWidget1)
        self.resist_avg.setReadOnly(True)
        self.resist_avg.setObjectName("resist_avg")
        self.gridLayout_11.addWidget(self.resist_avg, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_10.setObjectName("label_10")
        self.gridLayout_11.addWidget(self.label_10, 0, 1, 1, 1)
        self.avg_resist_50 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.avg_resist_50.setReadOnly(True)
        self.avg_resist_50.setObjectName("avg_resist_50")
        self.gridLayout_11.addWidget(self.avg_resist_50, 1, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_11.setObjectName("label_11")
        self.gridLayout_11.addWidget(self.label_11, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_9.setObjectName("label_9")
        self.gridLayout_11.addWidget(self.label_9, 0, 0, 1, 1)
        self.gridLayout_15.addLayout(self.gridLayout_11, 1, 0, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.label_22 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.gridLayout_16.addWidget(self.label_22, 0, 0, 1, 1)
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_15 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_15.setObjectName("label_15")
        self.gridLayout_13.addWidget(self.label_15, 0, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_16.setObjectName("label_16")
        self.gridLayout_13.addWidget(self.label_16, 0, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_17.setObjectName("label_17")
        self.gridLayout_13.addWidget(self.label_17, 0, 2, 1, 1)
        self.humd_avg = QtWidgets.QLineEdit(self.layoutWidget2)
        self.humd_avg.setReadOnly(True)
        self.humd_avg.setObjectName("humd_avg")
        self.gridLayout_13.addWidget(self.humd_avg, 1, 0, 1, 1)
        self.humd_avg_50 = QtWidgets.QLineEdit(self.layoutWidget2)
        self.humd_avg_50.setReadOnly(True)
        self.humd_avg_50.setObjectName("humd_avg_50")
        self.gridLayout_13.addWidget(self.humd_avg_50, 1, 1, 1, 1)
        self.humd_avg_15 = QtWidgets.QLineEdit(self.layoutWidget2)
        self.humd_avg_15.setReadOnly(True)
        self.humd_avg_15.setObjectName("humd_avg_15")
        self.gridLayout_13.addWidget(self.humd_avg_15, 1, 2, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_13, 1, 0, 1, 1)
        self.layoutWidget3 = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.label_23 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.gridLayout_17.addWidget(self.label_23, 0, 0, 1, 1)
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.label_18 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_18.setObjectName("label_18")
        self.gridLayout_14.addWidget(self.label_18, 0, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_20.setObjectName("label_20")
        self.gridLayout_14.addWidget(self.label_20, 0, 2, 1, 1)
        self.temp_avg = QtWidgets.QLineEdit(self.layoutWidget3)
        self.temp_avg.setReadOnly(True)
        self.temp_avg.setObjectName("temp_avg")
        self.gridLayout_14.addWidget(self.temp_avg, 1, 0, 1, 1)
        self.temp_avg_50 = QtWidgets.QLineEdit(self.layoutWidget3)
        self.temp_avg_50.setReadOnly(True)
        self.temp_avg_50.setObjectName("temp_avg_50")
        self.gridLayout_14.addWidget(self.temp_avg_50, 1, 1, 1, 1)
        self.temp_avg_15 = QtWidgets.QLineEdit(self.layoutWidget3)
        self.temp_avg_15.setReadOnly(True)
        self.temp_avg_15.setObjectName("temp_avg_15")
        self.gridLayout_14.addWidget(self.temp_avg_15, 1, 2, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_19.setObjectName("label_19")
        self.gridLayout_14.addWidget(self.label_19, 0, 1, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_14, 1, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.splitter_3)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget4 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.layoutWidget4)
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.label_34 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_34.setAlignment(QtCore.Qt.AlignCenter)
        self.label_34.setObjectName("label_34")
        self.gridLayout_20.addWidget(self.label_34, 0, 0, 1, 1)
        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.label_24 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_24.setObjectName("label_24")
        self.gridLayout_18.addWidget(self.label_24, 0, 0, 1, 1)
        self.freq_f1 = QtWidgets.QLineEdit(self.layoutWidget4)
        self.freq_f1.setReadOnly(True)
        self.freq_f1.setObjectName("freq_f1")
        self.gridLayout_18.addWidget(self.freq_f1, 0, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_25.setObjectName("label_25")
        self.gridLayout_18.addWidget(self.label_25, 1, 0, 1, 1)
        self.freq_f3 = QtWidgets.QLineEdit(self.layoutWidget4)
        self.freq_f3.setReadOnly(True)
        self.freq_f3.setObjectName("freq_f3")
        self.gridLayout_18.addWidget(self.freq_f3, 1, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_26.setObjectName("label_26")
        self.gridLayout_18.addWidget(self.label_26, 2, 0, 1, 1)
        self.freq_f5 = QtWidgets.QLineEdit(self.layoutWidget4)
        self.freq_f5.setReadOnly(True)
        self.freq_f5.setObjectName("freq_f5")
        self.gridLayout_18.addWidget(self.freq_f5, 2, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_27.setObjectName("label_27")
        self.gridLayout_18.addWidget(self.label_27, 3, 0, 1, 1)
        self.freq_f7 = QtWidgets.QLineEdit(self.layoutWidget4)
        self.freq_f7.setReadOnly(True)
        self.freq_f7.setObjectName("freq_f7")
        self.gridLayout_18.addWidget(self.freq_f7, 3, 1, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_28.setObjectName("label_28")
        self.gridLayout_18.addWidget(self.label_28, 4, 0, 1, 1)
        self.freq_f9 = QtWidgets.QLineEdit(self.layoutWidget4)
        self.freq_f9.setReadOnly(True)
        self.freq_f9.setObjectName("freq_f9")
        self.gridLayout_18.addWidget(self.freq_f9, 4, 1, 1, 1)
        self.gridLayout_20.addLayout(self.gridLayout_18, 1, 0, 1, 1)
        self.layoutWidget5 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.gridLayout_21 = QtWidgets.QGridLayout(self.layoutWidget5)
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.diss_d3 = QtWidgets.QLineEdit(self.layoutWidget5)
        self.diss_d3.setReadOnly(True)
        self.diss_d3.setObjectName("diss_d3")
        self.gridLayout_19.addWidget(self.diss_d3, 1, 1, 1, 1)
        self.diss_d7 = QtWidgets.QLineEdit(self.layoutWidget5)
        self.diss_d7.setReadOnly(True)
        self.diss_d7.setObjectName("diss_d7")
        self.gridLayout_19.addWidget(self.diss_d7, 3, 1, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_33.setObjectName("label_33")
        self.gridLayout_19.addWidget(self.label_33, 4, 0, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_32.setObjectName("label_32")
        self.gridLayout_19.addWidget(self.label_32, 3, 0, 1, 1)
        self.diss_d1 = QtWidgets.QLineEdit(self.layoutWidget5)
        self.diss_d1.setReadOnly(True)
        self.diss_d1.setObjectName("diss_d1")
        self.gridLayout_19.addWidget(self.diss_d1, 0, 1, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_30.setObjectName("label_30")
        self.gridLayout_19.addWidget(self.label_30, 1, 0, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_31.setObjectName("label_31")
        self.gridLayout_19.addWidget(self.label_31, 2, 0, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_29.setObjectName("label_29")
        self.gridLayout_19.addWidget(self.label_29, 0, 0, 1, 1)
        self.diss_d5 = QtWidgets.QLineEdit(self.layoutWidget5)
        self.diss_d5.setReadOnly(True)
        self.diss_d5.setObjectName("diss_d5")
        self.gridLayout_19.addWidget(self.diss_d5, 2, 1, 1, 1)
        self.diss_d9 = QtWidgets.QLineEdit(self.layoutWidget5)
        self.diss_d9.setReadOnly(True)
        self.diss_d9.setObjectName("diss_d9")
        self.gridLayout_19.addWidget(self.diss_d9, 4, 1, 1, 1)
        self.gridLayout_21.addLayout(self.gridLayout_19, 1, 0, 1, 1)
        self.label_35 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_35.setAlignment(QtCore.Qt.AlignCenter)
        self.label_35.setObjectName("label_35")
        self.gridLayout_21.addWidget(self.label_35, 0, 0, 1, 1)
        self.frame_5 = QtWidgets.QFrame(self.splitter_3)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setContentsMargins(5, 5, 2, 2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_13 = QtWidgets.QLabel(self.frame_5)
        self.label_13.setObjectName("label_13")
        self.gridLayout_12.addWidget(self.label_13, 0, 0, 1, 1)
        self.htr_serial = QtWidgets.QComboBox(self.frame_5)
        self.htr_serial.setObjectName("htr_serial")
        self.gridLayout_12.addWidget(self.htr_serial, 0, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame_5)
        self.label_14.setObjectName("label_14")
        self.gridLayout_12.addWidget(self.label_14, 0, 2, 1, 1)
        self.qcm_serial = QtWidgets.QComboBox(self.frame_5)
        self.qcm_serial.setObjectName("qcm_serial")
        self.gridLayout_12.addWidget(self.qcm_serial, 0, 3, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_12)
        self.layoutWidget6 = QtWidgets.QWidget(self.splitter_3)
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.layoutWidget6)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame = QtWidgets.QFrame(self.layoutWidget6)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(16)
        self.frame.setMidLineWidth(6)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.qc_type = QtWidgets.QComboBox(self.frame)
        self.qc_type.setObjectName("qc_type")
        self.qc_type.addItem("")
        self.qc_type.addItem("")
        self.gridLayout_2.addWidget(self.qc_type, 1, 0, 1, 1)
        self.calibrate_btn = QtWidgets.QPushButton(self.frame)
        self.calibrate_btn.setObjectName("calibrate_btn")
        self.gridLayout_2.addWidget(self.calibrate_btn, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.gridLayout_3.addWidget(self.frame, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget6)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_3, 0, 0, 2, 2)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget6)
        self.label_8.setObjectName("label_8")
        self.gridLayout_9.addWidget(self.label_8, 0, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.layoutWidget6)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_4.setLineWidth(16)
        self.frame_4.setMidLineWidth(6)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.reset_btn = QtWidgets.QPushButton(self.frame_4)
        self.reset_btn.setEnabled(False)
        self.reset_btn.setObjectName("reset_btn")
        self.gridLayout_8.addWidget(self.reset_btn, 0, 2, 1, 1)
        self.progress_bar = QtWidgets.QProgressBar(self.frame_4)
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setOrientation(QtCore.Qt.Horizontal)
        self.progress_bar.setInvertedAppearance(False)
        self.progress_bar.setObjectName("progress_bar")
        self.gridLayout_8.addWidget(self.progress_bar, 2, 0, 1, 3)
        self.start_btn = QtWidgets.QPushButton(self.frame_4)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ui\\resources\\start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_btn.setIcon(icon1)
        self.start_btn.setIconSize(QtCore.QSize(10, 10))
        self.start_btn.setObjectName("start_btn")
        self.gridLayout_8.addWidget(self.start_btn, 0, 0, 1, 1)
        self.stop_btn = QtWidgets.QPushButton(self.frame_4)
        self.stop_btn.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ui\\resources\\stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_btn.setIcon(icon2)
        self.stop_btn.setIconSize(QtCore.QSize(10, 10))
        self.stop_btn.setObjectName("stop_btn")
        self.gridLayout_8.addWidget(self.stop_btn, 0, 1, 1, 1)
        self.perm_status = QtWidgets.QLineEdit(self.frame_4)
        self.perm_status.setReadOnly(True)
        self.perm_status.setObjectName("perm_status")
        self.gridLayout_8.addWidget(self.perm_status, 1, 0, 1, 3)
        self.verticalLayout_5.addLayout(self.gridLayout_8)
        self.gridLayout_9.addWidget(self.frame_4, 1, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_9, 2, 1, 2, 2)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget6)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 1, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.layoutWidget6)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setLineWidth(16)
        self.frame_2.setMidLineWidth(6)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 0, 1, 1, 1)
        self.measure_type = QtWidgets.QComboBox(self.frame_2)
        self.measure_type.setObjectName("measure_type")
        self.measure_type.addItem("")
        self.measure_type.addItem("")
        self.gridLayout_4.addWidget(self.measure_type, 1, 0, 1, 1)
        self.freq_list = QtWidgets.QComboBox(self.frame_2)
        self.freq_list.setEnabled(False)
        self.freq_list.setObjectName("freq_list")
        self.gridLayout_4.addWidget(self.freq_list, 1, 1, 1, 1)
        self.qcm_temp_ctrl = QtWidgets.QCheckBox(self.frame_2)
        self.qcm_temp_ctrl.setEnabled(False)
        self.qcm_temp_ctrl.setObjectName("qcm_temp_ctrl")
        self.gridLayout_4.addWidget(self.qcm_temp_ctrl, 2, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_4)
        self.gridLayout_5.addWidget(self.frame_2, 2, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_5, 0, 2, 2, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget6)
        self.label_7.setObjectName("label_7")
        self.gridLayout_7.addWidget(self.label_7, 0, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.layoutWidget6)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_3.setLineWidth(16)
        self.frame_3.setMidLineWidth(6)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.file_dest = QtWidgets.QLineEdit(self.frame_3)
        self.file_dest.setEnabled(False)
        self.file_dest.setObjectName("file_dest")
        self.gridLayout_6.addWidget(self.file_dest, 3, 0, 1, 1)
        self.file_select = QtWidgets.QToolButton(self.frame_3)
        self.file_select.setEnabled(False)
        self.file_select.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ui\\resources\\folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.file_select.setIcon(icon3)
        self.file_select.setObjectName("file_select")
        self.gridLayout_6.addWidget(self.file_select, 3, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        self.label_6.setObjectName("label_6")
        self.gridLayout_6.addWidget(self.label_6, 1, 0, 1, 1)
        self.auto_export = QtWidgets.QCheckBox(self.frame_3)
        self.auto_export.setObjectName("auto_export")
        self.gridLayout_6.addWidget(self.auto_export, 0, 0, 1, 2)
        self.verticalLayout_4.addLayout(self.gridLayout_6)
        self.gridLayout_7.addWidget(self.frame_3, 1, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_7, 2, 0, 2, 1)
        self.verticalLayout_6.addWidget(self.splitter_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 22))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Export = QtWidgets.QMenu(self.menu_File)
        self.menu_Export.setObjectName("menu_Export")
        self.menu_Edit = QtWidgets.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menu_Update = QtWidgets.QMenu(self.menu_Edit)
        self.menu_Update.setObjectName("menu_Update")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Connect = QtWidgets.QAction(MainWindow)
        self.action_Connect.setObjectName("action_Connect")
        self.action_Quit = QtWidgets.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.action_Resistor = QtWidgets.QAction(MainWindow)
        self.action_Resistor.setObjectName("action_Resistor")
        self.action_Voltage = QtWidgets.QAction(MainWindow)
        self.action_Voltage.setObjectName("action_Voltage")
        self.action_Reset_Recorded_Data = QtWidgets.QAction(MainWindow)
        self.action_Reset_Recorded_Data.setObjectName("action_Reset_Recorded_Data")
        self.action_All = QtWidgets.QAction(MainWindow)
        self.action_All.setObjectName("action_All")
        self.action_Resistance = QtWidgets.QAction(MainWindow)
        self.action_Resistance.setObjectName("action_Resistance")
        self.action_Humidity = QtWidgets.QAction(MainWindow)
        self.action_Humidity.setObjectName("action_Humidity")
        self.action_Temperature = QtWidgets.QAction(MainWindow)
        self.action_Temperature.setObjectName("action_Temperature")
        self.action_Amplitude = QtWidgets.QAction(MainWindow)
        self.action_Amplitude.setObjectName("action_Amplitude")
        self.action_Phase = QtWidgets.QAction(MainWindow)
        self.action_Phase.setObjectName("action_Phase")
        self.actionDissipation = QtWidgets.QAction(MainWindow)
        self.actionDissipation.setObjectName("actionDissipation")
        self.actionAbsorption = QtWidgets.QAction(MainWindow)
        self.actionAbsorption.setObjectName("actionAbsorption")
        self.menu_Export.addAction(self.action_All)
        self.menu_Export.addSeparator()
        self.menu_Export.addAction(self.action_Resistance)
        self.menu_Export.addAction(self.action_Humidity)
        self.menu_Export.addAction(self.action_Temperature)
        self.menu_Export.addAction(self.action_Amplitude)
        self.menu_Export.addAction(self.action_Phase)
        self.menu_Export.addAction(self.actionDissipation)
        self.menu_Export.addAction(self.actionAbsorption)
        self.menu_File.addAction(self.action_Connect)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.menu_Export.menuAction())
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Update.addAction(self.action_Resistor)
        self.menu_Update.addAction(self.action_Voltage)
        self.menu_Edit.addAction(self.menu_Update.menuAction())
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Reset_Recorded_Data)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
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

        self.retranslateUi(MainWindow)
        self.auto_export.toggled['bool'].connect(self.file_dest.setEnabled) # type: ignore
        self.auto_export.toggled['bool'].connect(self.file_select.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.htr_serial, self.qcm_serial)
        MainWindow.setTabOrder(self.qcm_serial, self.qc_type)
        MainWindow.setTabOrder(self.qc_type, self.calibrate_btn)
        MainWindow.setTabOrder(self.calibrate_btn, self.measure_type)
        MainWindow.setTabOrder(self.measure_type, self.freq_list)
        MainWindow.setTabOrder(self.freq_list, self.qcm_temp_ctrl)
        MainWindow.setTabOrder(self.qcm_temp_ctrl, self.auto_export)
        MainWindow.setTabOrder(self.auto_export, self.file_dest)
        MainWindow.setTabOrder(self.file_dest, self.start_btn)
        MainWindow.setTabOrder(self.start_btn, self.stop_btn)
        MainWindow.setTabOrder(self.stop_btn, self.reset_btn)
        MainWindow.setTabOrder(self.reset_btn, self.file_select)
        MainWindow.setTabOrder(self.file_select, self.resist_avg)
        MainWindow.setTabOrder(self.resist_avg, self.avg_resist_50)
        MainWindow.setTabOrder(self.avg_resist_50, self.avg_resist_15)
        MainWindow.setTabOrder(self.avg_resist_15, self.humd_avg)
        MainWindow.setTabOrder(self.humd_avg, self.humd_avg_50)
        MainWindow.setTabOrder(self.humd_avg_50, self.humd_avg_15)
        MainWindow.setTabOrder(self.humd_avg_15, self.temp_avg)
        MainWindow.setTabOrder(self.temp_avg, self.freq_f9)
        MainWindow.setTabOrder(self.freq_f9, self.freq_f7)
        MainWindow.setTabOrder(self.freq_f7, self.temp_avg_50)
        MainWindow.setTabOrder(self.temp_avg_50, self.temp_avg_15)
        MainWindow.setTabOrder(self.temp_avg_15, self.freq_f1)
        MainWindow.setTabOrder(self.freq_f1, self.freq_f3)
        MainWindow.setTabOrder(self.freq_f3, self.freq_f5)
        MainWindow.setTabOrder(self.freq_f5, self.diss_d9)
        MainWindow.setTabOrder(self.diss_d9, self.diss_d5)
        MainWindow.setTabOrder(self.diss_d5, self.diss_d7)
        MainWindow.setTabOrder(self.diss_d7, self.perm_status)
        MainWindow.setTabOrder(self.perm_status, self.diss_d3)
        MainWindow.setTabOrder(self.diss_d3, self.diss_d1)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sensor Fusion"))
        self.label_21.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Resistance (Ohm)</span></p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "Average (<50)"))
        self.label_11.setText(_translate("MainWindow", "Average (<15)"))
        self.label_9.setText(_translate("MainWindow", "Average"))
        self.label_22.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Humidity (%RH)</span></p></body></html>"))
        self.label_15.setText(_translate("MainWindow", "Average"))
        self.label_16.setText(_translate("MainWindow", "Average (<50)"))
        self.label_17.setText(_translate("MainWindow", "Average (<15)"))
        self.label_23.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Temperature (degC)</span></p></body></html>"))
        self.label_18.setText(_translate("MainWindow", "Average"))
        self.label_20.setText(_translate("MainWindow", "Average (<15)"))
        self.label_19.setText(_translate("MainWindow", "Average (<50)"))
        self.label_34.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Frequency (Hz)</span></p></body></html>"))
        self.label_24.setText(_translate("MainWindow", "F1"))
        self.label_25.setText(_translate("MainWindow", "F3"))
        self.label_26.setText(_translate("MainWindow", "F5"))
        self.label_27.setText(_translate("MainWindow", "F7"))
        self.label_28.setText(_translate("MainWindow", "F9"))
        self.label_33.setText(_translate("MainWindow", "D9"))
        self.label_32.setText(_translate("MainWindow", "D7"))
        self.label_30.setText(_translate("MainWindow", "D3"))
        self.label_31.setText(_translate("MainWindow", "D5"))
        self.label_29.setText(_translate("MainWindow", "D1"))
        self.label_35.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Dissipation (ppm)</span></p></body></html>"))
        self.label_13.setText(_translate("MainWindow", "HTR Serial Sensor"))
        self.label_14.setText(_translate("MainWindow", "QCM Serial Sensor"))
        self.qc_type.setItemText(0, _translate("MainWindow", "5 MHz"))
        self.qc_type.setItemText(1, _translate("MainWindow", "10 MHz"))
        self.calibrate_btn.setText(_translate("MainWindow", "Calibrate"))
        self.label.setText(_translate("MainWindow", "Quartz Crystal Type"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Step 1. Calibration</span></p></body></html>"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Step 4. Start</span></p></body></html>"))
        self.reset_btn.setText(_translate("MainWindow", "Reset"))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.stop_btn.setText(_translate("MainWindow", "Stop"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Step 2. Setup Measurement</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Measurement Type"))
        self.label_3.setText(_translate("MainWindow", "Frequency"))
        self.measure_type.setItemText(0, _translate("MainWindow", "Single Measurement"))
        self.measure_type.setItemText(1, _translate("MainWindow", "Multiple Measurements"))
        self.qcm_temp_ctrl.setText(_translate("MainWindow", "Temperature Control"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Step 3. Exportation</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "File Destination"))
        self.auto_export.setText(_translate("MainWindow", "Auto Export Data on Stop"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Export.setTitle(_translate("MainWindow", "&Export"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.menu_Update.setTitle(_translate("MainWindow", "&Update References"))
        self.action_Connect.setText(_translate("MainWindow", "&Connect"))
        self.action_Quit.setText(_translate("MainWindow", "&Quit"))
        self.action_Quit.setToolTip(_translate("MainWindow", "Quit the program"))
        self.action_Resistor.setText(_translate("MainWindow", "&Resistor"))
        self.action_Resistor.setToolTip(_translate("MainWindow", "Update the reference resistor"))
        self.action_Voltage.setText(_translate("MainWindow", "&Voltage"))
        self.action_Voltage.setToolTip(_translate("MainWindow", "Update the reference voltage"))
        self.action_Reset_Recorded_Data.setText(_translate("MainWindow", "&Reset Recorded Data"))
        self.action_Reset_Recorded_Data.setToolTip(_translate("MainWindow", "Reset the recorded data up to this point"))
        self.action_All.setText(_translate("MainWindow", "&All"))
        self.action_All.setToolTip(_translate("MainWindow", "Exports all data"))
        self.action_Resistance.setText(_translate("MainWindow", "&Resistance"))
        self.action_Resistance.setToolTip(_translate("MainWindow", "Exports resistance data only"))
        self.action_Humidity.setText(_translate("MainWindow", "&Humidity"))
        self.action_Humidity.setToolTip(_translate("MainWindow", "Exports humidity data only"))
        self.action_Temperature.setText(_translate("MainWindow", "&Temperature"))
        self.action_Temperature.setToolTip(_translate("MainWindow", "Exports temperature data only"))
        self.action_Amplitude.setText(_translate("MainWindow", "&Amplitude"))
        self.action_Phase.setText(_translate("MainWindow", "&Phase"))
        self.actionDissipation.setText(_translate("MainWindow", "Dissipation"))
        self.actionAbsorption.setText(_translate("MainWindow", "Resonance &Frequency"))