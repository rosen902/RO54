from math import log10, pow
import csv

class RSSISample:
	def __init__(self, mac_address: str, rssi: list[float]) -> None:
		self.mac_address = mac_address
		self.rssi = rssi

	def convert_to_dbm(self, mw : float) -> float:
		return 10*log10(mw)

	def convert_to_mw(self, dbm : float) -> float:
		return pow(10,dbm/10)

	def get_average_rssi(self) -> float:
		sum = 0
		for value in self.rssi:
			sum += self.convert_to_mw(value)
		result = sum / len(self.rssi)
		return self.convert_to_dbm(result)



class FingerprintSample:
	def __init__(self, samples: list[RSSISample]) -> None:
		self.samples = samples
	
	def is_mac_address_known(self, mac_address : str):
		if len(self.samples) == 0:
			return False, None
		else:
			for index, rssi_sample in enumerate(self.samples):
				if rssi_sample.mac_address == mac_address:
					return True, index	
			return False, None
	
	def add_rssi_sample(self, rssi_sample : RSSISample):
		self.samples.append(rssi_sample)

	def add_rssi_value_to_sample(self, sample_index: int, rssi_value: float):
		self.samples[sample_index].rssi.append(rssi_value)

	def get_all_couples(self):
		couples = []
		for sample in self.samples:
			couples.append(sample.mac_address)
			couples.append(round(sample.get_average_rssi(),2))
		return couples


class SimpleLocation:
	def __init__(self, x: float, y: float, z: float) -> None:
		self.x = x
		self.y = y
		self.z = z
	
	def __eq__(self, __o: object) -> bool:
		if not isinstance(__o, SimpleLocation):
			return NotImplemented
		return self.x == __o.x and self.y == __o.y and self.z == __o.z
	
	def get_as_list(self):
		return [self.x, self.y, self.z]



class Fingerprint:
	def __init__(self, position: SimpleLocation, sample: FingerprintSample) -> None:
		self.position = position
		self.sample = sample


class FingerprintDatabase:
	def __init__(self) -> None:
		self.db = []
	
	def _is_location_known(self, location: SimpleLocation):
		if len(self.db) == 0:
			return False, None
		else:
			for index, fingerprint in enumerate(self.db):
				if fingerprint.position == location:
					return True, index	
			return False, None


	def load_data(self, filename : str):
		with open(filename, "r") as csv_file:
			for row in csv.reader(csv_file, delimiter=","):
				if len(row) < 5:
					continue

				row_location = SimpleLocation(row[0], row[1], row[2])
				row_adresses = row[4:]
				couples_list = [[row_adresses[i], float(row_adresses[i+1])] for i in range(0, len(row_adresses), 2)]

				position_known, fgp_index = self._is_location_known(row_location)
				if not position_known:
					fgp_sample = FingerprintSample([])
					for couple in couples_list:
						mac_address_known, rssi_spl_index = fgp_sample.is_mac_address_known(couple[0])
						if not mac_address_known:
							fgp_sample.add_rssi_sample(RSSISample(couple[0], [couple[1]]))
						else:
							fgp_sample.add_rssi_value_to_sample(rssi_spl_index, (couple[1]))

					self.db.append(Fingerprint(row_location, fgp_sample))
				else:
					for couple in couples_list:
						mac_address_known, rssi_spl_index = self.db[fgp_index].sample.is_mac_address_known(couple[0])
						if not mac_address_known:
							self.db[fgp_index].sample.add_rssi_sample(RSSISample(couple[0], [couple[1]]))
						else:
							self.db[fgp_index].sample.add_rssi_value_to_sample(rssi_spl_index, (couple[1]))
		

	def generate_result_file(self):
		with open("result.csv", "w") as result_file:
			writer = csv.writer(result_file)

			for fingerprint in self.db:
				position = fingerprint.position.get_as_list()
				direction = [0]
				couples = fingerprint.sample.get_all_couples()
				line = position + direction + couples
				writer.writerow(line)