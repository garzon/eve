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
			if sysID.replace("-", "").isalnum(): 
				res = self._cursor.execute("select solarSystemID from mapSolarSystems where solarSystemName = '%s'" % sysID.title()).fetchall()
				if len(res) == 1:
					return self.fetch(res[0][0])
			raise Exception("_SolarSystemModel::fetch() error - unknown solar system '%s'" % sysID.title())
		raise Exception("_SolarSystemModel::fetch() error - unsupported type of sysID")

	@classmethod
	def loadAll(self):
		if self._isAllLoaded: return

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
		self._isAllLoaded = True

	def load(self):
		self.isLoaded = True
		self.loadAll()

	@classmethod
	def updateAllJumps(self):
		self.loadAll()
		for solarSysID in self._datapool:
			self._datapool[solarSysID].__updateJumps()
		self._database.commit()

	# functions below are private ----------------------------

	def __updateJumps(self):
		if not self.isLoaded: self.loadAll()
		lastCount = sum(self.jumpsHist[-5:])
		thisCount = self.jumpsNum - lastCount
		self.jumpsHist += [thisCount]
		if len(self.jumpsHist) > 48*6:
			self.jumpsHist = self.jumpsHist[1:]
		self.__saveHist()

	def __saveHist(self):
		savedStr = ','.join([str(x) for x in self.jumpsHist])
		self._cursor.execute("update mapSolarSystems set jumpsHist='%s' where solarSystemID = '%d'" % (savedStr, self.sysID))

	def __init__(self, sysID):
		assert self._isAllLoaded == False

		self.neighbor = set()
		self.sysID = sysID
		self.__setInfo()
		self.__setNeighborhood()

		# extra info(lazy load) -----------
		self.isLoaded = self._isAllLoaded
		self.jumpsNum = 0

	def __setInfo(self):
		res = self._cursor.execute("select solarSystemName, security, jumpsHist from mapSolarSystems where solarSystemID = '%d'" % self.sysID).fetchone()
		self.name = res[0]
		self.security = res[1]
		self.jumpsHist = [int(x) for x in res[2].split(',')]

	def __addNeighbor(self, sysID):
		if isinstance(sysID, int):
			self.neighbor.add(sysID)
		elif isinstance(sysID, list):
			self.neighbor = self.neighbor.union(sysID)
		else:
			raise Exception("_SolarSystemModel::addNeighbor() - sysID type error")
	
	def __setNeighborhood(self):
		res = self._cursor.execute("select toSolarSystemID from mapSolarSystemJumps where fromSolarSystemID = '%d'" % self.sysID).fetchall()
		self.__addNeighbor([toSysID[0] for toSysID in res])

	def __str__(self):
		return "<%s(%d): %.3f, jumps: %d>" % (self.name, self.sysID, self.security, self.jumpsNum)

	def __repr__(self):
		return "garzonEve._SolarSystemModel.fetch(%d)" % self.sysID