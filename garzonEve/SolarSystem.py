from _SolarSystemModel import _SolarSystemModel 

class SolarSystem:

	@classmethod
	def loadAll(self):
		_SolarSystemModel.loadAll()

	def __init__(self, sysID):
		self._model = _SolarSystemModel.fetch(sysID)

	def __getitem__(self, keyname):
		if not isinstance(keyname, str): raise Exception("SolarSystem::__getitem__() error - the type of keyname must be str.")
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
		raise Exception("SolarSystem::__getitem__() error - keyname(%s) undefined" % keyname)

	def isSafe(self):
		return round(self._model.security*10) >= 5

	def is00(self):
		return round(self._model.security*10) <= 0

	def isNotSoSafe(self):
		return (not self.is00()) and (not self.isSafe())

	def _getNeighborInJumps(self, distance, searched):
		searched.add(self._model.sysID)
		if distance != 0:
			toGo = self._model.neighbor.difference(searched)
			while True:
				if len(toGo) == 0: break
				aim = toGo.pop()
				sys = SolarSystem(aim)
				searched = sys._getNeighborInJumps(distance-1, searched)
				toGo = toGo.difference(searched)
		return searched

	def getNeighborInJumps(self, distance = 1):
		ret = self._getNeighborInJumps(distance, set())
		ret.remove(self._model.sysID)
		return ret

	@classmethod
	def calcJumpsFrom(self, sys):
		if isinstance(sys, int): sys = self(sys)
		return sys.calcJumpsFromThis()

	def calc

	@classmethod
	def updateAllJumps(self):
		_SolarSystemModel.updateAllJumps()

	def __str__(self):
		return str(self._model)

	def __repr__(self):
		return "garzonEve.SolarSystem(%d)" % self._model.sysID