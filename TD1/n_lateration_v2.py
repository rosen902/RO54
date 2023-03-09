from math import sqrt, pow
import itertools
from sys import exit
import numpy as np

class Position:
    def __init__(self, coords : list):
        self.coords = coords

class Estimator(Position):
    def __init__(self, coords: list):
        super().__init__(coords)
    
    def distance_from_target(self, emettors_list : list):
        result = 0
        for emettor in emettors_list:
            norm = 0
            for i in range(len(self.coords)):
                norm = norm + pow(self.coords[i] - emettor.coords[i], 2)
            norm = sqrt(norm)
            result = result + abs(emettor.distance - norm)

        return result

class Emettor(Position):
    def __init__(self, coords: list, distance_from_target : float):
        super().__init__(coords)
        self.distance = distance_from_target

class Locator:
    def __init__(self):
        self.dimensions = None
        self.decimals = None
        self.emettors_list = []
        self.estimator = None
        self.fork_coord_one = None
        self.fork_coord_two = None
    
    def set_parameters(self):
        while type(self.dimensions) is not int:
            try:
                self.dimensions = int(input("\nHow many dimensions does your space have ?\n==> "))
            except KeyboardInterrupt:
                exit()
            except:
                pass
        print("It will therefore be necessary to define", self.dimensions + 1, "emettors...")

        while type(self.decimals) is not int or self.decimals < 0:
            try:
                self.decimals = int(input("\nHow many decimals do you want ?\n==> "))
            except KeyboardInterrupt:
                exit()
            except:
                pass
        print("The result will have", self.decimals ,"decimals.")

        for i in range(self.dimensions + 1):
            emettor_coords = []
            distance_from_target = None
            while len(emettor_coords) != (self.dimensions):
                try:
                    non_parsed_data = input("\nEnter the coordinates of the emettor number {}, separating them with the symbol \';\' \n==> ".format(i+1))
                    emettor_coords = [float(coord) for coord in non_parsed_data.split(";")]
                except KeyboardInterrupt:
                    exit()
                except:
                    pass

            while type(distance_from_target) is not float:
                try:
                    distance_from_target = float(input("\nHow far from the target is this emettor ?\n==> "))
                except KeyboardInterrupt:
                    exit()
                except:
                    pass
            self.emettors_list.append(Emettor(emettor_coords, distance_from_target))
        
        self.estimator = Estimator([0. for j in range(self.dimensions)])
        
        fork_coord_two_coords = []
        for i in range(self.dimensions):
            fork_coord_two_coords.append(max([ emettor.coords[i] for emettor in self.emettors_list]))

        self.fork_coord_two = Position(fork_coord_two_coords)
        self.fork_coord_one = Position(self.estimator.coords)


    def generate_space_of_points(self, pas : float):
        iterables = []
        for i in range(self.dimensions):
            round_vector = np.arange(self.fork_coord_one.coords[i], self.fork_coord_two.coords[i] + pas, pas)
            round_vector = [round(x,self.decimals+1) for x in round_vector]
            iterables.append(round_vector)
        for point in itertools.product(*iterables):
            yield point
    

    def approximation_step(self, pas: float):
        for point in self.generate_space_of_points(pas):
            current_point = Estimator(list(point))
            if current_point.distance_from_target(self.emettors_list) < self.estimator.distance_from_target(self.emettors_list):
                self.estimator = current_point
        self.fork_coord_two.coords = [round(x + pas, self.decimals+1) for x in self.estimator.coords]
        self.fork_coord_one.coords = [round(x - pas, self.decimals+1) for x in self.estimator.coords]



    def approximate(self):
        self.approximation_step(1)
        if self.decimals > 0:
            for i in range(1, self.decimals+2):
                self.approximation_step(1 / (10 ** abs(i)))

        self.estimator.coords = [round(x, self.decimals) for x in self.estimator.coords]
        print("La cible est situee aux coordonnees suivantes :",self.estimator.coords)



locator = Locator()
locator.set_parameters()
locator.approximate()
