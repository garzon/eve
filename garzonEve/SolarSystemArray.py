from _SolarSystemModel import _SolarSystemModel
from SolarSystem import SolarSystem

class SolarSystemArray:

	_allSystemsSingleton = 0

	def __init__(self):
		self.map = dict() # key: sysID, value: cooresponding instance of SolarSystem

	@classmethod
	def fromIDSet(self, IDSet):
		ret = self()
		ret.map = {sysID: SolarSystem(sysID) for sysID in IDSet}
		return ret

	@classmethod
	def all(self):
		if isinstance(self._allSystemsSingleton, int):
			_SolarSystemModel.loadAll()
			self._allSystemsSingleton = self.fromIDSet(_SolarSystemModel._datapool)
		return self._allSystemsSingleton

	def add(self, sysID):
		self.map[sysID] = SolarSystem(sysID)
		return self

	def remove(self, sysID):
		return self.map.pop(sysID)

	def count(self):
		return len(self.map)

	# @param lamExp - function signature: bool lamExp(SolarSystem);
	def filter(self, lamExp):
		ret = SolarSystemArray()
		for solarSysID in self.map:
			if lamExp(SolarSystem(solarSysID)) == True:
				ret.add(solarSysID)
		return ret

	def getSysIDList(self):
		return self.map.keys()

	def __getitem__(self, sysID):
		return self.map[sysID]

	def __str__(self):
		return '\n'.join([str(x) for x in self.map.values()])

	def __repr__(self):
		return "SolarSystemArray.SolarSystemArray.fromIDSet(%s)" % repr(self.map.keys())