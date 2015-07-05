from garzonEve.__Data import __Data
import evelink.map

class __SolarSystemModel(__Data):

	@classmethod
	def fetch(self, sysID):
		if not self.datapool.has_key(sysID):
			self.datapool[sysID] = self(sysID)
		return self.datapool[sysID]

	@classmethod
	def loadAll(self):
		# setup static data
		res = self.cur.execute("select solarSystemID from mapSolarSystems").fetchall()
		for solarArr in res:
			self.fetch(solarArr[0])

		# setup extra info
		# setup jumps info
		res = evelink.map.Map().jumps_by_system().result
		for solarSysID in self.datapool:
			self.datapool[solarSysID].isLoaded = True
			if res.has_key(solarSysID):
				self.datapool[solarSysID].jumpsNum = res[solarSysID]

	def load(self):
		self.isLoaded = True
		self.loadAll()

	# functions below are private ----------------------------

	def __init__(self, sysID):
		self.neighbor = set()
		self.sysID = arg
		self.__setInfo()
		self.__setNeighborhood()

		# extra info(lazy load) -----------
		self.isLoaded = False
		self.jumpsNum = 0

	def __setInfo(self):
		res = self.__cursor.execute("select solarSystemName, security from mapSolarSystems where solarSystemID = '%d'" % self.gid).fetchone()
		self.name = res[0]
		self.security = res[1]

	def __addNeighbor(self, sysID):
		if isinstance(sysID, int):
			self.neighbor.add(sysID)
		elif isinstance(sysID, list):
			self.neighbor = self.neighbor.union(sysID)
		else:
			raise "__SolarSystemModel::addNeighbor() - sysID type error"
	
	def __setNeighborhood(self):
		res = self.__cursor.execute("select toSolarSystemID from mapSolarSystemJumps where fromSolarSystemID = '%d'" % self.gid).fetchall()
		self.__addNeighbor([toSysID[0] for toSysID in res])

	def __str__(self):
		return "<%s(%d): %.2f, jumps: %d>" % (self.name, self.gid, self.security, self.jumpsNum)

	def __repr__(self):
		return "__SolarSystemModel.__SolarSystemModel.fetch(%d)" % self.sysID