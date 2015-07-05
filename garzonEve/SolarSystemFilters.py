def lowerSec(sys):
	return sys.isNotSoSafe()

def safeSec(sys):
	return sys.isSafe()

def sec00(sys):
	return sys.is00()

def andQuery(q1, q2):
	return lambda sys: q1(sys) and q2(sys)

def orQuery(q1, q2):
	return lambda sys: q1(sys) or q2(sys)

def notQuery(q):
	return lambda sys: not q(sys)