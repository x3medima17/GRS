import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.websocket
import os
import json


from math import atan2,sqrt 
from tornado.options import define, options
from pprint import pprint

define("port",default=9090,help="Service port",type=int)
options.parse_command_line()


clients = []
axes = ['heading','pitch','roll']
fingers = ['wrist','thumb','index','middle','ring','pinky']

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/ws",WebSocketHandler),
        ]
        
        settings = dict(
            debug = True,
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            login_url = "/auth",
            cookie_secret = "Settings.COOKIE_SECRET",
            
        )
        tornado.web.Application.__init__(self,handlers,**settings)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self,origin):
        return True

    def open(self):
        print "Connetion oppened"
        clients.append(self)

    def on_message(self,message):
        print "Got message: %s" % message
        raw = message.replace(";"," ")
        data = message.split(";")

        message = dict()
        for i in xrange(6):
            tmp = data[i].split(' ')
            print tmp
            x = float(tmp[0])*1.0
            y = float(tmp[1])*1.0
            z = float(tmp[2])*1.0
            message[fingers[i]] = dict(
                    heading = atan2(y,x),
                    roll = atan2(y,sqrt(x**2+z**2)),
                    pitch = atan2(x,sqrt(y**2+z**2)),
                    x = x,
                    y = y,
                    z = z
                )
        acc = data[-1].split(' ')

        message["wrist"]['acceleration-w'] = acc[0]
        message["wrist"]['acceleration-x'] = acc[1]
        message["wrist"]['acceleration-y'] = acc[2]
        message["wrist"]['acceleration-z'] = acc[3]
        
        data = dict(
            data = message,
            raw = raw
            )

        message = json.dumps(data)
        for client in clients:
            client.write_message(message)


    def on_close(self):
        print "Connetion closed"
        clients.remove(self)


if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()