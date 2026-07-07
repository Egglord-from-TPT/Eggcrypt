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
def ehash(inp):
    inp=str(inp)
    tot=0
    for i in inp:
        tot+=ord(i)
    import time
    seed=1
    for i in range(int(time.time()*10000)%100):
    	a=str(time.time()*10000)
    	a=a[0:10]
    	a=int(a)
    	seed=int(seed*a+(round(seed^a)))
    key=seed
    out=""
    for i in str(key):
        out+=str(int(i)+((tot*int(i))%256))
    o=""
    for i in out:
        o+=ascii(int(i)+tot)
    out=""
    for i in range(len(o)-1):
        out+=ascii(i*tot+int(o[i]))
    for n in map(int,[out[i:i+2] for i in range(0,    len(out),2)]):o+=chr(n+32)
    if len(out)%2:o+=chr(int(out[-1])*21)
    o=o.lstrip("0123456789")
    h=0
    for c in o:h=(h*31+ord(c))&((1<<256)-1)
    chars="0123456789abcdefghijklmnopqrstuvwxyz"
    x=""
    while h:x=chars[h%36]+x;h//=36
    out=x.zfill(50)
    return out
