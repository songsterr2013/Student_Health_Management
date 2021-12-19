from main import app

from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop

if __name__ == '__main__':

    s = HTTPServer(WSGIContainer(app))
    s.listen(8090)  # 監聽 9900 端口
    IOLoop.current().start()

    #app.run(debug=True, host="0.0.0.0", port=8090)
