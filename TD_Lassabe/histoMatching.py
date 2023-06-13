from math import log10, pow, pi , sqrt, floor ,exp
from positionning import SimpleLocation, Fingerprint, FingerprintSample,FingerprintDatabase

class HistoValue:
    def __init__(self,rssiValue: int, countValue: int):
        self.rssi = rssiValue
        self.count = countValue
        self.prob = 0
    def addCount(self):
        self.count = self.count+1

    def set_prob(self,countMax):
        self.prob = self.count/countMax

class NormHisto :
    def __init__(self, mac: str, hist : list[HistoValue] ):
        self.histogram  = hist
        self.mac = mac

    def add(self, prob : HistoValue):
        self.histogram.append(prob)

    def probability(self,histo2):
        proba = 0
        for hist_value_1 in self.histogram:
            for hist_value_2 in histo2.histogram:
                if hist_value_1.rssi == hist_value_2.rssi:
                    proba += min(hist_value_1.prob,hist_value_2.prob)
                    break
                  
        return proba

    

class FingerPrintNormalized:
    def __init__(self):
        self.position = SimpleLocation(0,0,0)
        self.list_histo = None

    def is_RSSI_value_known(normalizedSample : list[HistoValue],rssi):
        if len(normalizedSample) == 0:
            return False, None
        else :
            for index, histoValue in enumerate(normalizedSample):
                if histoValue.rssi == rssi:
                    return True, index
            return False, None
        
    def set_histogram(self,fingerprint : Fingerprint):
        self.position = fingerprint.position
        count_max = 0
        for rssi_list in fingerprint.sample.samples:
            histoValues = []
            count_max = len(rssi_list.rssi)
            for rssi_value in rssi_list.rssi:
                is_known, indexHistoValue =  self.is_RSSI_value_known(histoValues,rssi_value)
                if not is_known:
                    histoValues.append(HistoValue(rssi_value,1))
                else :
                    histoValues[indexHistoValue].addCount()

            for value in histoValues:
                value.set_prob(count_max)
            self.list_histo.append(NormHisto(rssi_list.mac_address,histoValues))

    def get_proba_histos(self,fgp_normalized):
        proba_histo = 0
        for histo in self.list_histo:
            for histo2 in fgp_normalized.list_histo:
                if histo.mac == histo2.mac:
                    proba_histo += histo.probability(histo2)
                    break
        return proba_histo
    
    def set_histogram_from_gauss(self,position : SimpleLocation, list_histo : list[NormHisto]):
        self.position = position
        self.list_histo = list_histo


def histogram_matching(database : FingerprintDatabase, sample_histo : FingerPrintNormalized) -> SimpleLocation:
        max_proba = 0
        best_location = SimpleLocation(0,0,0)
        for fingerprint in database.db:
            histoFingerprint = FingerPrintNormalized()
            histoFingerprint.set_histogram(fingerprint)
            proba = sample_histo.get_proba_histos(histoFingerprint)
            if proba > max_proba:
                max_proba = proba
                best_location = fingerprint.location
        return best_location