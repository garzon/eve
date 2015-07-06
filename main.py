import garzonEve

# test case
garzonEve.SolarSystem.loadAll()
jita = garzonEve.SolarSystem('jita')
print jita
print jita['jumpsHist']
print '-----------------'

def query(solarSys):
	return solarSys.isNotSoSafe() and garzonEve.SolarSystemArray.fromIDSet(solarSys.getNeighborInJumps(4)).add(solarSys['sysID']).filter(lambda sys: sys.isNotSoSafe() and sum(sys['jumpsHist'][-6*3:]) == 0).count >= 2

allsys = garzonEve.SolarSystemArray.all()
res = allsys.filter(query)
print res