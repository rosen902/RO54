from math import log10

def dB_to_lin(data: float) -> float:
	"""dB_to_lin
	convert from decibel to linear
	"""
	return pow(10, data / 10.)

def lin_to_dB(data: float) -> float:
	"""lin_to_dB
	convert from linear to decibel
	"""
	return 10. * log10(data)

