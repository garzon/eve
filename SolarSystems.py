import Database

import SolarSystem

class SolarSystems:

	__allSystemsSingleton = 0

	def __init__(self):
		self.map = dict()

	def add(self, sys):
		if isinstance(sys, int):
			self.map[sys] = self.all().map[sys]
		elif isinstance(sys, SolarSystem.SolarSystem):
			self.map[sys.gid] = sys
		else:
			raise "SolarSystems::add() - sys type error"
		
	@staticmethod
	def all():
		if isinstance(self.__allSystemsSingleton, int):
			__allSystemsSingleton = SolarSystems()
			res = Database.cur.execute("select * from mapSolarSystems").fetchall()
			for solarArr in res:
				tmp = SolarSystem.SolarSystem(solarArr)
				__allSystemsSingleton.map[tmp.gid] = tmp
		return __allSystemsSingleton

	def query(lamExp):
		for solarSysID in self.map.keys():
			if query() == True:
				return solarSysID