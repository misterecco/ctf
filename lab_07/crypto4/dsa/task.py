#!/usr/bin/python
from secrets import FLAG
from dsa import verify, sign

PORT = 8365

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn

print sign("flag")
print sign("ala ma kota")

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        params = self.path[1:]
        [data, sig] = [x.decode('hex') for x in params.split(',')]
        try:
          if verify(data, int(sig)):
            if data == "flag":
               ret = FLAG
            else:
               ret = 'ok'
          else:
            ret = "bad sig"
        except:
          ret = 'error'
        self.wfile.write(ret)
        
        
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
if __name__ == "__main__":
    server = ThreadedHTTPServer(('', PORT), myHandler)
    server.serve_forever()