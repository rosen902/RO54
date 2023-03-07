import math

class RSSISample:
	def __init__(self, mac_address: str, rssi: list[float]) -> None:
		self.mac_address = mac_address
		self.rssi = rssi

	def convert_to_dbm(self, mw : float) -> float:
		return 10*math.log(mw)

	def convert_to_mw(self, dbm : float) -> float:
		return math.pow(10,dbm/10)

	def get_average_rssi(self) -> float:
		sum = 0
		for value in self.rssi:
			sum += self.convert_to_mw(value)
		result = sum / len(self.rssi)
		return self.convert_to_dbm(result)

class FingerprintSample:
	def __init__(self, samples: list[RSSISample]) -> None:
		self.samples = samples

class SimpleLocation:
	def __init__(self, x: float, y: float, z: float) -> None:
		self.x = x
		self.y = y
		self.z = z

class Fingerprint:
	def __init__(self, position: SimpleLocation, sample: FingerprintSample) -> None:
		self.position = position
		self.sample = sample

class FingerprintDatabase:
	def __init__(self) -> None:
		self.db = []