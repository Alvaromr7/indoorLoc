import sqlite3
db = sqlite3.connect('users.db')
db.execute("CREATE TABLE node1 (ID INTEGER PRIMARY KEY AUTOINCREMENT, MAC CHAR(100) NOT NULL, SIGNAL CHAR(100) NOT NULL, FECHA DATETIME, UNIQUE(MAC))")
db.commit()
