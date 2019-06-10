#!/usr/bin/env python
from bottle import route, run, template, request
import sqlite3
import json
import time
from datetime import datetime, timedelta

@route('/', method='POST')
def index():
    body = request.body.read().decode('utf8') # read directly HTTP input
    get_dict = json.loads(body) # decode json and get native python dict
    id = get_dict.get('id')
    maclist = get_dict.get('maclist')
    signallist = get_dict.get('signallist')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nowlist = []
    for i in range(len(maclist)):
        nowlist.append(now)
    data_list = list(zip(maclist, signallist, nowlist))


    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    if (id == 1):
        c.executemany("REPLACE INTO node1 (MAC,SIGNAL,FECHA) VALUES(?,?,?)", data_list)
    if (id == 2):
        c.executemany("REPLACE INTO node2 (MAC,SIGNAL,FECHA) VALUES(?,?,?)", data_list)
    conn.commit()

    return "Items added.\n"

@route('/data', method='GET')
def index():
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    t = datetime.now() - timedelta(seconds = 3)
    c.execute('SELECT * FROM node1 where fecha > ?', (t,))
    node1_table = c.fetchall()
    c.execute('SELECT * FROM node2 where fecha > ?', (t,))
    node2_table = c.fetchall()

    return template('simple.tpl', rows1 = node1_table, rows2 = node2_table)

run(host='0.0.0.0', port=8080)
