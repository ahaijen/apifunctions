# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a getFaToken REST API - part of myAPIs module
"""

# using flask_restful
from myAPIs import utils

class GetFAToken():
  
    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(args):
       username, password = utils.getCredentials(args)
       if utils.withToken(args):
           return {"token": password }
       else:
           return {"token": "no token" }