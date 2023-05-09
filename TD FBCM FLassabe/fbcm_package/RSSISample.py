import string
from fbcm_package.Tools import lin_to_dB, dB_to_lin

class RSSISample:
	"""RSSISample
	Simple RSSISample used for FBCM computation and Fingerprint matching (a little modified)
	RSSISample is an object that store rssi values for one MAC address; so one fingerprint should handle multiples instance of RSSISample
	"""
	def __init__(self, mac_address: string) -> None:
		"""Constructor
		mac_address -> mac address of the Sample
		_signal_list -> list of RSSI for one sample
		_signal_average -> average of all RSSI values of the sample
		_averaged -> if the Sample already been averaged or not
		"""
		
		self.mac_address = mac_address
		self._signal_list = []
		self._signal_average = 0
		self._averaged = True;

	def add(self, rssi: float) -> None:
		"""add
		add a rssi value to the list
		"""
		
		self._signal_list.append(rssi)
		
		#avarage value is not correct anymore
		self._averaged = False

	def get_average_rssi(self) -> float:
		"""get_average_rssi
		return averaged value of the rssi
		"""
		
		# check if there is values in the list, otherwise return invalid average
		if len(self._signal_list) == 0:
			return -1

		# compute the average
		if not self._averaged:
			sum = 0
			for sig in self._signal_list:
				sum += dB_to_lin(sig)
			moy = sum/len(self._signal_list)
			moy_rounded = round(lin_to_dB(moy), 5)
			self._signal_average = moy_rounded
			self._averaged = True

		return self._signal_average

	def __repr__(self) -> str:
		ret = 'macAddress : '
		ret += str(self.mac_address)
		ret += ', \nsignals :('
		for RSSI in self._signal_list:
			ret = ret + str(RSSI) + ", "
		ret = ret + ')\n'
		return ret
