import sqlite3

db = sqlite3.connect("universeDataDx.db")
read_cur = db.cursor()

class __Data:
	datapool = dict()
	__cursor = read_cur
