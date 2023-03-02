from math import sqrt, pow

class Position:
    def __init__(self, *args : float):
        self.coord_array = []
        for coordinate in args:
            self.coord_array.append(coordinate)

class Emettor:
    def __init__(self, distance_from_target : float, *args:
        self.distance_from_target = distance_from_target
        self.position = Position(args)

class Locator:
    def __init__(self):
        self.dimensions = None
        self.decimals = None
        self.estimator = None
        self.dmin = None
        self.emettors_list = []
    
    def distance_from_estimator(self, position : Position):
        try:


    
    def set_parameters(self):
        while type(self.dimensions) is not int:
            try:
                self.dimensions = int(input("\nHow many dimensions does your space have ?\n==> "))
            except:
                pass
        print("It will therefore be necessary to define", self.dimensions + 1, "emettors...")

        while type(self.decimals) is not int:
            try:
                self.decimals = int(input("\nHow many decimals do you want ?\n==> "))
            except:
                pass

local = Locator()