#!/usr/bin/env python
from bottle import route, run, template, request, SimpleTemplate, Bottle,abort,debug
import sys
# sys.path.append("../python")
from connectedDevices import *

app = Bottle()

@app.route('/')
def index():
# def handle_websocket():
#     wsock = request.environ.get('wsgi.websocket')
#     if not wsock:
#         abort(400, 'Expected WebSocket request.')
#
#     while True:
#         try:
#             message = wsock.receive()
#             wsock.send("Your message was: %r" % message)
#         except WebSocketError:
#             break
#
#     from gevent.pywsgi import WSGIServer
#     from geventwebsocket import WebSocketError
#     from geventwebsocket.handler import WebSocketHandler
#     server = WSGIServer(("localhost", 8080), app,
#                         handler_class=WebSocketHandler)
#     server.serve_forever()

    info={'iplist': iplist, 'maclist': maclist, 'signallist': signallist, 'hostlist': hostlist}
    return template('views/simple.tpl', info)


if __name__ == '__main__':
    app.run()

debug(True)
run(host='localhost', port=8080, reloader=True)
