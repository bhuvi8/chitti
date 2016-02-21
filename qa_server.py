import random
import string
import sqlite3
import os, os.path
import cherrypy
#from cherrypy.lib import sessions
from statement_classifier import StmtClassify
          
class Query(object):
    def __init__(self):
        self.s_class = StmtClassify()
    
    exposed = True
    def GET(self,q):
        print(cherrypy.request.headers)
        if q:
            req_obj = {}
            #if not cherrypy.session.get('uid'):
                #print (cherrypy.session.id)
                #cherrypy.session['uid'] = ''.join(random.sample(string.hexdigits,16))
            #print (cherrypy.session['uid'])
            cherrypy.log("Req: %s" %q)
            req_obj['q'] = q
            req_obj['ip'] = cherrypy.request.remote.ip
            resp_class = self.s_class.classify(req_obj)
            cherrypy.response.status = 200
            cherrypy.log("Resp: %s" %resp_class)
            return resp_class

class Root(object):
    exposed = True            
    def GET(self): 
        print(cherrypy.request.headers)
        cherrypy.response.status = 200
        return "Hi! Ask me something"

if __name__ == '__main__':
    cherrypy.config.update('qa_server.conf')
    root = Root()
    root.q = Query()
    cherrypy.tree.mount(root, '/','qa_server.conf')
    cherrypy.engine.start()
    cherrypy.engine.block()
