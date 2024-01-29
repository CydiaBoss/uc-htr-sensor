# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QResizeEvent

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        # Main Window Functions
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 643)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\resources/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1000, 600))
        self.centralwidget.setObjectName("centralwidget")

        # Upper Widget
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1000, 40))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.verticalLayout_7.addWidget(self.label)
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        # Graphing Widget
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(0, 40, 1000, 340))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # Resistance Plot
        self.resist_plot = LivePlotWidget(self.widget1)
        self.resist_curve = LiveLinePlot()
        self.resist_plot.addItem(self.resist_curve)
        self.resist_data = DataConnector(self.resist_curve, max_points=150, update_rate=1.0)
        self.verticalLayout_3.addWidget(self.resist_plot)

        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Humidity Plot
        self.humidity_plot = LivePlotWidget(self.widget1)
        self.humidity_curve = LiveLinePlot()
        self.humidity_plot.addItem(self.humidity_curve)
        self.humidity_data = DataConnector(self.humidity_curve, max_points=150, update_rate=1.0)
        self.verticalLayout_2.addWidget(self.humidity_plot)

        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # Temperature Plot
        self.temperature_plot = LivePlotWidget(self.widget1)
        self.temperature_curve = LiveLinePlot()
        self.temperature_plot.addItem(self.temperature_curve)
        self.temperature_data = DataConnector(self.temperature_curve, max_points=150, update_rate=1.0)
        self.verticalLayout.addWidget(self.temperature_plot)

        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
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
        self.menu_Export.addAction(self.action_All)
        self.menu_Export.addSeparator()
        self.menu_Export.addAction(self.action_Resistance)
        self.menu_Export.addAction(self.action_Humidity)
        self.menu_Export.addAction(self.action_Temperature)
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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sensor Fusion"))
        self.label.setText(_translate("MainWindow", "Resistance"))
        self.label_2.setText(_translate("MainWindow", "Humidity"))
        self.label_3.setText(_translate("MainWindow", "Temperature"))
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

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        '''
        Update Widgets in resizing
        '''
        new_width = a0.size().width()
        self.widget.setGeometry(QtCore.QRect(0, 0, new_width, 40))
        self.widget1.setGeometry(QtCore.QRect(0, 40, new_width, 340))
        return super().resizeEvent(a0)