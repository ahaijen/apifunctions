# -*- coding: utf-8 -*-
"""
Spyder Editor

This one calls forwards a GET or POST to a new server after Xforming the URL - part of myAPIs module

api.add_resource(forwardToServiceWithXform.ForwardToServiceDummy, '/*/<string:secure>/<string:method>/<path:u_path>')

"""

# using flask_restful
from myAPIs import utils
import requests
import json

def getURL(argdict, u_path, secure):
    newbody = {}
    if secure == 'N':
        finalurl = 'http://' + u_path
    else:
        finalurl = 'https://' + u_path
    i = 0
    for key in argdict:
       if key not in ('un', 'pw', 'pwid', 'u_path', 'method', 'secure', 'action'):
          if key.startswith('URL'):
             param = key[3:]
             value = argdict[key]
             finalurl = finalurl.replace(param, value)
          elif key.startswith('BODY'):
             param = key[4:]
             value = argdict[key]
             newbody[param] = value
          else:
             if i == 0:
                finalurl = finalurl + '?'
                i = 1
             else:
                finalurl = finalurl + '&'
             finalurl = finalurl + key + '=' + argdict[key]
    return newbody, finalurl

def handlerequestdummy(argdict, header, body, method, secure, u_path):
    newbody, finalurl = getURL(argdict, u_path, secure)
    username, password = utils.getCredentials(argdict)
    argdict['username'] = username
    argdict['password'] = password
    argdict['u_path'] = u_path
    argdict['finalurl'] = finalurl
    # argdict['isjson'] = request.is_json
    argdict['method'] = method
    for key in newbody: argdict[key] = newbody[key]
    for key in body: argdict[key] = body[key]
    return argdict
         
def handlerequest(argdict, header, body, method, secure, u_path):
    newbody, finalurl = getURL(argdict, u_path, secure)
    username, password = utils.getCredentials(argdict)
    content = dict(body)
    for key in newbody: content[key] = newbody[key]
    data = json.dumps(content)
    headers = { "Content-Type" : "application/json" }
    if utils.withToken(argdict):
        headers['Authorization'] = 'Bearer ' + password
        if method == 'post':
            response = requests.post(url=finalurl, headers=headers, data=data)
        elif method == 'patch':
            response = requests.patch(url=finalurl, headers=headers, data=data)
        elif method == 'delete':
            response = requests.delete(url=finalurl, headers = headers, data=data)
        elif method == 'get':
            response = requests.get(url=finalurl, headers = headers, data=data)
        else:
            response = requests.post(url=finalurl, headers=headers, data=data)    
    else:
        if method == 'post':
            response = requests.post(url=finalurl, headers = headers, auth=(username,password), data=data)
        elif method == 'patch':
            response = requests.patch(url=finalurl, headers = headers, auth=(username,password), data=data)
        elif method == 'delete':
            response = requests.delete(url=finalurl, headers = headers, auth=(username,password), data=data)
        elif method == 'get':
            response = requests.get(url=finalurl, headers = headers, auth=(username,password), data=data)
        else:
            response = requests.post(url=finalurl, headers = headers, auth=(username,password), data=data)    
    try:
        return response.json()
    except:
        return response.text
    
def processdummy(argdict, header, body):
        secure = 'Y'
        method = 'POST'
        u_path = "localhost"
        if 'secure' in argdict: secure = argdict['secure']
        if 'method' in argdict: method = argdict['method']
        if 'u_path' in argdict: u_path = argdict['u_path']
        return handlerequestdummy(argdict, header, body, method, secure, u_path)

def process(argdict, header, body):
        secure = 'Y'
        method = 'POST'
        u_path = "localhost"
        if 'secure' in argdict: secure = argdict['secure']
        if 'method' in argdict: method = argdict['method']
        if 'u_path' in argdict: u_path = argdict['u_path']
        return handlerequest(argdict, header, body, method, secure, u_path)