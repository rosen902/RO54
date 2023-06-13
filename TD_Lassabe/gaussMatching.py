from math import log10, pow, pi , sqrt, floor ,exp
from positionning import SimpleLocation, Fingerprint, FingerprintSample,FingerprintDatabase
from histoMatching import  NormHisto , FingerPrintNormalized


class GaussModel:
    def __init__(self,mac : str, avg: float, stddev: float):
        self.mac = mac
        self.average_rssi = avg
        self.standard_deviation = stddev

    def histogram_from_gauss(self) -> NormHisto:

        min_value = floor(self.average_rssi) -10
        max_value = floor(self.average_rssi) +10
        proba_list = []
        for rssi in range(min_value,max_value):
            proba = 1/(self.standard_deviation * sqrt(2*pi))*exp(-(rssi - self.average_rssi)**2 / (2 * self.standard_deviation**2))
            proba_list.append(proba)
        return NormHisto(self.mac,proba_list)

class FingerPrintGaussed:
    def __init__(self, fingerprint : Fingerprint):
        self.location = fingerprint.position
        self.gaussed_Sample_list = []
        #self.normalized_fingerprint = FingerPrintNormalized(fingerprint)

        for rssiSample in fingerprint.sample.samples:
            average_rssi = rssiSample.get_average_rssi()
            # calcul ecart type
            total = 0
            for rssi in rssiSample.rssi:
                total += pow(rssi - average_rssi,2)
            stddev = sqrt(total/len(rssiSample.rssi))
            self.gaussed_Sample_list.append(GaussModel(rssiSample.mac_address,average_rssi,stddev))

    def gauss_to_histogram(self) -> FingerPrintNormalized:
        histogramms_fingerprint = []
        for gauss_model in self.gaussed_Sample_list:
            histogramms_fingerprint.append(gauss_model.histogram_from_gauss())
        fgp_normalized = FingerPrintNormalized()
        fgp_normalized.set_histogram_from_gauss(self.location,histogramms_fingerprint)
        return fgp_normalized
    
def gauss_matching(database: FingerprintDatabase,sample : FingerPrintGaussed) -> SimpleLocation:
        max_proba = 0
        best_location = SimpleLocation(0,0,0)
        histo_gaussed_fgp = sample.gauss_to_histogram()
        for fingerprint in database.db:
            fgp_gaussed_normalized = FingerPrintGaussed(fingerprint).gauss_to_histogram()
            proba = 0.5
            for histo in histo_gaussed_fgp.list_histo:
                 for histo2 in fgp_gaussed_normalized.list_histo:
                      if histo.mac == histo2.mac:
                           proba += histo.probability(histo2)
            if proba >= max_proba:
                max_proba = proba
                best_location = fingerprint.location
        return best_location
