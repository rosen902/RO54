import string
from fbcm_package.Location import Location
from fbcm_package.RSSISample import RSSISample

class Fingerprint_header:
	"""Fingerprint_header
	Header for different types of fingerprint (see FingerprintingMatching)
	contain by default the location and a list of RSSI
	"""
	def __init__(self, position: Location) -> None:
		"""Constructor
		construct the fingerprint (default constructor)
		"""
		self.location = position
		self._RSSISample_list = []
		
	def __repr__(self) -> str:
		return 'Position :' + str(self.location) + ', RSSISample_list :' + str(self._RSSISample_list)

class Fingerprint(Fingerprint_header):
	"""Fingerprint
	Fingerprint used for FBCM calculation
	"""
	def __init__(self, position: Location) -> None:
		"""Constructor
		Build an empty fingerprint
		"""
		super().__init__(position)
	
	def add(self, RSSI: float, mac_address: string) -> None:
		"""add
		add a rssi value to the list given a specific mac address
		"""
		# look if an instance of this mac address is already stored in memory
		for RSSISample_n in self._RSSISample_list:
			if RSSISample_n.mac_address == mac_address:
    			# address mac already knowned, rssi value is added to the sample
				RSSISample_n.add(RSSI)
				break
		else:
    		# otherwise create a new instance of RSSISample and add it to the list 
			new_RSSISample = RSSISample(mac_address)
			new_RSSISample.add(RSSI)
			self._RSSISample_list.append(new_RSSISample)
