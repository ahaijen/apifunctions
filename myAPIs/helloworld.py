# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a HelloWorld REST API - part of myAPIs module
"""

 
    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
def process(argdict, header, body):
       method = 'POST'
       if 'method' in argdict: method = argdict['method']
       for key in body: argdict[key] = body[key]
       argdict['helloworld'] = method + ' Hello World'
       return argdict