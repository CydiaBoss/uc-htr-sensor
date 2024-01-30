# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCloseEvent, QResizeEvent
from PyQt5.QtWidgets import QMessageBox

import pyqtgraph as pq

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget
from constants import REF_RESIST_UNIT

from tools import active_ports, identical_list

class Ui_MainWindow(QtWidgets.QMainWindow):

    # Signals
    
    # Set up Data Collection Signals
    resist_avg_sig = QtCore.pyqtSignal('QString')
    resist_avg_15_sig = QtCore.pyqtSignal('QString')
    resist_avg_50_sig = QtCore.pyqtSignal('QString')

    def setupUi(self, MainWindow):
        # Look for ports for menu stuff
        self.ports = active_ports()

        # Setup Signals
        self.resist_avg_sig.connect(self.update_resist_avg)
        self.resist_avg_15_sig.connect(self.update_resist_avg_15)
        self.resist_avg_50_sig.connect(self.update_resist_avg_50)

        # Main Window Functions
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\resources/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.mainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1000, 600))
        self.centralwidget.setObjectName("centralwidget")

        # Upper Widget
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1000, 40))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        title_font = QtGui.QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_font.setWeight(75)

        # Titles
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setFont(title_font)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.verticalLayout_7.addWidget(self.label)
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)

        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setFont(title_font)
        self.label_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setFont(title_font)
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
        self.resist_plot = LivePlotWidget(self.widget1, labels={"bottom": "Time since Connection", "left": f"Resistance ({REF_RESIST_UNIT}Ω)"})
        self.resist_curve = LiveLinePlot(brush="red", pen="red")
        self.resist_plot.addItem(self.resist_curve)
        self.resist_data = DataConnector(self.resist_curve, update_rate=1.0)
        self.verticalLayout_3.addWidget(self.resist_plot)

        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Humidity Plot
        self.humidity_plot = LivePlotWidget(self.widget1, labels={"bottom": "Time since Connection", "left": "Humidity (%RH)"})
        self.humidity_curve = LiveLinePlot(brush="green", pen="green")
        self.humidity_plot.addItem(self.humidity_curve)
        self.humidity_data = DataConnector(self.humidity_curve, update_rate=1.0)
        self.verticalLayout_2.addWidget(self.humidity_plot)

        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # Temperature Plot
        self.temperature_plot = LivePlotWidget(self.widget1, labels={"bottom": "Time since Connection", "left": "Temperature (°C)"})
        self.temperature_curve = LiveLinePlot(brush="blue", pen="blue")
        self.temperature_plot.addItem(self.temperature_curve)
        self.temperature_data = DataConnector(self.temperature_curve, update_rate=1.0)
        self.verticalLayout.addWidget(self.temperature_plot)

        self.horizontalLayout.addLayout(self.verticalLayout)

        # Bottom Widgets
        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(0, 380, 1000, 100))
        self.widget2.setObjectName("widget3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        node_font = QtGui.QFont()
        node_font.setPointSize(10)
        node_font.setBold(True)
        node_font.setWeight(75)
        node_value_font = QtGui.QFont()
        node_value_font.setPointSize(10)
        node_value_font.setWeight(30)

        # Resistance Nodes
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_4 = QtWidgets.QLabel(self.widget2)
        self.label_4.setFont(node_font)
        self.label_4.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_4.setObjectName("label_4")
        self.resistance_avg = QtWidgets.QLabel(self.widget2)
        self.resistance_avg.setFont(node_value_font)
        self.resistance_avg.setAlignment(QtCore.Qt.AlignHCenter)
        self.resistance_avg.setObjectName("resistance_avg")
        self.verticalLayout_8.addWidget(self.label_4)
        self.verticalLayout_8.addWidget(self.resistance_avg)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_5 = QtWidgets.QLabel(self.widget2)
        self.label_5.setFont(node_font)
        self.label_5.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_5.setObjectName("label_5")
        self.resistance_avg_50 = QtWidgets.QLabel(self.widget2)
        self.resistance_avg_50.setFont(node_value_font)
        self.resistance_avg_50.setAlignment(QtCore.Qt.AlignHCenter)
        self.resistance_avg_50.setObjectName("resistance_avg_50")
        self.verticalLayout_9.addWidget(self.label_5)
        self.verticalLayout_9.addWidget(self.resistance_avg_50)
        self.horizontalLayout_3.addLayout(self.verticalLayout_9)
        
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.widget2)
        self.label_6.setFont(node_font)
        self.label_6.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_6.setObjectName("label_6")
        self.resistance_avg_15 = QtWidgets.QLabel(self.widget2)
        self.resistance_avg_15.setFont(node_value_font)
        self.resistance_avg_15.setAlignment(QtCore.Qt.AlignHCenter)
        self.resistance_avg_15.setObjectName("resistance_avg_15")
        self.verticalLayout_10.addWidget(self.label_6)
        self.verticalLayout_10.addWidget(self.resistance_avg_15)
        self.horizontalLayout_3.addLayout(self.verticalLayout_10)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Connect = QtWidgets.QMenu(MainWindow)
        self.menu_Connect.setObjectName("action_Connect")
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
        self.action_Refresh = QtWidgets.QAction(MainWindow)
        self.action_Refresh.setObjectName("action_Refresh")
        self.action_Settings = QtWidgets.QAction(MainWindow)
        self.action_Settings.setObjectName("action_Settings")
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
        self.menu_Connect.addAction(self.action_Refresh)
        self.menu_Connect.addSeparator()

        # COM Menu
        self.action_ports : List[QtWidgets.QAction] = []
        for port in self.ports:
            temp_port_action = QtWidgets.QAction(MainWindow)
            temp_port_action.setObjectName(port)
            self.action_ports.append(temp_port_action)
            self.menu_Connect.addAction(temp_port_action)

        self.menu_Export.addAction(self.action_All)
        self.menu_Export.addSeparator()
        self.menu_Export.addAction(self.action_Resistance)
        self.menu_Export.addAction(self.action_Humidity)
        self.menu_Export.addAction(self.action_Temperature)
        self.menu_File.addAction(self.menu_Connect.menuAction())
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
        self.label.setText(_translate("MainWindow", "Live Resistance Data"))
        self.label_2.setText(_translate("MainWindow", "Live Humidity Data"))
        self.label_3.setText(_translate("MainWindow", "Live Temperature Data"))
        self.label_4.setText(_translate("MainWindow", "Average Resistance"))
        self.label_5.setText(_translate("MainWindow", "Average Resistance (Last 50)"))
        self.label_6.setText(_translate("MainWindow", "Average Resistance (Last 15)"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Export.setTitle(_translate("MainWindow", "&Export"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.menu_Update.setTitle(_translate("MainWindow", "&Update References"))
        self.menu_Connect.setTitle(_translate("MainWindow", "&Connect"))
        self.action_Quit.setText(_translate("MainWindow", "&Quit"))
        self.action_Quit.setToolTip(_translate("MainWindow", "Quit the program"))
        self.action_Resistor.setText(_translate("MainWindow", "&Resistor"))
        self.action_Resistor.setToolTip(_translate("MainWindow", "Update the reference resistor"))
        self.action_Voltage.setText(_translate("MainWindow", "&Voltage"))
        self.action_Voltage.setToolTip(_translate("MainWindow", "Update the reference voltage"))
        self.action_Reset_Recorded_Data.setText(_translate("MainWindow", "&Reset Recorded Data"))
        self.action_Reset_Recorded_Data.setToolTip(_translate("MainWindow", "Reset the recorded data up to this point"))
        self.action_Refresh.setText(_translate("MainWindow", "&Refresh"))
        self.action_Refresh.setToolTip(_translate("MainWindow", "Refresh the list of used ports"))
        self.action_All.setText(_translate("MainWindow", "&All"))
        self.action_All.setToolTip(_translate("MainWindow", "Exports all data"))
        self.action_Resistance.setText(_translate("MainWindow", "&Resistance"))
        self.action_Resistance.setToolTip(_translate("MainWindow", "Exports resistance data only"))
        self.action_Humidity.setText(_translate("MainWindow", "&Humidity"))
        self.action_Humidity.setToolTip(_translate("MainWindow", "Exports humidity data only"))
        self.action_Temperature.setText(_translate("MainWindow", "&Temperature"))
        self.action_Temperature.setToolTip(_translate("MainWindow", "Exports temperature data only"))

        # All Port Menu
        for action_port in self.action_ports:
            action_port.setText(_translate("MainWindow", action_port.objectName().upper()))
            action_port.setToolTip(_translate("MainWindow", "Switches to this port"))

    def updatePorts(self):
        """
        Update available ports to select
        """
        old_ports = self.ports
        self.ports = active_ports()
        self.ports.append()

        # Ignore if nothing changed
        if identical_list(old_ports, self.ports):
            return
        
        # Remove all menu items
        for action_port in self.action_ports:
            self.menu_Connect.removeAction(action_port)

        # Add New COM Menu
        self.action_ports : List[QtWidgets.QAction] = []
        for port in self.ports:
            temp_port_action = QtWidgets.QAction(self.mainWindow)
            temp_port_action.setObjectName(port)
            self.action_ports.append(temp_port_action)
            self.menu_Connect.addAction(temp_port_action)

    # Events

    def resizeEvent(self, a0: QResizeEvent) -> None:
        '''
        Update Widgets in resizing
        '''
        new_width = a0.size().width()
        new_height = a0.size().height()
        self.widget.setGeometry(QtCore.QRect(0, 0, new_width, 40))
        self.widget1.setGeometry(QtCore.QRect(0, 40, new_width, int(new_height*340/600)))
        self.widget2.setGeometry(QtCore.QRect(0, 40 + int(new_height*340/600), new_width, int(new_height*100/600)))
        return super().resizeEvent(a0)
        
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        # Ask for confirmation before closing
        confirmation = QMessageBox.question(self, "Confirmation", "Are you sure you want to close the application?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            a0.accept()
        else:
            a0.ignore() 
    
    # Slots

    @QtCore.pyqtSlot()
    def on_action_Quit_triggered(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_action_Refresh_triggered(self):
        self.updatePorts()

    # Resistance Stuff

    @QtCore.pyqtSlot(str)
    def update_resist_avg(self, value):
        self.resistance_avg.setText(value)

    @QtCore.pyqtSlot(str)
    def update_resist_avg_15(self, value):
        self.resistance_avg_15.setText(value)

    @QtCore.pyqtSlot(str)
    def update_resist_avg_50(self, value):
        self.resistance_avg_50.setText(value)