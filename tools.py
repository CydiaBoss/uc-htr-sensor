import sys, glob
import operator
from typing import List
from serial import Serial, SerialException

def active_ports() -> List[str]:
	""" 
	Gathers a list of used ports and returns them
	"""
	if sys.platform.startswith('win'):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this excludes your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')

	results = []
	for port in ports:
		try:
			s = Serial(port)
			s.close()
			results.append(port)
		except (OSError, SerialException):
			pass

	return results

def identical_list(a : list, b : list) -> bool:
	"""
	Check if two lists are identical
	"""
	for i in a:
		if operator.countOf(a, i) != operator.countOf(b, i):
			return False
	if(len(a) != len(b)):
		return False
	return True