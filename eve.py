import garzonEve

query = lambda solarSys: solarSys.isNotSoSafe() and solarSys['jumpsNum'] == 0
allsys = garzonEve.SolarSystemArray.all()
res = allsys.filter(query)
print res