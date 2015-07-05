import garzonEve

jita = garzonEve.SolarSystem('jita')
print jita
print garzonEve.SolarSystemArray.fromIDSet(jita.getNeighborInJumps())
exit()

query = lambda solarSys: solarSys.isNotSoSafe()
allsys = garzonEve.SolarSystemArray.all()
res = allsys.filter(query)
print res