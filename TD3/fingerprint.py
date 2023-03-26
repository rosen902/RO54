from math import pow


class Entity:
    def __init__(self, rssi):
        self.rssi = rssi

class Cellule(Entity):
    def __init__(self, rssi, x, y):
        super().__init__(rssi)
        self.coords = [x, y]
    
    def get_metric(self, rssi):
        return sum([abs(self.rssi[i] -  rssi[i]) for i in range(len(self.rssi))])
    

class Geolocator:
    def __init__(self, fp_database: list[Cellule], k: int, mobile_terminal : Entity):
        self.db = fp_database
        self.mobile_terminal = mobile_terminal
        self.k = k

        self.k_nearest_cells = None
        self.alphas = []
        self.coeffs = []
        
    
    def _find_nearest_cells(self):
        self.k_nearest_cells = sorted(cells, key=lambda cell: cell.get_metric(phone.rssi))[:self.k]

    def _find_alphas(self):
        for i in range(1,len(self.k_nearest_cells)):
            self.alphas.append(self.k_nearest_cells[i].get_metric(self.mobile_terminal.rssi) / self.k_nearest_cells[i-1].get_metric(self.mobile_terminal.rssi))

    def _find_coeffs(self):
        list_to_sum = [1.]
        for i in range(len(self.alphas)):
            list_to_sum.append(list_to_sum[i]/self.alphas[i])

        coeff1 = 1/sum(list_to_sum)
        self.coeffs.append(coeff1)

        for i in range(len(self.alphas)):
            self.coeffs.append(self.coeffs[i]/self.alphas[i])


    def find_coordinates(self, rounded: bool = False):
        self._find_nearest_cells()
        self._find_alphas()
        self._find_coeffs()
        
        x = 0
        y = 0
        for i in range(len(self.k_nearest_cells)):
            x += self.coeffs[i]*self.k_nearest_cells[i].coords[0]
            y += self.coeffs[i]*self.k_nearest_cells[i].coords[1]
        
        if rounded == True:
            print("The coordinates of the mobile terminal are :({};{})".format(round(x,2),round(y,2)))
        else:
            print("The coordinates of the mobile terminal are :({};{})".format(x,y))
        


cells = [Cellule([-38,-27,-54,-13],2,2),
       Cellule([-74,-62,-48,-33],2,6),
       Cellule([-13,-28,-12,-40],2,10),
       Cellule([-34,-27,-38,-41],6,2),
       Cellule([-64,-48,-72,-35],6,6),
       Cellule([-45,-37,-20,-15],6,10),
       Cellule([-17,-50,-44,-33],10,2),
       Cellule([-27,-28,-32,-45],10,6),
       Cellule([-30,-20,-60,-40],10,10)]


phone = Entity([-26,-42,-13,-46])

geolocator = Geolocator(cells, 4, phone)
geolocator._find_nearest_cells()
geolocator._find_alphas()
geolocator._find_coeffs()
geolocator.find_coordinates(rounded=True)



