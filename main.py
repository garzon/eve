import garzonEve

# test case
garzonEve.SolarSystem.loadAll()
jita = garzonEve.SolarSystem('jita')
print jita
print '-----------------'

def query(solarSys):
	global jita
	if not solarSys.isNotSoSafe(): return False
	if not solarSys['jumpsNum'] == 0: return False
	neighbor = solarSys.getNeighborInJumps(5)
	if neighbor.filter(lambda sys: sys.isNotSoSafe() and solarSys['jumpsNum'] == 0).count() < 3: return False
	print solarSys
	print jita.calcJumpsTo(solarSys)
	return True

allsys = garzonEve.SolarSystemArray.all()
res = allsys.filter(query)