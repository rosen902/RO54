from fbcm_package.CSVParser import CSVParser
from fbcm_package.Location import Location
from fbcm_package.Fingerprint import Fingerprint, Fingerprint_header
from fbcm_package.RSSISample import RSSISample
import string

"""
This python programm is the real histogram matching and should not be confused with the _v1 version
"""

class RSSISample_normed_2(RSSISample):
    """RSSISample_normed_2
    RSSISample used to store rssi values for one MAC adress
    """

    def __init__(self, mac_address :string):
        """Constructor
    
        """

        super().__init__(mac_address)
        # sum of all rssis stored in _signal_list
        self.sum = 0

        # if probas already been computed or not
        self._proba_computed = True

        # list of probabilities of each values stored in parallel in the next attribute
        self._signal_list_proba = []
        
        # list of UNIQUE rssi values; should not be confused with _signal_list stored in the parent class
        self._signal_list_val = []

    def add(self, rssi: float) -> None:
        """add methode
        used to add a new rssi value in the list
        """

        super().add(rssi)
        self.sum += 1
        self._proba_computed = False

    def add_fake(self, rssi: float, proba: float) -> None:
        """add_fake
        this methode is used by gaussian class to convert itself into normed one. Hazardous to use, please don't.
        """

        self._signal_list_proba.append(proba)
        self._signal_list_val.append(rssi)
        self._proba_computed = True
        
    def get_proba(self, rssi: float) -> float:
        """get_proba
        return the probability of one rssivalue. Sum of all probas are always equal to 1
        """

        # check if empty list
        if self.sum == 0: print("error empty rssi"); return 0
        
        # check if probabilities should be computed
        if not self._proba_computed:

            # clear the list in case of non empty situation (recalculation)
            self._signal_list_proba.clear()

            #set counter list (temporary var)
            signal_list_counter = []

            # run through the signal list of elements
            for rssi_n in self._signal_list:

                # check if the rssi value already been encountered
                for i in range(len(self._signal_list_val)):
                    if self._signal_list_val[i] == rssi_n:

                        # if yes increment his counter in the counter list
                        signal_list_counter[i] += 1
                        break
                else:
                    # otherwise add a new line to the list
                    self._signal_list_val.append(rssi_n)
                    signal_list_counter.append(1)

            # once all values have been sorted, compute the probabilities for each of them
            for i in range(len(signal_list_counter)):
                self._signal_list_proba.append(signal_list_counter[i]/self.sum)

            # set the flag to True, so this Sample will not be re computed again.
            self._proba_computed = True
        
        # look in the table for the requested rssi value and return its probability, or 0 if not founded
        for i in range(len(self._signal_list_val)):
            if self._signal_list_val[i] == rssi:
                return self._signal_list_proba[i]
        else:
            return 0

    def __repr__(self) -> str:
        ret = super().__repr__()
        ret += ', val_list :('
        for sig in self._signal_list_val:
            ret = ret + str(sig) + ", "
        ret = ret + ')\n'
        ret += ', proba_list :('
        for sig in self._signal_list_proba:
            ret = ret + str(sig) + ", "
        ret = ret + ')\n'
        return ret

class Fingerprint_normed_2(Fingerprint_header):
    """Fingerprint_normed_2
    Fingerprint class used to store RSSISample with a probability associated to each of them (for histogram matching)
    """

    def __init__(self, fingerprint: Fingerprint) -> None:
        """Constructor
        Create an instance of fingerprint using a basic fingerprint that is converted to be used as normed_v2 fingerprint
        This implementation of fingerprint is based on the "Fingerprint" version, since datas are extracted from the database in this form
        """
        # call super constructor
        super().__init__(fingerprint.location)
        
        # go through all rssi samples in the fingerprint to extract usefull datas used to create the Fingerprint normed
        for RSSISample_n in fingerprint._RSSISample_list:

            # create an instance of RSSISample_normed_2
            newRSSISample_normed = RSSISample_normed_2(RSSISample_n.mac_address)

            # add each rssi values to this isntance
            for RSSI_val in RSSISample_n._signal_list:
                newRSSISample_normed.add(RSSI_val)
            
            self._RSSISample_list.append(newRSSISample_normed)

    def __repr__(self) -> str:
        ret = super().__repr__()

        return ret
    
def probability_2(histo1: Fingerprint_normed_2, histo2: Fingerprint_normed_2) -> float:
    """probability_2
    This methode return the probability that two fingerprints corresponds to the same location.
    It compare the probabilities of each pair of rssi sample with the same mac address to be the same
    """

    distance = 0.0
    # for each rssi sample in the first fingerprint
    for rssi_sample_1_n in histo1._RSSISample_list:

        # for each rssi sample in the second fingerprint
        for rssi_sample_2_n in histo2._RSSISample_list:

            # if the mac address of the two rssi sample are the same
            if rssi_sample_1_n.mac_address == rssi_sample_2_n.mac_address:

                # add all minimum distance between the two rssi sample
                for RSSI_val in rssi_sample_1_n._signal_list:
                    add = min(rssi_sample_1_n.get_proba(RSSI_val), rssi_sample_2_n.get_proba(RSSI_val))
                    distance += add
                break
    
    return distance

def histogram_matching_2(db: CSVParser, sample: Fingerprint_normed_2) -> Location:
    """histogram_matching_2
    iterate over the database to find the best matching location
    """
    
    max_probability = 0
    max_probability_location = Location(0,0,0)
    
    # for each fingerprint in the database
    for fingerprint_n in db.fingerprint_list:

        # compute the probability of the two fingerprint
        proba = probability_2(Fingerprint_normed_2(fingerprint_n), sample)

        # if the probability is better than the previous one
        if proba >= max_probability:
            max_probability = proba
            max_probability_location = fingerprint_n.location
    
    return max_probability_location
