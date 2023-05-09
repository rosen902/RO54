from fbcm_package.CSVParser import CSVParser
from fbcm_package.Location import Location
from fbcm_package.Fingerprint import Fingerprint

#constant; maximum |RSSI| taked into account
MAXDISTANCE = 80

def rssi_distance(rssi_sample_list_1, rssi_sample_list_2) -> float:
    """rssi_distance
    this function evaluate the "distance" between two rssi readings
    """

    # number of mac address in common
    N = 0

    # total sum of difference
    distance = 0.0 

    # run through each rssi list to find identical mac address rssi sample
    for rssi_sample_1_n in rssi_sample_list_1:
        for rssi_sample_2_n in rssi_sample_list_2:
            if rssi_sample_1_n.mac_address == rssi_sample_2_n.mac_address:

                # compute the difference between both to the global sum
                add = abs(rssi_sample_1_n.get_average_rssi() - rssi_sample_2_n.get_average_rssi())

                # if the difference is too big, it is truncated
                if add > MAXDISTANCE:
                    print("max_dist: " + str(add))
                    add = MAXDISTANCE

                # difference added to the distance
                distance += add

                # counter of in common incremented
                N += 1
                break
    
    # number of not in common mac address value between rssi sample lists 
    not_in_common = len(rssi_sample_list_1) + len(rssi_sample_list_2) - 2*N

    # each not in common count for one MAXDISTANCE. Added to the total sum
    distance += not_in_common * MAXDISTANCE

    return distance
    
def simple_matching(db: CSVParser, sample: Fingerprint) -> Location:
    """simple_matching
    return the location of the fingerprint with the nearest RSSI values
    """
    min_dist = 100000000000000000000000 #un grand nombre
    min_location = Location(0,0,0)

    # run through fingerprint list
    for fingerprint_n in db.fingerprint_list:
        
        # compute distance
        dist = rssi_distance(fingerprint_n._RSSISample_list, sample._RSSISample_list)

        # store the closest one
        if dist <= min_dist:
            min_dist = dist
            min_location = fingerprint_n.location
    
    return min_location

