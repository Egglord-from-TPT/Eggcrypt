def encrypt(txt, key, rep=0):
    encoded=""
    for i, ch in enumerate(txt):
        b=ord(ch)^ord(key[i%len(key)])
        for digit in str(b):
            encoded+=f"{int(digit)+200:03d}"
    out=""
    for i in range(0, len(encoded),2):
        chunk=encoded[i:i+2]
        if len(chunk)==2:
            out+=chr(int(chunk))
        else:
            out+=chr(int(chunk)*10)
    if rep:
        return out
    return encrypt(out,key,1)
def decrypt(txt, key, rep=0):
    if rep==0:
        txt=decrypt(txt,key,1)
    encoded=""
    for ch in txt:
        n=ord(ch)
        if n<100:
            encoded+=f"{n//10}"
        else:
            encoded+=f"{n:02d}"
    digits=""
    for i in range(0,len(encoded),3):
        part=encoded[i:i+3]
        if len(part)==3:
            digits+=str(int(part)-200)
    values=[]
    temp=""
    for d in digits:
        temp+=d
        if int(temp)>31:
            values.append(int(temp))
            temp=""
    result=""
    for i, v in enumerate(values):
        result+=chr(v^ord(key[i%len(key)]))
    return result
def key():
    import time
    seed=1
    for i in range(int(time.time()*10000)%100):
            a=str(time.time()*10000)
            a=a[0:10]
            a=int(a)
            seed=int(seed*a+(round(seed^a)))
    return seed
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
