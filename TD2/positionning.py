from math import log10, pow, pi
import csv


class RSSISample:
    def __init__(self, mac_address: str, rssi: list[float]) -> None:
        self.mac_address = mac_address
        self.rssi = rssi

    def convert_to_dbm(self, mw: float) -> float:
        return 10*log10(mw)

    def convert_to_mw(self, dbm: float) -> float:
        return pow(10, dbm/10)

    def get_average_rssi(self) -> float:
        sum = 0
        for value in self.rssi:
            sum += self.convert_to_mw(value)
        result = sum / len(self.rssi)
        return self.convert_to_dbm(result)


class FingerprintSample:
    def __init__(self, samples: list[RSSISample]) -> None:
        self.samples = samples

    def is_mac_address_known(self, mac_address: str):
        if len(self.samples) == 0:
            return False, None
        else:
            for index, rssi_sample in enumerate(self.samples):
                if rssi_sample.mac_address == mac_address:
                    return True, index
            return False, None

    def add_rssi_sample(self, rssi_sample: RSSISample):
        self.samples.append(rssi_sample)

    def add_rssi_value_to_sample(self, sample_index: int, rssi_value: float):
        self.samples[sample_index].rssi.append(rssi_value)

    def get_all_couples(self):
        couples = []
        for sample in self.samples:
            couples.append(sample.mac_address)
            couples.append(round(sample.get_average_rssi(), 2))
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

        def rssi_distance(self, second_sample: FingerprintSample) -> float:
            pass

        def simple_matching(self, db: FingerprintDatabase) -> SimpleLocation:
            pass


class NormHisto:
    def __inti__(self, histo: dict[int, float]):
        self.histogram = histo

    def probability(self, histo2: NormHisto) -> float:
        pass

    def histogram_matching(self, db: FingerprintDatabase) -> float:
        pass


class GaussModel:
    def __init__(self, avg: float, stddev: float):
        self.average_rssi = avg
        self.standard_deviation = stddev

    def histogram_from_gauss(self) -> RSSISample:
        pass


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

    def load_data(self, filename: str):
        with open(filename, "r") as csv_file:
            for row in csv.reader(csv_file, delimiter=","):
                if len(row) < 5:
                    continue

                row_location = SimpleLocation(row[0], row[1], row[2])
                row_adresses = row[4:]
                couples_list = [[row_adresses[i], float(
                    row_adresses[i+1])] for i in range(0, len(row_adresses), 2)]

                position_known, fgp_index = self._is_location_known(
                    row_location)
                if not position_known:
                    fgp_sample = FingerprintSample([])
                    for couple in couples_list:
                        mac_address_known, rssi_spl_index = fgp_sample.is_mac_address_known(
                            couple[0])
                        if not mac_address_known:
                            fgp_sample.add_rssi_sample(
                                RSSISample(couple[0], [couple[1]]))
                        else:
                            fgp_sample.add_rssi_value_to_sample(
                                rssi_spl_index, (couple[1]))

                    self.db.append(Fingerprint(row_location, fgp_sample))
                else:
                    for couple in couples_list:
                        mac_address_known, rssi_spl_index = self.db[fgp_index].sample.is_mac_address_known(
                            couple[0])
                        if not mac_address_known:
                            self.db[fgp_index].sample.add_rssi_sample(
                                RSSISample(couple[0], [couple[1]]))
                        else:
                            self.db[fgp_index].sample.add_rssi_value_to_sample(
                                rssi_spl_index, (couple[1]))

    def generate_result_file(self):
        with open("result.csv", "w") as result_file:
            writer = csv.writer(result_file)

            for fingerprint in self.db:
                position = fingerprint.position.get_as_list()
                direction = [0]
                couples = fingerprint.sample.get_all_couples()
                line = position + direction + couples
                writer.writerow(line)

    def get_rssi_sample_by_mac(mac: str):
        pass


class AccessPoint:
    def __init__(self, mac: str, loc: SimpleLocation = SimpleLocation(0, 0, 0), f: float = 2417000000, a: float = 5.0, p: float = 20.0):
        self.mac = mac
        self.mac_address = mac
        self.location = loc
        self.output_power_dbm = p
        self.antenna_dbi = a
        self.output_frequency_hz = f
        pass


def compute_FBCM_index(distance: float, rssi_values: RSSISample, ap: AccessPoint) -> float:
    """
Function compute_FBCM_index computes a FBCM index based on the distance (between transmitter and receiver)
and the AP parameters. We consider the mobile device's antenna gain is 2.1 dBi.
:param distance: the distance between AP and device
:param rssi_values: the RSSI values associated to the AP for current calibration point. Use their average value.
:return: one value for the FBCM index
"""
    GR = 2.1
    GT = ap.antenna_dbi
    PR = RSSISample.get_average_rssi()
    PT = ap.output_power_dbm
    c = 299792458
    l = c/ap.output_frequency_hz
    l4pi = pow((l/(4*pi)), 2)
    distance = abs(distance)

    if distance == 0:
        distance = 0.00001

    index = (PT-PR+GT+GR+20*log10(l/(4*pi), 10)) / (10*log10(distance))
    return index


def estimate_distance(rssi_avg: float, fbcm_index: float, ap: AccessPoint) -> float:
    """
    Function estimate_distance estimates the distance between an access point and a test point based on
    the test point rssi sample.
    :param rssi: average RSSI value for test point
    :param fbcm_index: index to use
    :param ap: access points parameters used in FBCM
    :return: the distance (meters)
    """
    GR = (2.1)
    GT = (ap.antenna_dbi)
    PR = (rssi_avg)
    PT = (ap.output_power_dbm)
    c = 299792458
    l = c/ap.output_frequency_hz
    l4pi = pow((l/(4 * pi)), 2)

    estimated_dist = pow(10, (PT-PR+GT+GR+20*log10(l/(4*pi)))/(10*fbcm_index))
    return estimated_dist


if __name__ == "__main__":
    AP = {"00:13:ce:95:e1:6f": AccessPoint("00:13:ce:95:e1:6f", SimpleLocation(4.93, 25.81, 3.55), 2417000000, 5.0, 20.0),
          "00:13:ce:95:de:7e": AccessPoint("00:13:ce:95:de:7e", SimpleLocation(4.83, 10.88, 3.78), 2417000000, 5.0, 20.0),
          "00:13:ce:97:78:79": AccessPoint("00:13:ce:97:78:79", SimpleLocation(20.05, 28.31, 3.74), 2417000000, 5.0, 20.0),
          "00:13:ce:8f:77:43": AccessPoint("00:13:ce:8f:77:43", SimpleLocation(4.13, 7.085, 0.80), 2417000000, 5.0, 20.0),
          "00:13:ce:8f:78:d9": AccessPoint("00:13:ce:8f:78:d9", SimpleLocation(5.74, 30.35, 2.04), 2417000000, 5.0, 20.0)}
