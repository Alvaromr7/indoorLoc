#!/usr/bin/env python
from bottle import route, run, template, request
import sqlite3
import json
import time

@route('/', method='POST')
def index():
    body = request.body.read().decode('utf8') # read directly HTTP input
    get_dict = json.loads(body) # decode json and get native python dict
    id = get_dict.get('id')
    maclist = get_dict.get('maclist')
    signallist = get_dict.get('signallist')

    data_list = list(zip(maclist, signallist))
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    if (id == 1):
        try:
            c.executemany("INSERT INTO node1 (MAC,SIGNAL) VALUES(?,?)", data_list)
        except Exception as exc:
            c.executemany("REPLACE INTO node1 (MAC,SIGNAL) VALUES(?,?)", data_list)
    if (id == 2):
        try:
            c.executemany("INSERT INTO node2 (MAC,SIGNAL) VALUES(?,?)", data_list)
        except Exception as exc:
            c.executemany("REPLACE INTO node2 (MAC,SIGNAL) VALUES(?,?)", data_list)
    conn.commit()

    # time.sleep(10)
    # c.execute('DELETE from users')
    # conn.commit()

    return "Items added.\n"

@route('/data', method='GET')
def index():
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM node1')
    node1_table = c.fetchall()
    c.execute('SELECT * FROM node2')
    node2_table = c.fetchall()
    # isEmpty = c.execute('SELECT count(*) from users')
    #
    # if (isEmpty != 0):
    #     c.execute('SELECT * FROM users')

    return template('simple.tpl', rows1 = node1_table, rows2 = node2_table)

run(host='0.0.0.0', port=8080)
