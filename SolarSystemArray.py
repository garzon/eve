import __Database
import evelink.map

import __SolarSystemModel

class SolarSystemArray:

	__allSystemsSingleton = 0

	def __init__(self):
		self.__map = dict() # key: sysID, value: cooresponding instance of __SolarSystemModel

	@staticmethod
	def all():
		if isinstance(self.__allSystemsSingleton, int):
			__allSystemsSingleton = SolarSystemArray()

			# setup static data
			res = __Database.cur.execute("select * from mapSolarSystems").fetchall()
			for solarArr in res:
				tmp = __SolarSystemModel.__SolarSystemModel(solarArr)
				__allSystemsSingleton.__map[tmp.gid] = tmp

			# setup extra info
			# setup jumps info
			res = evelink.map.Map().jumps_by_system().result
			for solarSysID in __allSystemsSingleton.__map:
				if res.has_key(solarSysID):
					__allSystemsSingleton.__map[solarSysID].jumpsNum = res[solarSysID]
		return __allSystemsSingleton

	def add(self, sysID):
		res = self.all().__map[sysID]
		self.__map[sysID] = res
		return res

	def remove(self, sysID):
		return self.__map.pop(sysID)

	def count(self):
		return len(self.__map)

	def filter(self, lamExp):
		ret = SolarSystemArray()
		for solarSysID in self.__map:
			if query(self.all().__map[solarSysID]) == True:
				ret.add(solarSysID)
		return ret

	def getSysIDList(self):
		return self.__map.keys()

	def __str__(self):
		return str(self.__map)