import csv
import string
from fbcm_package.Fingerprint import Fingerprint
from fbcm_package.Location import Location

class CSVParser:
	"""CSVParser
	Class designated to load RSSI datas from CSV files matching a specific format.
	Each datas are then stored in their corresponding object and stored in a list.
	"""

	def __init__(self, file: string):
		"""Constructor
		Create an instance of the class that extract datas from the given file and store it into internal attribute (public)
		"""
		self.fingerprint_list:Fingerprint = []

		# try to open the document
		with open(file, newline='') as csvfile:
			# open csv reader
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

			# for each rows in the file
			for row in spamreader:
    			
				# extract each x,y,z coordinates of the fingerprint
				x = row[0]
				y = row[1]
				z = row[2]

				# create location instance to store datas
				location = Location(x, y, z)

				# dismiss orientation, we don't use it
				orientation = row[3]

				# check if this location already exist in the database (meaning there is multiples definition of a fingerprint)
				for fingerprint_n in self.fingerprint_list:
					if fingerprint_n.location == location:
    					# redondency detected, fingerprints are merged

    					# datas are red 2 by 2, since each rssi value is preceded by the corresponding MAC address	
						# for each pair of mac address + rssi measurement
						for i in range(4,len(row),2):

							# max address is retrieved
							mac_address = row[i]

							# rssi value is retrieved
							signal = float(row[i+1])

							# rssi signal for that mac adress is stored
							fingerprint_n.add(signal, mac_address)
						# redondency founded, break the search loop
						break
				else:
    				# no redondency founded
					# creating new instance of fingerprint
					new_fingerprint = Fingerprint(location)
    				
					# datas are red 2 by 2, since each rssi value is preceded by the corresponding MAC address	
					# for each pair of mac address + rssi measurement
					for i in range(4,len(row),2):
    						
    					# max address is retrieved
						mac_address = row[i]
						
						# rssi value is retrieved
						signal = float(row[i+1])
						
						# rssi signal for that mac adress is stored
						new_fingerprint.add(signal, mac_address)
					
					#fingerprint is added to the database
					self.fingerprint_list.append(new_fingerprint)
	
	def __repr__(self) -> str:
		ret = ''
		for APs in self.fingerprint_list:
			ret = ret + str(APs) + ",\n"
		return ret