import __Database

class __SolarSystemModel:
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
			raise "__SolarSystemModel::__init__() - arg type error"
		self.__setNeighborhood()

		# extra info
		self.jumpsNum = 0

	def __setInfo(self):
		res = __Database.cur.execute("select solarSystemName, security from mapSolarSystems where solarSystemID = '%d'" % self.gid).fetchone()
		self.name = res[0]
		self.security = res[1]

	def __addNeighbor(self, n_gid):
		if isinstance(n_gid, int):
			self.neighbor.add(n_gid)
		elif isinstance(n_gid, list):
			self.neighbor = self.neighbor.union(n_gid)
		else:
			raise "__SolarSystemModel::addNeighbor() - n_gid type error"
	
	def __setNeighborhood(self):
		res = __Database.cur.execute("select toSolarSystemID from mapSolarSystemJumps where fromSolarSystemID = '%d'" % self.gid).fetchall()
		self.__addNeighbor([toSysID[0] for toSysID in res])

	def __str__(self):
		return "%s(%d): %.2f, jumps: %d" % (self.name, self.gid, self.security, self.jumpsNum)