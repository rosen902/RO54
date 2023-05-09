from math import sqrt, pow

class Location:
	"""Location
	structure containing coordinates in carthesian form
	"""
	def __init__(self, x: float, y: float, z: float) -> None:
		"""Constructor
		
		"""
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)

	def __eq__(self, other):
		if self.x == other.x and self.y == other.y and self.z == other.z:
			return True
		else:
			return False

	def __str__(self) -> str:
		return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) +')'

def evaluateDistance(p1:Location, p2:Location) -> float:
	"""evaluateDistance
	compute the Euclidian distance between p1 and p2
	"""
	dist = sqrt(pow(p1.x-p2.x, 2) + pow(p1.y-p2.y, 2) + pow(p1.z-p2.z, 2))
	return dist
