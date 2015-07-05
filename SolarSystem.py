import Database

class SolarSystem:
	def __init__(self, arg):
		self.neighbor = set()
		if isinstance(arg, int):
			self.gid = arg
			self.__setInfo()
		elif isinstance(arg, tuple):
			self.name = arg[3]
			self.security = arg[20]
			self.gid = arg[2]
		else:
			raise "SolarSystem::__init__() - arg type error"
		self.__setNeighborhood()

	def __setInfo(self):
		res = Database.cur.execute("select solarSystemName, security from mapSolarSystems where solarSystemID = '%d'" % self.gid).fetchone()
		self.name = res[0]
		self.security = res[1]
	
	def __setNeighborhood(self):
		res = Database.cur.execute("select toSolarSystemID from mapSolarSystemJumps where fromSolarSystemID = '%d'" % self.gid).fetchall()
		self.addNeighbor([toSysID[0] for toSysID in res])

	def isSafe(self):
		return round(safety) >= 0.5

	def is00(self):
		return round(safety) <= 0

	def isLowSafety(self):
		return not self.is00() and not self.isSafe()

	def addNeighbor(self, n_gid):
		if isinstance(n_gid, int):
			self.neighbor.add(n_gid)
		elif isinstance(n_gid, list):
			self.neighbor = self.neighbor.union(n_gid)
		else:
			raise "SolarSystem::addNeighbor() - n_gid type error"

	def getNeighbor(self, dist):
		if dist == 0: return set()
		