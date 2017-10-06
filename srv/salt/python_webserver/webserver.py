#!/usr/bin/env python3

import datetime
import json
from bottle import error, get, post, response, request, run
from sqlalchemy import *

@error(405)
def custom405(error):
    response.status = 401
    return json.dumps({"error": "invalid method"})

@get('/now')
def now():
    return "Current date and time is " + '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

@post('/later')
def later():
    if request.method == 'POST' and 'name' in request.POST:
        name = request.forms.get("name")

        if name == '':
            response.status = 402
            return json.dumps({"error": "invalid name", "payload": name})
        elif name.isalnum():
            return json.dumps({"status": "ok"})
        else:
            response.status = 402
            return json.dumps({"error": "invalid name", "payload": name})

    response.status = 402
    return json.dumps({"error": "name=foo is the only valid param"})

@get('/check')
def check():
    m = MetaData()
    t = Table('t', m, Column('x', Integer))
    s = select([t], for_update="read")
    
    #try:
    url = 'postgresql://plugdj:plugdj@localhost:5432/plugdj'
    engine = sqlalchemy.create_engine(url, client_encoding='utf8', echo=True)
    with engine.begin() as conn:
        m.create_all(conn)
        conn.execute(s)
        
    connection = engine.connect() 
    return connection

run(host='localhost', port=9000, debug=True)