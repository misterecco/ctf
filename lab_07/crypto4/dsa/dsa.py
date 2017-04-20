import hashlib
import random
from secrets import PRIVATE, SECRET

G = 0xe6a5905121b0fd7661e2eb06db9a4d96799165478a0b2baf09836c59ccf4f086bc2a55191ee4bf8b2324f6f53294da244342aba000f7b915861ba2167d09c5569910ae80990c3c79040879d8e16e48219127718d9ff05f71a905041564e9bcb55417b39cdb0b7afc6863ccd10b90ee42f856840e0dd5f8602e49592b58a22d39
P = 0xf2a4ca87978e05b112ef4a16b547c5036cd51fadac0cf967c152e56378c792a45e76e0ebfd62b2b23e94ca3727fbe1ebb308211cf8938c8a735db2de4cd26f0beb53b51fc2a5474bd0d466fc54fce13a4ec2b9840800ecdf337c55105c9b7d702b7f2d20bb3cba16a5948a208f8886ab2eddd1284a5b8ec457bf696be4bbb51b
Q = 0x9821a36da85bf3bcfb379d7cc39f5b6db7a553d5
PUBLIC = 0x5596b39949bab7979f8a679c11daad86ed59394ff4956769ec036d579ae6f80cd99bd12c442e10ee6aceed275739cb07417842d28d45f82b7a64d506c6f50f95622491a07c834260d64eb75bdaccdfdcf8ca4584f0c300403a4bed1ca515854b97732c8638118f71720c054f15d441f784a8c7b0c1a41dd07eb9acaaa7a7126e

def h(x):
  return int(hashlib.md5(x).hexdigest(), 16)

def rand():
   return h(SECRET + str(random.getrandbits(8)))
   
def egcd(a, b):
  if a == 0:
    return (b, 0, 1)
  else:
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
  g, x, y = egcd(a, m)
  if g != 1:
    raise Exception('modular inverse does not exist')
  else:
    return x % m

def sign(data):
  k = rand()
  r = pow(G, k, P) % Q
  s = (modinv(k, Q) * (h(data) + PRIVATE * r)) % Q
  return (r*Q + s)

def verify(data, sig):
  r = sig / Q
  s = sig % Q
  if r < 0 or s < 0 or r > Q:
    return False
  w = modinv(s, Q)
  u1 = (h(data) * w) % Q
  u2 = (r * w) % Q
  v = ((pow(G, u1, P) * pow(PUBLIC, u2, P)) % P) % Q
  return r == v