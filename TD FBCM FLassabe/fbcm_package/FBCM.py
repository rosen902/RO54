from fbcm_package.AccessPoint import AccessPoint
from fbcm_package.Tools import dB_to_lin
from fbcm_package.Location import Location, evaluateDistance
from math import pi, log, log10
from fbcm_package.RSSISample import RSSISample

class FBCM:
    """Friis-Based Calibrated Model class 
    this class is used to handle localisation based on friis index as descibed in the paper.
    It process in two steps:
        1st - Calibration time using well knowned datas
        2nd - Localization using computed indexes
    """
    def __init__(self, AP_list, fingerprint_list) -> None:
        """Constructor
            AP_list : list of AP present
            fingerprint_list : list of fingerprint to calibrate
        Construct the object, and calibrate the model for the given dataset and access points
        the list of fingerprint is used only for calibration and is dump after
        """
        # list of Access points
        self._AP_list = AP_list

        # list of fingerprint (used only for calibration)
        self._fbcm_index = []

        # run through the Access point list
        for AP_n in self._AP_list:

            # temporary list of indexes
            AP_fbcm_index = []

            # run through the fingerprint list
            for fingerprint_n in fingerprint_list:

                # evaluate the real distance between the fingerprint and the AP
                distance = evaluateDistance(fingerprint_n.location, AP_n.location)

                # run through the RSSI Sample list
                for rssiSample in fingerprint_n._RSSISample_list:
                    
                    #look for RSSI Samples that concern the AP (corresponding mac address)
                    if rssiSample.mac_address == AP_n.mac_address:
                        # compute index with this sample and knowing the distance. 
                        # I firstly tried to filter long distances when rssi is hign
                        if rssiSample.get_average_rssi() > -80:
                            AP_POS_fbcm_index = _compute_FBCM_index(distance, rssiSample, AP_n)
                            break

                # adding index to the list
                # I choose to filter indexes between 3 and 3.5
                if AP_POS_fbcm_index > 2 and AP_POS_fbcm_index < 3.5:
                    AP_fbcm_index.append(AP_POS_fbcm_index)
            
            # averaging indexes
            self._fbcm_index.append(sum(AP_fbcm_index)/len(AP_fbcm_index))

    def evaluate(self, RSSISample_to_evaluate, invp: int = 1) -> Location:
        """evaluate
        this methode evaluate a RSSI sample with the calibrated model
            RSSISample_to_evaluate : RSSISample to evaluate
            invp is the precision for multilateration (1/precision)
        """
        # list of distances with each access points
        distances = []


        # run through the AP list
        for j in range(0,len(self._AP_list)):
            #list of distances computed for one AP
            dist_for_AP = []

            # run through the list of RSSI values
            for i in range(0,len(RSSISample_to_evaluate)):
                
                #search for RSSI value that correspond to the AP
                if RSSISample_to_evaluate[i].mac_address == self._AP_list[j].mac_address:

                    # estimate the distance using Friis index
                    dist = _estimate_distance(RSSISample_to_evaluate[i].get_average_rssi(), self._fbcm_index[j], self._AP_list[j])

                    # append to the list of distances
                    dist_for_AP.append(dist)
                    break
            
            # if list not empty, add the mean value of the list
            if (len(dist_for_AP) != 0):
                distances.append(sum(dist_for_AP)/len(dist_for_AP))
            else:
                # otherwise return -1 for error
                distances.append(-1)
        
        # extracts locations of APs
        locations_list = [access_point.location for access_point in self._AP_list]
        
        # search for the location of the sample giving AP location and estimated distances with them
        pos = _multilateration(distances,locations_list , invp)
        return pos


def _compute_FBCM_index(distance: float, rssi: RSSISample, ap: AccessPoint) -> float:
    """_compute_FBCM_index
    this methode compute the FBCM index for a rssi, an access point and a knowned distance
        distance : distance between the fingerprint and the access point
        rssi : RSSISample to evaluate
        ap : AccessPoint to evaluate
    """
    GR = (2.1)
    GT = (ap.antenna_dbi)
    PR = (rssi.get_average_rssi())
    PT = (ap.output_power_dbm)
    c = 299792458 
    l = c/ap.output_frequency_hz
    l4pi = (l/(4 * pi)) ** 2
    
    # check if distance is non null; if it is, the distance is a bit shifted to avoid division by zero
    if distance <= 0:
        print("error distance <= 0 : [" + str(distance) + "], value rounded to 0.0001")
        distance = 0.0001

    # I tried multiples version of the formula, using dB or linear version. Only the last one looks to work properly
    #friss_index = log((PT/PR) * GT * GR * l4pi, distance)
    #friss_index = -log((1/l4pi) * log10(PR-PT-GT-GR), 10)
    friss_index = (PT-PR+GT+GR+20*log(l/(4*pi), 10)) / (10*log(distance))
    return friss_index
    
def _estimate_distance(rssi_avg: float, fbcm_index: float, ap: AccessPoint) -> float:
    """_estimate_distance
    this methode estimate the distance of a rssi to an access point. It use the previously calculated index of this ap for that purpose
        rssi_avg : average value of the rssi sample
        fbcm_index : previously calculated index
        ap : access point to evaluate
    """
    GR = (2.1)
    GT = (ap.antenna_dbi)
    PR = (rssi_avg)
    PT = (ap.output_power_dbm)
    c = 299792458
    l = c/ap.output_frequency_hz
    l4pi = (l/(4 * pi)) ** 2
    
    # I tried multiples version of the formula, using dB or linear version. Only the last one looks to work properly
    #estimated_distance = pow((PT/PR) * GT * GR * l4pi, 1/fbcm_index)
    #estimated_distance = pow((1/l4pi) * log10(PR-PT-GT-GR), -1/fbcm_index)
    estimated_distance = pow(10, (PT-PR+GT+GR+20*log(l/(4*pi)))/(10*fbcm_index))
    return estimated_distance

#TODO: improve this function
def _multilateration(distances, ap_locations, invp: int = 10) -> Location:
    """_multilateration
    this methode return a location that is not that far from each 
        distances : list of distances between the sample and each access point
        ap_locations : list of locations of each access point
    """
    # get the maximum distance of each AP in order to draw the rectangle of possibilities
    maxd = max(distances) + 1

    # compute the min, max edges on each coordinates.
    minx = int(min([loc.x for loc in ap_locations]) - maxd)
    miny = int(min([loc.y for loc in ap_locations]) - maxd)
    minz = int(min([loc.z for loc in ap_locations]) - maxd)

    maxx = int(max([loc.x for loc in ap_locations]) + maxd)
    maxy = int(max([loc.y for loc in ap_locations]) + maxd)
    maxz = int(max([loc.z for loc in ap_locations]) + maxd)

    # get the precision
    precision = 1/invp

    # number of APs
    N = len(distances)
    # set initial minium distance (big one)
    minDist = 10000000000000000
    # set initial min location
    minPos = Location(0,0,0)

    # run through x, y, z range in order to evaluate the best location
    for xint in range(minx *invp, maxx *invp):
        x = xint * precision
        for yint in range(miny *invp, maxy *invp):
            y = yint * precision
            for zint in range(minz *invp, maxz *invp):
                z = zint * precision

                # location to evaluate
                p = Location(x, y, z)
                sum = 0
                for i in range(0,N):
                    # sum up the distances of the location with each range of each AP given the estimated distance
                    # -1 mean that the distance failled be computed
                    if (distances[i] != -1):
                        sum += abs(evaluateDistance(p, ap_locations[i]) - distances[i])
                
                # store the position if the sum is the lowest
                if sum<minDist:
                    minDist = sum
                    minPos = p
    return minPos