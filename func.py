import io
import json
import oci
import logging
import myAPIs
from urllib.parse import urlparse, parse_qs
from myAPIs import utils, helloworld, forwardToServiceWithXform
from fdk import response



def handler(ctx, data: io.BytesIO = None):
    logging.getLogger().info("Simple API Gateway Starting")  
    resp = {}
    requesturl = ctx.RequestURL()
    
    logging.getLogger().info("Request URL: " + json.dumps(requesturl))
    parsed_url = urlparse(requesturl)
    query_string = utils.parse_args(parse_qs(parsed_url.query))

    logging.getLogger().info("Query string: " + json.dumps(query_string))
    config = dict(ctx.Config())
    utils.init(config)
        
    logging.getLogger().info("Configuration: " + json.dumps(config))
    
    headers = ctx.Headers()
    logging.getLogger().info("Headers: " + json.dumps(headers))
    resp["Headers"] = headers
    
    try:
        requestbody_str = data.getvalue().decode('UTF-8')
        body = {}
        if requestbody_str:
            body = json.loads(requestbody_str)
            resp["Request body"] = body
        else:
            resp["Request body"] = {}
    except Exception as ex:
        print('ERROR: The request body is not JSON', ex, flush=True)
        raise
    
    action = 'action'
    if action in query_string: action = query_string['action']
    
    if action == 'getfatoken':
        username, password = utils.getCredentials(query_string)
        resp = {}
        resp["username"] = username
        resp["password"] = password
    elif action == 'forwardXformDummy':
        resp = forwardToServiceWithXform.processdummy(query_string, headers, body)
    elif action == 'forwardXform':
        resp = forwardToServiceWithXform.process(query_string, headers, body)
    elif action == 'helloworld':
        resp = helloworld.process(query_string, headers, body)
    else:
        resp["config"] = config
        resp["query_string"] = query_string
        
    logging.getLogger().info("function handler end")
    return response.Response(
        ctx, 
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )