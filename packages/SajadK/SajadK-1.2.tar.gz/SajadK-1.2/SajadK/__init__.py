import base64 as a,random as b
def x(d,k):
    r = bytearray()
    for i,j in enumerate(d):
        r.append(j ^ k[i % len(k)])
    return bytes(r)
def SajadEnc_HARD(f):
    with open(f,'r') as c:l = c.readlines()
    e = []
    for m in l:
        k = [b.randint(1,50) for _ in range(b.randint(20,60))]
        n = x(m.encode(),k)
        z = a.b64encode(n).decode()
        e.append((z,k))
        m = f'''from SajadK import SajadDec_HARD
een={e} 
exec(SajadDec_HARD((een)))'''
    return m
def SajadDec_HARD(e):
    d = []
    for s,k in e:
        u = a.b64decode(s)
        v = x(u,k)
        d.append(v.decode('utf-8'))
    return '\n'.join(d)