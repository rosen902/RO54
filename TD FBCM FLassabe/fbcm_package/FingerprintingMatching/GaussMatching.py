from fbcm_package.CSVParser import CSVParser
from fbcm_package.Location import Location
from fbcm_package.Fingerprint import Fingerprint, Fingerprint_header
from fbcm_package.RSSISample import RSSISample
from fbcm_package.FingerprintingMatching.HistoMatching_v2 import Fingerprint_normed_2, RSSISample_normed_2, probability_2

from math import pow, sqrt, floor, pi, exp
import string

class RSSISample_gaussed(RSSISample):
    """RSSISample_gaussed
    RSSISample_gaussed is an version of RSSISample that is used to handle gaussian values for calculation
    """

    def __init__(self, mac_address :string, avg: float, stddev: float):
        """Constructor
        Construct the object, and set the average and standard deviation
        mac_address : mac address of the AP
        avg : average rssi
        stddev : standard deviation
        """

        super().__init__(mac_address)
        self._average_rssi = avg
        self._standard_deviation = stddev
        
    def __repr__(self) -> str:
        ret = 'macAddress : '
        ret += str(self.mac_address)
        ret += ', average_rssi : '
        ret += str(self._average_rssi)
        ret += ', standard_deviation : '
        ret += str(self._standard_deviation)
        return ret

class Fingerprint_gaussed(Fingerprint_header):
    """Fingerprint_gaussed
    Fingerprint_gaussed is an version of Fingerprint that is used to handle gaussian calculation using RSSISample_gaussed
    """

    def __init__(self, fingerprint: Fingerprint) -> None:
        """Constructor
        This class is an implementation of fingerprint that handle gaussian matching. 
        It use basic Fingerprint to construct itself
        """
        super().__init__(fingerprint.location)

        # go throuth rssiSample database
        for RSSISample_n in fingerprint._RSSISample_list:
            
            # compute the average value
            average_rssi = RSSISample_n.get_average_rssi()
            
            # check if sample is not empty
            if average_rssi == -1:continue

            # compute the standard deviation
            sum = 0.0; N=0
            for rssi in RSSISample_n._signal_list:
                sum += pow(rssi - average_rssi, 2)
                N += 1
            standard_deviation = sqrt(sum / N)

            # create the instance of rssi sample gaussed
            new_rssi_sample_gaussed = RSSISample_gaussed(RSSISample_n.mac_address, average_rssi, standard_deviation)

            self._RSSISample_list.append(new_rssi_sample_gaussed)

def gauss_to_histogram(fingerprint: Fingerprint_gaussed) -> Fingerprint_normed_2:
    """gauss_to_histogram
    This method convert a fingerprint in gauss form to a fingerprint in histogram form in order to use it with histogram matching method
    """
    # create the instance of fingerprint_normed_2 (empty)
    FPtemp = Fingerprint(fingerprint.location)
    newfingerprint = Fingerprint_normed_2(FPtemp)

    # go throuth rssiSample database
    for RSSISample_n in fingerprint._RSSISample_list:
        
        # create the instance of rssi sample with the same mac address
        new_rssi_sample_n = RSSISample_normed_2(RSSISample_n.mac_address)

        # retrieve the average value and the standard deviation
        sig = RSSISample_n._standard_deviation
        mu = RSSISample_n._average_rssi
        
        # set the bounds of the histogram
        min_dBm = floor(RSSISample_n._average_rssi)-10
        max_dBm = floor(RSSISample_n._average_rssi)+10
        
        

        # compute the histogram from min_dBm to max_dBm
        for x in range(min_dBm,max_dBm):

            if sig == 0:
                # avoid dividing by zero situation (list with only one element)
                proba_gaussed = 0
            else:
                # compute the gaussian value
                proba_gaussed = 1/(sig * sqrt(2*pi)) * exp(- ((x - mu)*(x - mu))/(2*sig*sig))

            # add the gaussian value to the histogram using fake function. This function doesn't check the unity of the set
            new_rssi_sample_n.add_fake(x, proba_gaussed)

        # add the new rssi sample to the new fingerprint
        newfingerprint._RSSISample_list.append(new_rssi_sample_n)
    return newfingerprint


def gauss_matching(db: CSVParser, sample: Fingerprint_gaussed) -> Location:
    """gauss_matching
    This method is used to match a fingerprint in gauss form to the database
    """

    max_probability = 0
    max_probability_location = Location(0,0,0)
    sample_gaussed = gauss_to_histogram(sample)

    # go throuth the database
    for fingerprint_n in db.fingerprint_list:

        # convert the fingerprint in gauss form to histogram form
        fingerprint_gaussed = gauss_to_histogram(Fingerprint_gaussed(fingerprint_n))

        # compute the probability of the two fingerprints to be the same
        proba = probability_2(fingerprint_gaussed, sample_gaussed)

        # check if the probability is higher than the previous one
        if proba >= max_probability:
            max_probability = proba
            max_probability_location = fingerprint_n.location

    return max_probability_location