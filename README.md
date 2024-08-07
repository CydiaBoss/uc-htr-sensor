# QCM H<sub>2</sub> Sensing System Software
This software is developed to interface with the many sensors in the QCM hydrogen sensing system. It records the QCM data, as well as the resistance, humidity, and temperature. The goal of the system is to detect the presenses of hydrogen gas at a low concentration (100 ppm in air).

## Features
- Discover the peak resonance frequencies of a 5MHz and 10MHz quartz crystal chip
- Record date from the QCM, HTR (Humidity, Temperature, Resistance), and the R sensors
- Save and export raw data to the a csv file
- Apply noise filtration to resistance, humidity, and temperature data
- View plots of the data
- Ability to localize software
- Live translations as the software is running
- Customize graph view

## Installation Guide
To install and run this software, you will need a few dependencies. You will need to install the National Instruments' DAQ drivers to be able to comunicate with the R sensor. This can be found <a href=https://www.ni.com/en/support/downloads/drivers/download.ni-daq-mx.html>at the NI site</a>.

### Source Code Launch
You can either clone this repository or run the Windows binary. To run the repository, create a virtual environment using the requirements.txt with Python version 3.11. Then, the application can be started by opening a terminal in the repository directory and running the \_\_main\_\_.py file with the following command.

`python __main__.py`

### Windows Binary Launch
If you are using Windows, this is the easier option. Simply run the installer and relax.