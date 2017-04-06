#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
from encryptor import encrypt as encrypt_block

master_key = open("key.txt").read(3).encode('hex')

print('master_key', int(master_key, 16))

PORT = 8353

ROUNDS = 2**24
def encrypt(key, plaintext):
    ciphertext = encrypt_block(int(plaintext, 16), int(key, 16), ROUNDS)
    return hex(ciphertext)[2:].rjust(6, '0')

class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        data = self.path[1:]
        self.wfile.write("plaintext: " + data + "\n")
        #try:
        encrypted = encrypt(master_key, data)
        #except:
        #  encrypted = "error"
        self.wfile.write("ciphertext: " + encrypted)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
if __name__ == "__main__":
    server = ThreadedHTTPServer(('', PORT), myHandler)
    server.serve_forever()