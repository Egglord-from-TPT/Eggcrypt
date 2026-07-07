def encrypt(txt,rep=0):
    a=[]
    b=""
    c=""
    for i in txt:
        b=ord(i)
        for j in str(b):
            c+=str(int(j)+200)
            if len(c)> 4:
                a.append(chr(int(c)))
                c=""
    txt=""
    for i in a:
        txt+=i
    if rep==1:
        return txt
    else:
        return encrypt(txt,1)
def decrypt(txt, rep=0):
    if rep==0:
        txt=decrypt(txt, 1)
    digits=""
    for ch in txt:
        num=ord(ch)
        digits+=str(num)
    result=""
    for i in range(0, len(digits), 3):
        chunk=digits[i:i+3]
        if len(chunk) ==3:
            original_digit=int(chunk)-200
            result += str(original_digit)
    final=""
    temp=""
    for d in result:
        temp+=d
        if int(temp)>31:
            final+=chr(int(temp))
            temp=""
    return final
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
    tot=sum(map(ord,key_str))%10000
    out=""
    for i in key_str:
        v=int(i,16)
        out+=str(v+((tot*v)%256))
    o=""
    for i in out:o+=chr((int(i)+tot)%256)
    out=""
    for i in range(len(o)-1):out+=ascii(i*tot+ord(o[i]))
    for n in map(int,[out[i:i+2] for i in range(0,len(out),2)]):o+=chr(n+32)
    if len(out)%2:o+=chr(int(out[-1])*21)
    o=o.lstrip("0123456789")
    h=0
    for c in o:h=(h*31+ord(c))&((1<<256)-1)
    chars="0123456789abcdefghijklmnopqrstuvwxyz"
    x=""
    while h:x=chars[h%36]+x;h//=36
    out=x.zfill(50)
    return out
