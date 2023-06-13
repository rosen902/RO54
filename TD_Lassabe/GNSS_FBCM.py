from math import log10, pow, pi , sqrt, floor ,exp
from positionning import Fingerprint, FingerprintDatabase,FingerprintSample, SimpleLocation, RSSISample
class IndexFBCM :
    def __init__(self, indexValue: float):
        #self.position = position
        self.indexValue = indexValue

class Distance :
    def __init__(self,mac : str , distance : float):
        self.mac = mac
        self.distance = distance

class AccessPoint:
    def __init__(self, mac: str, loc: SimpleLocation = SimpleLocation(0, 0, 0), f: float = 2417000000, a: float = 5.0, p: float = 20.0):
        self.mac = mac
        self.mac_address = mac
        self.location = loc
        self.output_power_dbm = p
        self.antenna_dbi = a
        self.output_frequency_hz = f

    def set_fbcm_index(self, index : float):
        self.fbcm_index = index


class GNSS_systems:
    """
    caliration la formule de la distance -> calibration de la position
        -> récupérer des devices avec des positions connues ( data set )
            -> construit les indexs
        Un fingerprint ( composé de plusieurs RSSISample):
            ->
    """
    def __init__(self, list_ap : list[AccessPoint] , fgp_dbRef : FingerprintDatabase):
        self.list_ap = list_ap
        self.fgp_dbRef = fgp_dbRef
        self.set_FBCM_ap_list()
    
        
    def get_database_calibrate(self,fgp_dbTest : FingerprintDatabase)-> FingerprintDatabase:
        fgp_dbCalibrate = FingerprintDatabase()
        for fingerprint in fgp_dbTest:
            distances_to_ap = []
            for rssi in fingerprint.sample.samples:
                for ap in self.list_ap:
                    if rssi.mac_address == ap.mac_address:
                        distance = self.estimate_distance(rssi.get_average_rssi(),ap.fbcm_index,ap)
                        distances_to_ap.append(Distance(rssi.mac_adresse,distance))
            pos_calibrate = self.multilateration(distances_to_ap,self.list_ap)
            fgp_dbCalibrate.db.append(Fingerprint(pos_calibrate,fingerprint.sample))

        return fgp_dbCalibrate

    def set_FBCM_ap_list(self):
        for ap in self.list_ap:
            ap_list_fbcm = [] 
            for fingerprint in self.fgp_dbRef:
                distance = fingerprint.position.distance(ap.location)
                index = 0
                for rssi in fingerprint.sample.samples:
                    # à voir pour le if
                    if rssi.mac_address == ap.mac_address :
                        index = self.compute_FBCM_index(distance,rssi,ap)
                        break
                # soit ajout un index qui correspond à une localisation
                # soit on fait la moyenne
                if index != 0 :
                    ap_list_fbcm.append(IndexFBCM(index))
            #retourner list des index ou directmeent la moyenne de cette liste
            ap.set_fbcm_index(sum(ap_list_fbcm)/len(ap_list_fbcm))

    def compute_FBCM_index(self,distance: float, rssi_values: RSSISample, ap: AccessPoint) -> float:
        """
        Function compute_*FBCM_index computes a FBCM index based on the distance (between transmitter and receiver)
        and the AP parameters. We consider the mobile device's antenna gain is 2.1 dBi.
        :param distance: the distance between AP and device
        :param rssi_values: the RSSI values associated to the AP for current calibration point. Use their average value.
        :return: one value for the FBCM index
        """
        GR = 2.1
        GT = ap.antenna_dbi
        PR = rssi_values.get_average_rssi()
        PT = ap.output_power_dbm
        c = 299792458
        l = c/ap.output_frequency_hz
        l4pi = pow((l/(4*pi)), 2)
        distance = abs(distance)

        if distance == 0:
            distance = 0.00001

        index = (PT-PR+GT+GR+20*log10(l/(4*pi), 10)) / (10*log10(distance))
        return index
    
    def estimate_distance(self,rssi_avg: float, fbcm_index: float, ap: AccessPoint) -> float:
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
    
    def multilateration(self,distances: list[Distance], ap_locations: list[AccessPoint]) -> SimpleLocation:
        """
        Function multilateration computes a location based on its distances towards at least 3 access points
        :param distances: the distances associated to the related AP MAC addresses as a string
        :param ap_locations: the access points locations, indexed by AP MAC address as strings
        :return: a location
        """
        precision = 0.1
        maximum_dist = max(distances)+1

        minDist = 999999
        best_position = SimpleLocation(0,0,0)
        min_x = int(min([loc.x for loc in ap_locations]) - maximum_dist)
        min_y = int(min([loc.y for loc in ap_locations]) - maximum_dist)
        min_z = int(min([loc.z for loc in ap_locations]) - maximum_dist)

        max_x = int(max([loc.x for loc in ap_locations]) + maximum_dist)
        max_y = int(max([loc.y for loc in ap_locations]) + maximum_dist)
        max_z = int(max([loc.z for loc in ap_locations]) + maximum_dist)

        #à voir pour utiliser la méthode corentin 

        for x in range(min_x*precision ,max_x*precision):
            for y in range(min_y*precision,max_y*precision):
                for z in range(min_z*precision,max_z*precision):
                    current_position = SimpleLocation(x,y,z)
                    sum = 0
                    for dist in distances:
                        for ap in ap_locations:
                            if dist.mac == ap.mac :
                                sum += abs(current_position.distance(ap.location) - dist.distance)
                                break
                    if sum <= minDist:
                        minDist = sum
                        best_position = current_position

        return best_position