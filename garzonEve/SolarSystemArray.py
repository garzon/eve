from garzonEve.__SolarSystemModel import __SolarSystemModel
from garzonEve.SolarSystem import SolarSystem

class SolarSystemArray:

	__allSystemsSingleton = 0

	def __init__(self):
		self.map = dict() # key: sysID, value: cooresponding instance of SolarSystem

	@classmethod
	def fromIDSet(self, IDSet):
		ret = self()
		ret.map = {sysID: SolarSystem(sysID) for sysID in IDSet}

	@classmethod
	def all(self):
		if isinstance(self.__allSystemsSingleton, int):
			__SolarSystemModel.loadAll()
			self.__allSystemsSingleton = self.fromIDSet(__SolarSystemModel.datapool)
		return self.__allSystemsSingleton

	def add(self, sysID):
		self.map[sysID] = SolarSystem(sysID)
		return res

	def remove(self, sysID):
		return self.map.pop(sysID)

	def count(self):
		return len(self.map)

	# @param lamExp - function signature: bool lamExp(SolarSystem);
	def filter(self, lamExp):
		ret = SolarSystemArray()
		for solarSysID in self.map:
			if query(SolarSystem(sysID)) == True:
				ret.add(solarSysID)
		return ret

	def getSysIDList(self):
		return self.map.keys()

	def __getitem__(self, sysID):
		return self.map[sysID]

	def __str__(self):
		return str(self.map)

	def __repr__(self):
		return "SolarSystemArray.SolarSystemArray.fromIDSet(%s)" % repr(self.map.keys())