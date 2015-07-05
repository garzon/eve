import SolarSystemArray

class SolarSystem:
	def __init__(self, sysID):
		self.__model = SolarSystemArray.all().__map[sysID]
		self.sysID = self.__model.gid
		self.name = self.__model.name
		self.security = self.__model.security

	def isSafe(self):
		return round(self.security) >= 0.5

	def is00(self):
		return round(self.security) <= 0

	def isNotSoSafe(self):
		return not self.is00() and not self.isSafe()

	def getNeighborInJumps(self, distance = 1, searched = set()):
		searched.add(self.sysID)
		if distance != 0:
			toGo = self.__model.neighbor.difference(searched)
			while True:
				if len(toGo) == 0: break
				aim = toGo.pop()
				sys = SolarSystem(aim)
				searched = sys.getNeighborInJumps(distance-1, searched)
				toGo = toGo.difference(searched)
		return searched
