from io import TextIOWrapper
from multiprocessing import Queue
import os
from typing import Union

from PyQt5.QtCore import QObject

from misc.constants import AUTO_FLUSH, SETTINGS

class DataSaving(QObject):
	"""
	Saving Data Engine
	"""

	def __init__(self, parent : QObject=None, file_name : str="") -> None:
		super().__init__(parent)
		# Setup Filename
		self.file_name = file_name.strip()
		self.file : Union[TextIOWrapper, None] = None
		self.row_count = 0

		# Setup Sensor Settings
		self.htr = True
		self.r = True
		self.qcm = True

		# Setup Queues for all Data Types
		# HTR
		self.htr_time = Queue()
		self.htr_humid = Queue()
		self.htr_temp = Queue()
		self.htr_resist = Queue()

		# R
		self.r_time = Queue()
		self.r_resist = Queue()
		
		# QCM
		self.freqs = []
		self.qcm_time = Queue()
		self.qcm_freq = [Queue(),]
		self.qcm_diss = [Queue(),]
		self.qcm_temp = Queue()

	def set_htr(self, state : bool):
		"""
		Toggle HTR
		"""
		self.htr = state

	def set_r(self, state : bool):
		"""
		Toggle R
		"""
		self.r = state

	def set_qcm(self, state : bool):
		"""
		Toggle QCM
		"""
		self.qcm = state

	def set_freqs(self, freqs : list[float]):
		"""
		Set Testing Frequencies
		"""
		self.freqs = freqs
		self.qcm_freq.clear()
		self.qcm_diss.clear()
		for _ in range(len(self.freqs)):
			self.qcm_freq.append(Queue())
			self.qcm_diss.append(Queue())

	def open(self):
		"""
		Open file
		"""
		# Make D oirectory if needed
		dir_name = os.path.dirname(self.file_name)
		if dir_name.strip() != "":
			os.makedirs(dir_name, exist_ok=True)
			
		self.file = open(self.file_name, "w")
		# Add Header
		self.header = ""

		# HTR?
		if self.htr:
			self.header += '"Time (HTR)","Humidity (%RH)","Temperature (degC)",'

			# Ignore R if included
			if not self.r:
				self.header += f'"Resistance ({SETTINGS.get_setting('ref_resist_unit').strip()}Ohm)",'

			# Column of Division
			self.header += ","

		# R?
		if self.r:
			self.header += f'"Time (R)","Resistance ({SETTINGS.get_setting('ref_resist_unit').strip()}Ohm)",,'

		# QCM?
		if self.qcm:
			self.header += '"Time (QCM)","Temperature (degC)",'

			# Duplicate Columns
			for freq in self.freqs:
				self.header += f'"Resonance Frequency at {freq} (Hz)","Dissipation at {freq} (ppm)",'

		# Write Header
		self.header += "\n"
		self.file.write(self.header)
		self.row_count += 1

	def is_htr_empty(self) -> bool:
		"""
		Checks if HTR has pending data
		"""
		empty = self.htr_time.empty() or self.htr_humid.empty() or self.htr_temp.empty()
		if not self.r:
			empty = empty or self.htr_resist.empty()
		return empty

	def is_r_empty(self) -> bool:
		"""
		Checks if R has pending data
		"""
		return self.r_time.empty() or self.r_resist.empty()

	def is_qcm_empty(self) -> bool:
		"""
		Checks if QCM has pending data
		"""
		empty = self.qcm_time.empty() or self.qcm_temp.empty()
		for i in range(len(self.freqs)):
			empty = empty or self.qcm_freq[i].empty() or self.qcm_diss[i].empty()
		return empty
	
	def pull_htr_data(self) -> list[float]:
		"""
		Grabs the latest HTR data
		"""
		htr_list = [
			self.htr_time.get(),
			self.htr_humid.get(),
			self.htr_temp.get(),
		]
		if not self.r:
			htr_list.append(self.htr_resist.get())
		return htr_list
	
	def pull_r_data(self) -> list[float]:
		"""
		Grabs the latest R data
		"""
		return [
			self.r_time.get(),
			self.r_resist.get(),
		]
	
	def pull_qcm_data(self) -> list[float]:
		"""
		Grabs the latest QCM data
		"""
		qcm_list = [
			self.qcm_time.get(),
			self.qcm_temp.get(),
		]
		for i in range(len(self.freqs)):
			qcm_list.append(self.qcm_freq[i].get())
			qcm_list.append(self.qcm_diss[i].get())
		return qcm_list

	def write(self):
		"""
		Write data to file
		"""
		while (not self.htr or not self.is_htr_empty()) and (not self.r or not self.is_r_empty()) and (not self.qcm or not self.is_qcm_empty()):
			# Generate next row
			row = ""

			# HTR?
			if self.htr:
				for value in self.pull_htr_data():
					row += f'"{value}",'

				# Column of Division
				row += ","

			# R?
			if self.r:
				for value in self.pull_r_data():
					row += f'"{value}",'

				# Column of Division
				row += ","

			# QCM?
			if self.qcm:
				for value in self.pull_qcm_data():
					row += f'"{value}",'

			# Write Row
			row += "\n"
			self.file.write(row)
			self.row_count += 1

			# Auto flush
			if self.row_count % AUTO_FLUSH == 0:
				self.file.flush()

	def close(self):
		"""
		Flushes the remaining data and closes the file
		"""
		# Store for optimzation
		htr_empty = self.is_htr_empty()
		r_empty = self.is_r_empty()
		qcm_empty = self.is_qcm_empty()

		# Flushing
		while not htr_empty or not r_empty or not qcm_empty:
			# Generate next row
			row = ""

			# HTR?
			if not htr_empty:
				for value in self.pull_htr_data():
					row += f'"{value}",'

				# Column of Division
				row += ","
			
			# No more HTR data, so excess space
			elif self.htr:
				row += ",,,"

				# Add , if resist
				if not self.r:
					row += ","

				# Column of Division
				row += ","

			# R?
			if not r_empty:
				for value in self.pull_r_data():
					row += f'"{value}",'

				# Column of Division
				row += ","
			
			# No more R data, so excess space
			elif self.r:
				row += ",,,"

			# QCM?
			if not qcm_empty:
				for value in self.pull_qcm_data():
					row += f'"{value}",'

			# Write Row
			row += "\n"
			self.file.write(row)
			self.row_count += 1

			# Auto flush
			if self.row_count % AUTO_FLUSH == 0:
				self.file.flush()

			# Next Iteration Rules
			htr_empty = self.is_htr_empty()
			r_empty = self.is_r_empty()
			qcm_empty = self.is_qcm_empty()

		# Final flush and Close
		self.file.flush()
		self.file.close()