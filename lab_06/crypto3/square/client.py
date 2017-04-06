import requests

addr = "http://p4.team:8354/"

def encrypt_request(data):
   r = requests.get(addr+data)
   ciphertext = r.text.split()[3].decode('hex')
   assert len(ciphertext) == 16
   return ciphertext

def encrypt(s):
   assert len(s) == 16
   return encrypt_request(s.encode('hex'))
   
def get_encrypted_flag():
   return encrypt_request("flag")