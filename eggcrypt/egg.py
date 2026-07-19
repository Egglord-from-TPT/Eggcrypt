from functools import lru_cache
def replace_non_255(text):
    return ''.join(c if ord(c)<=255 else '?' for c in text)
def hash2(txt):
    txt=str(txt)
    data=txt.encode()
    m=0xFFFFFFFFFFFFFFFF
    h=0x9E3779B97F4A7C15^len(data)
    i=0
    while i+8<=len(data):
        x=int.from_bytes(data[i:i+8],"little")
        h^=x*0x9E3779B185EBCA87&m
        h=((h<<31)|(h>>33))&m
        h*=0xC2B2AE3D27D4EB4F&m
        i+=8
    x=0
    for j,b in enumerate(data[i:]):
        x|=b<<(j*8)
    h^=x*0x165667B19E3779F9&m
    h^=h>>33
    h=h*0xFF51AFD7ED558CCD&m
    h^=h>>33
    h=h*0xC4CEB9FE1A85EC53&m
    h^=h>>33
    return str(h)
@lru_cache(maxsize=512)
def makesbox(key):
    prev=hash2(key)
    stream=[]
    while len(stream)<256:
        n=int(prev,36)
        for _ in range(50):
            stream.append(n&255)
            n>>=8
            if len(stream)>=256:
                break
        prev=hash2(prev)
    unused=list(range(256))
    sbox=[]
    for i in range(255,-1,-1):
        b=stream.pop()%(i+1)
        sbox.append(unused.pop(b))
    return sbox
def _to_bytes(data):
    if isinstance(data, bytes):
        return data
    elif isinstance(data, str):
        return data.encode('utf-8')
    elif isinstance(data, int):
        return str(data).encode('utf-8')
    else:
        return str(data).encode('utf-8')
def _xor_bytes(data, key):
    data=_to_bytes(data)
    key=_to_bytes(key)
    key_len=len(key)
    return bytes(data[i]^key[i%key_len] for i in range(len(data)))
def _diffuse_bytes(data):
    data=bytearray(_to_bytes(data))
    for i in range(1, len(data)):
        data[i]^=data[i-1]
    return bytes(data)
def _undiffuse_bytes(data):
    data=bytearray(_to_bytes(data))
    for i in range(len(data)-1, 0, -1):
        data[i]^=data[i-1]
    return bytes(data)
def _rol(x):
    return ((x<<1)|(x>>7))&0xff
def _diffuse2_bytes(data):
    data=bytearray(_to_bytes(data))
    for i in range(1, len(data)):
        data[i] ^= _rol(data[i-1])
    return bytes(data)
def _undiffuse2_bytes(data):
    data=bytearray(_to_bytes(data))
    for i in range(len(data)-1, 0, -1):
        data[i] ^= _rol(data[i-1])
    return bytes(data)
def _permute_bytes(data, perm):
    data=_to_bytes(data)
    return bytes(data[i] for i in perm)
def make_perm(n, key=7):
    perm=[]
    used=set()
    x=key&0x7fffffff
    for _ in range(n):
        x=(x*1103515245+12345)&0x7fffffff
        x=int.from_bytes(_xor_bytes(str(x),hash2(x*0x9E3779B185EBCA87)),"big")
        pos=x%n
        while pos in used:
            pos=(pos+1)%n
        used.add(pos)
        perm.append(pos)
    return perm
def inverse_perm(perm):
    inv=[0]*len(perm)
    for new_pos, old_pos in enumerate(perm):
        inv[old_pos]=new_pos
    return inv
def round_sbox(key, r):
    round_key=_xor_bytes(str(key), hash2(str(key)+str(r*0x9E3779B97F4A7C15)))
    return makesbox(round_key.decode('latin-1', errors='replace'))
@lru_cache(maxsize=512)
def roundkey(key, r):
    return int(hash2(str(key)+str(r*0x9E3779B97F4A7C15)), 36)
def encrypt(txt, key):
    data=_to_bytes(txt)
    for r in range(10):
        rk=roundkey(key, r)
        rk_bytes=str(rk).encode('utf-8')
        data=_xor_bytes(data, rk_bytes)
        sbox=round_sbox(key, r)
        data=bytes(sbox[b] for b in data)
        data=_diffuse2_bytes(data)
        data=_diffuse_bytes(data)
        perm=make_perm(len(data), roundkey(key, r))
        data=_permute_bytes(data, perm)
    for r in range(22):
        h=hash2(hash2(r)+hash2(key))
        data=_xor_bytes(data, h)
    data=_diffuse2_bytes(data)
    final_perm=make_perm(len(data), roundkey(key, 999))
    data=_permute_bytes(data, final_perm)
    return data.hex()
def decrypt(txt, key):
    data=bytes.fromhex(txt)
    final_perm=make_perm(len(data), roundkey(key, 999))
    data=_permute_bytes(data, inverse_perm(final_perm))
    data=_undiffuse2_bytes(data)
    for r in range(21, -1, -1):
        h=hash2(hash2(r)+hash2(key))
        data=_xor_bytes(data, h)
    for r in range(9, -1, -1):
        perm=make_perm(len(data), roundkey(key, r))
        data=_permute_bytes(data, inverse_perm(perm))
        data=_undiffuse_bytes(data)
        data=_undiffuse2_bytes(data)
        sbox=round_sbox(key, r)
        inv=[0]*256
        for i, v in enumerate(sbox):
            inv[v]=i
        data=bytes(inv[b] for b in data)
        rk=roundkey(key, r)
        rk_bytes=str(rk).encode('utf-8')
        data=_xor_bytes(data, rk_bytes)
    return data.decode('utf-8', errors='replace')
def key(seed=""):
    if seed=="":
        import time
        seed=int(str(seed).lstrip("-"))
        for i in range(int(time.time()*10000)%100):
                a=str(time.time()*10000)
                a=a[0:10]
                a=int(a)
                seed=int(seed*a+(round(seed^a)))
    return hash(hash2(seed))
def hash(inp):
    inp=str(inp)
    H=[0x243f6a8885a308d3,0x13198a2e03707344,0xa4093822299f31d0,0x082efa98ec4e6c89]
    for i,c in enumerate(inp):
       x=ord(c)+(i<<8)
       j=i%4
       H[j]^=x
       H[j]=(H[j]*0x100000001b3)&0xffffffffffffffff
       H[(j+1)%4]^=H[j]>>17
    key_str=''.join(f'{x:016x}' for x in H)
    tot=sum((i+1)*ord(c) for i,c in enumerate(key_str))
    for i in inp:
        tot^=ord(i)
    out=""
    for i in key_str:
        v=int(i,16)
        out+=str(v+((tot*v)%256))
    o=""
    for i in out:o+=chr((int(i)+tot)%256)
    out=""
    for i in range(len(o)-1):out+=str(i*tot+ord(o[i]))
    for n in map(int,[out[i:i+2] for i in range(0,len(out),2)]):o+=chr(n+32)
    if len(out)%2:o+=chr(int(out[-1])*21)
    o=o.lstrip("0123456789")
    h=0
    for c in o:
       h^=ord(c)
       h=((h<<13)|(h >> 243))&((1<<256)-1)
       h=(h*0x9e3779b97f4a7c15)&((1<<256)-1)
    chars="0123456789abcdefghijklmnopqrstuvwxyz"
    x=""
    while h:x=chars[h%36]+x;h//=36
    out=x.zfill(50)
    return out
