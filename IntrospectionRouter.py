#!/usr/bin/env python
import sys
from ZenAPIConnector import ZenAPIConnector, ZenAPIConfig
from pprint import pprint

config_file = 'creds.cfg'

config = ZenAPIConfig(config_file)

url = config.getUrl()
username = config.getUsername()
password = config.getPassword()
ssl_verify = config.getSSLVerify()

router = 'IntrospectionRouter'
router_endpoint = '/zport/dmd/introspection_router'

def getAllRouters():
    method = 'getAllRouters'
    data = {}
    api = ZenAPIConnector(url, router, router_endpoint, method, username, password, ssl_verify, data)
    response = api.send()
    data = response.json()['result']['data']
    routers = {}
    for r in data:
        routers[r['action']] = r['urlpath']
    return routers

def getAllRouterMethods():
    all_routers = getAllRouters()
    method = 'getRouterMethods'
    router_methods = {}
    for router_name in all_routers.keys():
        data = {'router': router_name}
        api = ZenAPIConnector(url, router, router_endpoint, method, username, password, ssl_verify, data)
        response = api.send()
        sys.stdout.write('.')
        sys.stdout.flush()
        data = response.json()
        router_methods[router_name] = data
    return router_methods

def printInfo(router_methods):
    for k,v in router_methods.iteritems():
        methods = v['result']['data']
        for method, info in methods.iteritems():
            print 'ROUTER NAME: %s' % (k)
            print 'METHOD: %s' % (method)
            print 'METHOD DOCUMENTATION: %s' % info['documentation']
            print 'METHOD ARGS: %s' % info['args']
            print 'METHOD KWARGS: %s' % info['kwargs']
            print '---------------------------------------'
        print '======================================'

if __name__ == '__main__':
    router_methods = getAllRouterMethods()
    printInfo(router_methods)
