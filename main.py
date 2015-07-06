import garzonEve

# test case
garzonEve.SolarSystem.loadAll()
jita = garzonEve.SolarSystem('jita')
print jita
print '-----------------'
print garzonEve.SolarSystemArray.fromIDSet(jita.getNeighborInJumps())
print '-----------------'
print garzonEve.SolarSystemArray.fromIDSet(jita.getNeighborInJumps()).filter(lambda sys: sys['security'] > 0.9)

print '-----------------'

exit()

def query(solarSys):
	return solarSys.isNotSoSafe() and garzonEve.SolarSystemArray.fromIDSet(solarSys.getNeighborInJumps(4)).add(solarSys['sysID']).filter(lambda sys: sys.isNotSoSafe() and sys['jumpsNum'] == 0).count >= 2

allsys = garzonEve.SolarSystemArray.all()
res = allsys.filter(query)
print res