from fbcm_package.CSVParser import CSVParser
from fbcm_package.Location import Location
from fbcm_package.Fingerprint import Fingerprint, Fingerprint_header
from fbcm_package.RSSISample import RSSISample
import string

""" /!\
This python programm comes from in a misinterpretation of the subject
Since it gives prety accurate localisation, I decided to keep it.
It use an histogramme build with each mac address, and not one histogramm per mac address
"""

class RSSISample_normed(RSSISample):
    """RSSISample_normed
    RSSI sample that also store a coef value.
    this value should not be modified by hands and is calculated ones by Fingerprint_normed class.
    RSSI sample is used to store rssi values for one MAC address
    """
    def __init__(self, mac_address :string, probability: float):
        """Constructor

        """
        super().__init__(mac_address)
        self._probability = probability

class Fingerprint_normed(Fingerprint_header):
    """Fingerprint_normed
    This class is an implementation of fingerprint that handle histogram matching. 
    It use basic Fingerprint to construct itself
    """
    def __init__(self, fingerprint: Fingerprint) -> None:
        """Constructor
        Create an instance of fingerprint using a basic fingerprint that is converted to be used as normed fingerprint
        This implementation of fingerprint is based on the "Fingerprint" version, since datas are extracted from the database in this form
        """
        super().__init__(fingerprint.location)
        total_sum = 0
        
        # compute the sum of all rssi values (averages) in the fingerprint
        for RSSISample_n in fingerprint._RSSISample_list:
            total_sum += RSSISample_n.get_average_rssi()
        
        # convert rssi sample to rssi sample normed and store it in the instance 
        for RSSISample_n in fingerprint._RSSISample_list:
            proba = RSSISample_n.get_average_rssi() / total_sum
            newRSSISample_normed = RSSISample_normed(RSSISample_n.mac_address, proba)
            self._RSSISample_list.append(newRSSISample_normed)
    
def probability(histo1: Fingerprint_normed, histo2: Fingerprint_normed) -> float:
    """probability
    This methode return the probability that two fingerprints corresponds to the same location.
    it basically a sum of minimal coef for each pair of rssi sample with the same mac address
    """

    # sum of coef in common
    distance = 0.0

    # go throw rssi sample lists to find matching
    for rssi_sample_1_n in histo1._RSSISample_list:
        for rssi_sample_2_n in histo2._RSSISample_list:
            if rssi_sample_1_n.mac_address == rssi_sample_2_n.mac_address:

                # take the smalled probability of them
                add = min(rssi_sample_1_n._probability, rssi_sample_2_n._probability)

                # sum up coefs in common
                distance += add
                break
    
    return distance

def histogram_matching(db: CSVParser, sample: Fingerprint_normed) -> Location:
    """histogram_matching
    iterate over the database to find the best matching location
    """
    max_probability = 0
    max_probability_location = Location(0,0,0)
    for fingerprint_n in db.fingerprint_list:
        
        # compute the probability of the current fingerprint
        proba = probability(Fingerprint_normed(fingerprint_n), sample)
        if proba >= max_probability:
            max_probability = proba
            max_probability_location = fingerprint_n.location
    
    return max_probability_location
