from _Data import _Data
import evelink.map

class _SolarSystemModel(_Data):

	calcJumpsFromWhere = -1

	@classmethod
	def fetch(self, sysID):
		if isinstance(sysID, int):
			if not self._datapool.has_key(sysID):
				self._datapool[sysID] = self(sysID)
			return self._datapool[sysID]
		elif isinstance(sysID, str):
			if sysID.replace("-", "").isalnum(): 
				res = self._cursor.execute("select solarSystemID from mapSolarSystems where solarSystemName = '%s'" % sysID.capitalize()).fetchall()
				if len(res) == 1:
					return self.fetch(res[0][0])
			raise Exception("_SolarSystemModel::fetch() error - unknown solar system '%s'" % sysID.capitalize())
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

	def getNeighborInJumps(self, distance = 1):
		ret = self._getNeighborInJumps(distance, set())
		ret.remove(self.sysID)
		return ret

	@classmethod
	def printPath(self, sys):
		if isinstance(sys, int):
			if sys == 0: return
			sys = self.fetch(sys)
		self.printPath(sys.shortPathSysID)
		print sys

	def shortestPath(self):
		self.calcJumpsFromWhere = self.sysID
		self.loadAll()
		for solarSysID in self._datapool:
			self._datapool[solarSysID].jumpsFrom = 99999999
		self.jumpsFrom = 0
		self.shortPathSysId = 0
		queue = [self.sysID]
		while len(queue) > 0:
			start = self.fetch(queue[0])
			queue = queue[1:]
			neighbors = start.getNeighborInJumps()
			for sysID in neighbors:
				neighbor = self.fetch(sysID)
				if neighbor.jumpsFrom > start.jumpsFrom + 1:
					neighbor.shortPathSysID = start.sysID
					neighbor.jumpsFrom = start.jumpsFrom + 1
					if sysID not in queue:
						queue.append(sysID)

	# functions below are private ----------------------------

	def __init__(self, sysID):
		assert self._isAllLoaded == False

		self.neighbor = set()
		self.sysID = sysID
		self.__setInfo()
		self.__setNeighborhood()

		# extra info(lazy load) -----------
		self.isLoaded = self._isAllLoaded
		self.jumpsNum = 0
		self.jumpsFrom = 0
		self.shortPathSysID = 0

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
			raise Exception("_SolarSystemModel::addNeighbor() - sysID type error")
	
	def __setNeighborhood(self):
		res = self._cursor.execute("select toSolarSystemID from mapSolarSystemJumps where fromSolarSystemID = '%d'" % self.sysID).fetchall()
		self.__addNeighbor([toSysID[0] for toSysID in res])

	def _getNeighborInJumps(self, distance, searched):
		searched.add(self.sysID)
		if distance != 0:
			toGo = self.neighbor.difference(searched)
			while True:
				if len(toGo) == 0: break
				aim = toGo.pop()
				sys = self.fetch(aim)
				searched = sys._getNeighborInJumps(distance-1, searched)
				toGo = toGo.difference(searched)
		return searched

	def __str__(self):
		return "<%s(%d): %.3f, jumps: %d>" % (self.name, self.sysID, self.security, self.jumpsNum)

	def __repr__(self):
		return "garzonEve._SolarSystemModel.fetch(%d)" % self.sysID