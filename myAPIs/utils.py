# -*- coding: utf-8 -*-
"""
Spyder Editor

utils used by other modules

"""

import myAPIs
import jwt
import time
import OpenSSL
import oci.object_storage

def getUserName():
    return 'defaultuser'

def getPassword():
    return 'defaultpwd'

def getFileName():
    return '/tmp/ahjwt.kst'

def getHeader(header):
    new_header = {}
    for element, value in header.items():
        if element != "Authorization": new_header[element] = value
    return new_header

def parse_args(query_string):
    new_qs = {}
    for key in query_string:
        element = query_string[key]
        new_qs[key] = element[0]
    return new_qs

def withToken(args):
    argdict = dict(args)
    if 'pw' in argdict: 
        if argdict['pw'] == 'getfatoken': 
            return True
        else:
            return False
    else:
        return False
    
def init(config):
    myAPIs.PWDICT.clear()
    myAPIs.TOKENDICT.clear()
    
    for key in config:
        value = config[key]
        if key.startswith('pw'):
           myAPIs.PWDICT[key[2:]] = value.split(':::')
            
        if key == 'privatekeypw':
           bucket, filename, password = value.split(':::')
           getKey(bucket, filename, password)
           
        if key.startswith('tk'):
           myAPIs.TOKENDICT[key[2:]] = value
    
def getCredentials(args):
    argdict = dict(args)
    username = getUserName()
    password = getPassword()
    if 'pwid' in argdict:
        if argdict['pwid'] in myAPIs.PWDICT: username, password = myAPIs.PWDICT[argdict['pwid']]
    if 'un' in argdict: username = argdict['un']
    if 'pw' in argdict: password = argdict['pw']
    if password == 'getfatoken': password = getToken(username)
    return username, password

def getKey(bucket, filename, password):
    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    namespace = client.get_namespace().data
    object = client.get_object(namespace, bucket, filename)
    with open(getFileName(), 'wb') as f:
        for chunk in object.data.raw.stream(1024 * 1024, decode_content=False):
            f.write(chunk)
    p12 = OpenSSL.crypto.load_pkcs12(open(getFileName(),'rb').read(), password)
    private_key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey())
    myAPIs.TOKENDICT['private_key'] = private_key
    return private_key

def getToken(username):
    payload = {}
    headers = {}

    headers['alg'] = myAPIs.TOKENDICT['alg']
    headers['typ'] = myAPIs.TOKENDICT['typ']
    headers['x5t'] = myAPIs.TOKENDICT['x5t']
    payload['prn'] = username
    payload['iss'] = myAPIs.TOKENDICT['iss']
    payload['iat'] = int(time.time())
    payload['exp'] = int(time.time()) + int(myAPIs.TOKENDICT['minutes'])*60
    # if 'private_key' not in myAPIs.TOKENDICT: getKey()
    
    token = jwt.encode(payload = payload, key = myAPIs.TOKENDICT['private_key'], headers = headers, algorithm = "RS256")
    
    if type(token) == 'bytes': token = token.decode('utf-8')
    
    return token
