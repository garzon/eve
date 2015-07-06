import sqlite3

_db = sqlite3.connect("universeDataDx.db")
_read_cur = _db.cursor()

class _Data:
	_datapool = dict()
	_cursor = _read_cur
	_database = _db
	_isAllLoaded = False