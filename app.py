import os, json, cherrypy
from bseHandler import stockTopTen, stockByName, getOperationDetails , saveToRedis

class MainPage(object):
    @cherrypy.expose
    def index(self):
        return open("index.html")

@cherrypy.expose
class StockList(object):
    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def GET(self):
        return stockTopTen()

@cherrypy.expose
class StockListUpdate(object):
    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def GET(self):
        saveToRedis()
        return {'Response' : True}

@cherrypy.expose
class OperationDetails(object):
    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def GET(self):
        _fechDate = getOperationDetails()
        return _fechDate[0] ,_fechDate[1]

@cherrypy.expose
class StockSearch(object):
    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def GET(self, name):
        return stockByName(name)

if __name__ == "__main__":

    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 5000))
        },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/update':{
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/operation':{
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/stocks': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/stocks/search': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'public'
        }
    }
    bseApp = MainPage()
    bseApp.update = StockListUpdate()
    bseApp.stocks = StockList()
    bseApp.operation = OperationDetails()
    bseApp.stocks.search = StockSearch()
    cherrypy.quickstart(bseApp, '/', conf)