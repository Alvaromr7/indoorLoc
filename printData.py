#!/usr/bin/env python
from bottle import route, run, template, request, SimpleTemplate, Bottle,abort,debug
import sqlite3
import json

@route('/', method='POST')
def index():
    body = request.body.read().decode('utf8') # read directly HTTP input
    get_dict = json.loads(body) # decode json and get native python dict
    maclist = get_dict.get('maclist')
    signallist = get_dict.get('signallist')

    data_list = list(zip(maclist, signallist))
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    try:
        c.executemany("INSERT INTO users (MAC,SIGNAL) VALUES(?,?)", data_list)
    except Exception as exc:
        c.executemany("REPLACE INTO users (MAC,SIGNAL) VALUES(?,?)", data_list)


    conn.commit()
    return "Items added."

run(host='0.0.0.0', port=8080)
