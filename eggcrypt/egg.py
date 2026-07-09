def encrypt(txt,key):
    data=""
    for i,ch in enumerate(txt):
        value=ord(ch)^ord(key[i%len(key)])
        data+=f"{value:03d}"
    return "".join(chr(int(data[i:i+3])) for i in range(0,len(data),3))
def decrypt(txt,key):
    data=""
    for ch in txt:
        data+=f"{ord(ch):03d}"
    result=""
    nums=[int(data[i:i+3]) for i in range(0,len(data),3)]
    for i,value in enumerate(nums):
        result+=chr(value^ord(key[i%len(key)]))
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
