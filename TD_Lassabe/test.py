from math import log

def adapt_speed_green(distance , highlimit,lowlimit):

    distanceZone = highlimit - lowlimit
    distanceObsZone = distance -lowlimit
    coeff_distance = -distanceObsZone/distanceZone 
    speed = 5/(-(log(-coeff_distance+4))) + 6.1
    return speed


print(adapt_speed_green(4,5,3.5))