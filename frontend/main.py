import tornado.web
import tornado.ioloop
import tornado.httpserver
import os
import fx
import pymongo 
import grs
import sys
import json

import tornado.options
from tornado.options import define, options

define("port",default=8080,help="Service port",type=int)
#options.log_file_prefix = os.path.join(os.path.dirname(__file__),"logfile.log")

options.parse_command_line()

conn = pymongo.MongoClient()
db = conn.grs


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",MainHandler),

            (r"/gestures",GesturesHadler),
            (r"/gestures/add",GesturesAddHandler)
        ]
        
        settings = dict(
            debug = True,
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            login_url = "/auth",
            cookie_secret = "Settings.COOKIE_SECRET",
            
        )
        tornado.web.Application.__init__(self,handlers,**settings)


class BaseHandler(tornado.web.RequestHandler):
    pass

class MainHandler(BaseHandler):
    def get(self):
        data = dict(
            wrist = dict(
                heading = 0,
                pitch = 0,
                roll = 0,
                ),
            thumb = dict(
                heading = 0,
                pitch = 0,
                roll = 0,
                ),
            index = dict(
                heading = 0,
                pitch = 0,
                roll = 0,
                ),
            middle = dict(
                heading = 0,
                pitch = 0,  
                roll = 0,
                ),
            ring = dict(
                heading = 0,
                pitch = 0,
                roll = 0,
                ),
            pinky = dict(
                heading = 0,
                pitch = 0,
                roll = 0,
                ),
            )
        page_data = dict(
            data = data,
            title = "GRS Home"
            )
        self.render("index.html",**page_data)

class GesturesHadler(BaseHandler):
    def get(self):
        page_data = dict(
            title = "GRS Home"
            )
        self.render("gestures.html",**page_data)


class GesturesAddHandler(BaseHandler):
    def get(self):
        page_data = dict(
            title = "Add gesture"
            )
        self.render("gestures.add.html",**page_data)

    def post(self):
        name = self.get_argument("gesture",None)
        training_data = self.get_argument("training_data",None)
        if not name or not training_data:
            self.write(fx.gen_result(1,"Missing data"))
            return

        try:
            training_data = json.loads(training_data)
        except:
            self.write(fx.gen_result(2,"Wrong format"))
            return

        obj = grs.GRS("grs")

        result = obj.add_gesture(name,training_data)
        self.write(fx.gen_result(**result))
        




if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()