from garzonEve.__SolarSystemModel import __SolarSystemModel 

class SolarSystem:

	@classmethod
	def loadAll(self):
		__SolarSystemModel.loadAll()

	def __init__(self, sysID):
		self.__model = __SolarSystemModel.fetch(sysID)

	def __getitem__(self, keyname):
		if not isinstance(keyname, str): raise "SolarSystem::__getitem__() error - the type of keyname must be str."
		if keyname == 'sysID':
			return self.__model.sysID
		elif keyname == 'name':
			return self.__model.name
		elif keyname == 'security':
			return self.__model.security
		elif keyname == 'jumpsNum':
			if self.__model.isLoaded == False:
				self.__model.load()
			return self.__model.jumpsNum
		raise "SolarSystem::__getitem__() error - keyname(%s) undefined" % keyname

	def isSafe(self):
		return round(self.__model.security) >= 0.5

	def is00(self):
		return round(self.__model.security) <= 0

	def isNotSoSafe(self):
		return not self.is00() and not self.isSafe()

	def getNeighborInJumps(self, distance = 1, searched = set()):
		searched.add(self.__model.sysID)
		if distance != 0:
			toGo = self.__model.neighbor.difference(searched)
			while True:
				if len(toGo) == 0: break
				aim = toGo.pop()
				sys = SolarSystem(aim)
				searched = sys.getNeighborInJumps(distance-1, searched)
				toGo = toGo.difference(searched)
		return searched

	def __str__(self):
		return str(self.__model)

	def __repr__(self):
		return "SolarSystem.SolarSystem(%d)" % self.__model.sysID