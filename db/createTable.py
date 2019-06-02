import sqlite3
db = sqlite3.connect('users.db')
db.execute("CREATE TABLE users (ID INTEGER PRIMARY KEY AUTOINCREMENT, MAC CHAR(100) NOT NULL, SIGNAL CHAR(100) NOT NULL, UNIQUE(MAC))")
db.execute("INSERT INTO users (MAC,SIGNAL) VALUES ('a1:b2:c3:d4:e5:f6', -25)")
db.commit()
