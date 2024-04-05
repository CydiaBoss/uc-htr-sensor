@echo off
pyuic5 ui/main_gui.ui -o main_gui.py
echo Replace "object" with "QtWidget.QMainWindow"