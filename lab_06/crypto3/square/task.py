#!/usr/bin/python
from aes import AES, text2matrix, matrix2text

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn


master_key = open("key.txt").read(16).encode('hex')
flag = open("flag.txt").read(16).encode('hex')

PORT = 8354

def revhex(s):
  return s.decode("hex")[::-1].encode('hex')

def encrypt(key, data, rounds):
    cipher = AES(int(key, 16))
    square = text2matrix(int(revhex(data), 16))

    cipher.add_round_key(square, cipher.round_keys[:4])

    for i in range(1, rounds):
        cipher.round_encrypt(square, cipher.round_keys[4 * i : 4 * (i + 1)])

    cipher.sub_bytes(square)
    cipher.shift_rows(square)
    cipher.add_round_key(square, cipher.round_keys[rounds*4:(rounds+1)*4])
    return revhex(hex(matrix2text(square))[2:-1].rjust(32, '0'))


class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		data = self.path[1:]
		self.wfile.write("plaintext: " + data + "\n")
		if data == "flag":
		  data = flag
		try:
		  encrypted = encrypt(master_key, data, 4)
		except:
		  encrypted = 'error'
		self.wfile.write("ciphertext: " + encrypted)
		
		
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
if __name__ == "__main__":
    server = ThreadedHTTPServer(('', PORT), myHandler)
    server.serve_forever()