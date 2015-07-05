from _Data import _Data
import evelink.map

class _SolarSystemModel(_Data):

	@classmethod
	def fetch(self, sysID):
		if isinstance(sysID, int):
			if not self._datapool.has_key(sysID):
				self._datapool[sysID] = self(sysID)
			return self._datapool[sysID]
		elif isinstance(sysID, str):
			sysID = sysID.replace("-", "")
			if sysID.isalnum(): 
				res = self._cursor.execute("select solarSystemID from mapSolarSystems where solarSystemName = '%s'" % sysID.title()).fetchall()
				if len(res) == 1:
					return self.fetch(res[0][0])
			raise Exception("_SolarSystemModel::fetch() error - unknown solar system")
		raise Exception("_SolarSystemModel::fetch() error - unsupported type of sysID")

	@classmethod
	def loadAll(self):
		# setup static data
		res = self._cursor.execute("select solarSystemID from mapSolarSystems").fetchall()
		for solarArr in res:
			self.fetch(solarArr[0])

		# setup extra info
		# setup jumps info
		res = evelink.map.Map().jumps_by_system().result[0]
		for solarSysID in self._datapool:
			self._datapool[solarSysID].isLoaded = True
			if res.has_key(solarSysID):
				self._datapool[solarSysID].jumpsNum = res[solarSysID]

	def load(self):
		self.isLoaded = True
		self.loadAll()

	# functions below are private ----------------------------

	def __init__(self, sysID):
		self.neighbor = set()
		self.sysID = sysID
		self.__setInfo()
		self.__setNeighborhood()

		# extra info(lazy load) -----------
		self.isLoaded = False
		self.jumpsNum = 0

	def __setInfo(self):
		res = self._cursor.execute("select solarSystemName, security from mapSolarSystems where solarSystemID = '%d'" % self.sysID).fetchone()
		self.name = res[0]
		self.security = res[1]

	def __addNeighbor(self, sysID):
		if isinstance(sysID, int):
			self.neighbor.add(sysID)
		elif isinstance(sysID, list):
			self.neighbor = self.neighbor.union(sysID)
		else:
			raise Exception("__SolarSystemModel::addNeighbor() - sysID type error")
	
	def __setNeighborhood(self):
		res = self._cursor.execute("select toSolarSystemID from mapSolarSystemJumps where fromSolarSystemID = '%d'" % self.sysID).fetchall()
		self.__addNeighbor([toSysID[0] for toSysID in res])

	def __str__(self):
		return "<%s(%d): %.3f, jumps: %d>" % (self.name, self.sysID, self.security, self.jumpsNum)

	def __repr__(self):
		return "__SolarSystemModel.__SolarSystemModel.fetch(%d)" % self.sysID