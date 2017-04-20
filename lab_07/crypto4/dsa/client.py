import requests

addr = "http://p4.team:8365/"
#addr = "http://127.0.0.1:8365/"

def verify(data, sig):
   r = requests.get(addr+data.encode("hex")+","+str(sig).encode('hex'))
   return r.text


print verify("ala ma kota", 12345)
print verify("ala ma kota", 546570688445704835686674299184868202931941422783387917947819004038221479879741842072174377056055)