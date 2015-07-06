import garzonEve

# test case
garzonEve.SolarSystem.loadAll()
jita = garzonEve.SolarSystem('jita')
print jita
print jita['jumpsHist']
print '-----------------'

def query(solarSys):
	if not solarSys.isNotSoSafe(): return False
	neighbor = garzonEve.SolarSystemArray.fromIDSet(solarSys.getNeighborInJumps(4)).add(solarSys['sysID'])
	neighbor = neighbor.filter(lambda sys: sys.isNotSoSafe() and sum(sys['jumpsHist'][-6*3:]) == 0)
	if neighbor.count() < 3: return False
	print neighbor[neighbor.map.keys()[0]]['jumpsHist']
	return True


allsys = garzonEve.SolarSystemArray.all()
res = allsys.filter(query)
# print res