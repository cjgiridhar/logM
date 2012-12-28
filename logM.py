import tornado
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import os, uuid, re, json

define("uploads", default = "syslog/")

class Form(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class JSON(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        data = json.loads(fileinfo['body'])
        if 'error' in  data.keys():
                self.write("ERROR" + data['error'])
        if 'info' in data.keys():
                self.write("INFO" + data['info'])

class Text(tornado.web.RequestHandler):
        def post(self):
                fileinfo = self.request.files['filearg'][0]
                lines = fileinfo['body'].split('\n')
                string = ''
                for line in lines:
                        if re.search('error',line):
                                string += "ERROR " + line + "<br />"
                        if re.search('info',line):
                                string += "INFO: " + line + "<br />"
                self.write(string)

application = tornado.web.Application([
        (r"/", Form),
        (r"/json", JSON),
        (r"/text", Text),
        ], debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
