import sqlite3
def vaccuum():
	con = sqlite3.connect("scraperwiki.sqlite")
	con.execute("VACUUM")
	con.close()

vaccuum() 