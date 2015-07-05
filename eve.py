import SolarSystems

query = lambda map, solarSys: solarSys.isLowSafety() && 
							solarSys.kills == 0 && 
							solarSys.sov == 0 && 