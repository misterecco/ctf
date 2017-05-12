import zlib
import sys

filename = 'blobs/f82fa19781db698493bf7df07184a9bedfe6aaa3'  # HEAD hash
filename = 'blobs/4d1110f22e2cc3c0f930eb3ea736caefd9e248cf'  # HEAD blob
# filename = 'blobs/58b3535e60f755da0843a7d5ee6af09e9c572ba2'  # flag
# filename = 'blobs/88b98e3943a5248187af28a86de749658d655415'  # app.py
# filename = 'blobs/ea94abbf5f8fbcbd1f971c57e6dad66424cfad47'  # database.py
# filename = 'blobs/6f0e3043f0582badac085d40179f861d515d2bc4'  # forms.py
# filename = 'blobs/5d6847293ebf35bf1aa41e8bfc2c344d53a8101a'  # models.py
# filename = 'blobs/6e2765b8bda6bb5a784cd54b4dbec4c3aef6dc62'  # static
# filename = 'blobs/35523e4d87b3ff4d205761831659ca9101c15b77'  # templates
# filename = 'blobs/c6810ac3be9d55cf7a39f2dfb0940e2862ba7dfc'  # layout
# filename = 'blobs/3f8ef1da3a989073dc9581b3abc12d51d3684d0f'  # helpers
# filename = 'blobs/2c88b21ab4ad8c9ec2f2a1077ac3d980b17cda80'  # read_message
# filename = 'blobs/9511aa1a533c1ee9f08dcc56f00534d2a4b05c67'  # list_messages
# filename = 'blobs/097ddbac853ef82f4f517d1016b4cd76e3527613'  # parent hash
# filename = 'blobs/68b34be575783e64c64d95a8d51956c2424889b1'  # parent blob
# filename = '../.git/objects/de/b39c36c1470da0faf3cab3f102b1870d570be6'
compressed_contents = open(filename, 'rb').read()
decompressed_contents = zlib.decompress(compressed_contents)

# print(decompressed_contents)
print(decompressed_contents.decode('utf-8'))

flag = "X\xb3S^`\xf7U\xda\x08C\xa7\xd5\xeej\xf0\x9e\x9cW+\xa2"
app = "\x88\xb9\x8e9C\xa5$\x81\x87\xaf(\xa8m\xe7Ie\x8deT\x15"
db = "\xea\x94\xab\xbf_\x8f\xbc\xbd\x1f\x97\x1cW\xe6\xda\xd6d$\xcf\xadG"
forms = "o\x0e0C\xf0X+\xad\xac\x08]@\x17\x9f\x86\x1dQ]+\xc4"
models = ']hG)>\xbf5\xbf\x1a\xa4\x1e\x8b\xfc,4MS\xa8\x10\x1a'
stt = "n'e\xb8\xbd\xa6\xbbZxL\xd5KM\xbe\xc4\xc3\xae\xf6\xdcb"
templates = "5R>M\x87\xb3\xffM Wa\x83\x16Y\xca\x91\x01\xc1[w"
layout = "\xc6\x81\n\xc3\xbe\x9dU\xcfz9\xf2\xdf\xb0\x94\x0e(b\xba}\xfc"
helpers = "?\x8e\xf1\xda:\x98\x90s\xdc\x95\x81\xb3\xab\xc1-Q\xd3hM\x0f"
read_message = ",\x88\xb2\x1a\xb4\xad\x8c\x9e\xc2\xf2\xa1\x07z\xc3\xd9\x80\xb1|\xda\x80"
list_messages = "\x95\x11\xaa\x1aS<\x1e\xe9\xf0\x8d\xccV\xf0\x054\xd2\xa4\xb0\\g"


def to_hex_string(ch):
    res = "%x" % (ord(ch),)
    return res if len(res) % 2 == 0 else '0' + res

def to_hash(s):
    return "".join([to_hex_string(i) for i in s])

# print("flag hash: ", to_hash(flag))
# print("app.py hash: ", to_hash(app))
# print("database.py hash: ", to_hash(db))
# print("forms.py hash: ", to_hash(forms))
# print("models.py hash: ", to_hash(models))
# print("static hash: ", to_hash(stt))
# print("templates hash: ", to_hash(templates))
# print("layout hash: ", to_hash(layout))
# print("helpers hash: ", to_hash(helpers))
# print("read_message hash: ", to_hash(read_message))
# print("list_messages hash: ", to_hash(list_messages))
