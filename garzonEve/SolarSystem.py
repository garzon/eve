from _SolarSystemModel import _SolarSystemModel 

class SolarSystem:

	@classmethod
	def loadAll(self):
		_SolarSystemModel.loadAll()

	def __init__(self, sysID):
		self._model = _SolarSystemModel.fetch(sysID)

	def __getitem__(self, keyname):
		if not isinstance(keyname, str): raise "SolarSystem::__getitem__() error - the type of keyname must be str."
		if keyname == 'sysID':
			return self._model.sysID
		elif keyname == 'name':
			return self._model.name
		elif keyname == 'security':
			return self._model.security
		elif keyname == 'jumpsNum':
			if self._model.isLoaded == False:
				self._model.load()
			return self._model.jumpsNum
		raise "SolarSystem::__getitem__() error - keyname(%s) undefined" % keyname

	def isSafe(self):
		return round(self._model.security) >= 0.5

	def is00(self):
		return round(self._model.security) <= 0

	def isNotSoSafe(self):
		return not self.is00() and not self.isSafe()

	def getNeighborInJumps(self, distance = 1, searched = set()):
		searched.add(self._model.sysID)
		if distance != 0:
			toGo = self._model.neighbor.difference(searched)
			while True:
				if len(toGo) == 0: break
				aim = toGo.pop()
				sys = SolarSystem(aim)
				searched = sys.getNeighborInJumps(distance-1, searched)
				toGo = toGo.difference(searched)
		return searched

	def __str__(self):
		return str(self._model)

	def __repr__(self):
		return "SolarSystem.SolarSystem(%d)" % self._model.sysID