from math import log10, pow, pi , sqrt, floor ,exp
from positionning import SimpleLocation, Fingerprint, FingerprintSample,FingerprintDatabase

class AverageRSSI:
    def __init__(self,mac : str, rssi_average : float):
        self.mac = mac
        self.rssi_average = rssi_average

class FingerPrintAverage:
    def __init__(self, position: SimpleLocation, average_sample: list[AverageRSSI] ) -> None:
        self.position = position
        self.average_sample = average_sample

    def rssi_distance(self,second_sample : list [AverageRSSI]):
        distance = 0.0
        max_distance = 50.0
        # se base sur la distance euclidienne : distance = √((x1 - x2)² + (y1 - y2)² + ... + (xn - yn)²)
        for rssi in self.average_sample :
            for rssi2 in second_sample:
                if rssi.mac == rssi2.mac:
                    distance += abs(rssi.rssi_average - rssi2.rssi_average) ** 2
                    break
            distance += max_distance**2 #quand l'addresse mac n'est pas commune aux deux fingerprint 
        return sqrt(distance)
    
def simple_matching(database : FingerprintDatabase, sample_average : AverageRSSI ) -> SimpleLocation:
        min_dist = 99999
        min_location = SimpleLocation(0,0,0)
        database.get_db_average_RSSI()
        for fingerprint_average in database.average_rssi_db:
           # recupere position + listSample
           dist = fingerprint_average.rssi_distance(sample_average) 
           if dist <= min_dist :
               min_dist = dist
               min_location = fingerprint_average.position

        return min_location