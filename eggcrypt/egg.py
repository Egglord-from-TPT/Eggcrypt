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
