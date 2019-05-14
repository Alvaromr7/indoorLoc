#!/usr/bin/env python
from bottle import route, run, template, request, SimpleTemplate, Bottle
import sys
sys.path.append("../python")
from connectedDevices import *

app = Bottle()

@app.route('/')
def index():
    info={'iplist': iplist, 'maclist': maclist, 'signallist': signallist, 'hostlist': hostlist}
    tpl = '''
    <table>
        <tr>
        	<td>IP address</td>
        	<td>Hostname</td>
        	<td>MAC address</td>
        	<td>Signal</td>
        </tr>
        %for i in range(len(maclist)):
            <tr>
                <td>{{iplist[i]}}</td>
                <td>{{hostlist[i]}}</td>
                <td>{{maclist[i]}}</td>
                <td>{{signallist[i]}}</td>
            </tr>
        %end
    </table>
    '''
    return template(tpl, info)


if __name__ == '__main__':
    app.run()

run(host='localhost', port=8080, reloader=True)
