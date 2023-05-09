from fbcm_package.Location import Location

class AccessPoint:
    """AccessPoint class
    Structure that handle access point's related informations.
    """
    def __init__(self, mac_address: str, loc:Location, p:float=20.0, a:float=5.0, f:float=2417000000) -> None:
        """Constructor
        Initialise the structure giving at least the adress and the location of the access point.
        """
        self.mac_address = mac_address
        self.location = loc
        self.output_power_dbm = p
        self.antenna_dbi = a
        self.output_frequency_hz = f

    def __str__(self) -> str:
        return '(MAC:' + str(self.mac_address) + ', Loc:' + str(self.location)