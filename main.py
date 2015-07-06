import garzonEve

garzonEve.SolarSystem.loadAll()
jita = garzonEve.SolarSystem('jita')

# test case
'''
jita.printPathTo('Deltole')
print '-----------------'
'''

def query(solarSys):
	global jita
	if not solarSys.isNotSoSafe(): return False
	if not solarSys['jumpsNum'] == 0: return False
	neighbor = garzonEve.SolarSystemArray.fromIDSet(solarSys.getNeighborInJumps(5))
	if neighbor.filter(lambda sys: sys.isNotSoSafe() and solarSys['jumpsNum'] == 0).count() < 4: return False
	print "%s: %d" % (solarSys, jita.calcJumpsTo(solarSys))
	return True

allsys = garzonEve.SolarSystemArray.all()
res = allsys.filter(query)