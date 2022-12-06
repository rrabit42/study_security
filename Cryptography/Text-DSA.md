# Text-DSA  
드림핵 DSA 문제 라업  

기본 원리는 EIGamal 전자 서명 공격과 같다. 다만 서명값 구하는 식이 - 에서 +로 변했으므로 그것만 주의해서 식 구해주면 된다.  

검증키(y, g, p, q), h는 해시 함수, 임의의 m1에 대한 서명값 (r1, s1), 임의의 m2에 대한 서명값 (r2, s2)에 대해  
DSA에서 고정된 k 값을 사용하면 s1-s2 했을 때 k 값을 구할 수 있게 된다. 왜냐하면 r1 = r2이기 때문   

편의상 m1 = h(m1), m2 = h(m2) ~~이걸 간과하고 그냥 메세지로 계산했더니 시간 오래걸림^^^ 메세지 m이 해시값이 된 메세지 m이란 것만 알았어도 더 빨리 풀었을 텐데~~  
k ≡ (m1 - m2)(s1 - s2)^-1 (mod q)  
x ≡ (ks - m)r^-1 (mod q)  

## 코드  
```
#!/usr/bin/python3
# pip install pycryptodome
# pip install pwntools
from pwn import *
from Crypto.Util.number import getPrime, inverse, bytes_to_long, isPrime
from random import randrange, choices
from hashlib import sha1
import string

# conn = remote('host3.dreamhack.games', 14784)
# conn.sendlineafter('Info\n', "3")
# conn.recvuntil("p = ")
# p = int(conn.recvline()[:-1])
# conn.recvuntil("q = ")
# q = int(conn.recvline()[:-1])
# conn.recvuntil("g = ")
# g = int(conn.recvline()[:-1])
# conn.recvuntil("y = ")
# y = int(conn.recvline()[:-1])
# bytes 로 받는데 int로 바꾸면 원래랑 숫자가 다름.. 왜지?
# 그리고 token은 이미 bytes 값인데 bytes로 또 감싸서 와서 어떻게 받는지 모르겠음


class DSA(object):
    def __init__(self, p, q, g, y):
        self.q = q
        self.p = p
        self.g = g
        self.y = y

    def sign(self, msg, k, x):
        r = pow(self.g, k, self.p) % self.q
        h = bytes_to_long(sha1(msg).digest())
        s = inverse(k, self.q) * (h + x * r) % self.q
        return (r, s)

    def verify(self, msg, sig):
        r, s = sig
        if s == 0:
            return False
        s_inv = inverse(s, self.q)
        h = bytes_to_long(sha1(msg).digest())
        e1 = h * s_inv % self.q
        e2 = r * s_inv % self.q
        r_ = pow(self.g, e1, self.p) * pow(self.y, e2,
                                           self.p) % self.p % self.q
        if r_ == r:
            return True
        else:
            return False

# 이렇게 해줘도 되고
# token = input("token: ")
# g = input("g: ")
# p = input("p: ")
# q = input("q: ")

# m1 = bytes.fromhex(input("first msg: "))
# r1, s1 = map(int, input("first sign: ").split(", "))

# m2 = bytes.fromhex(input("second msg: "))
# r2, s2 = map(int, input("second sign: ").split(", "))

# 복붙해줘도 
p = 1029550091302805930673379199424771464139519937622569469989774323331234972682071090184798181820687
q = 779153598807228531750347884740674975780552475653
g = 274771888580173876491262727682282988431265939857202726079607923900269459882861485732575839977766
y = 347804538058650103368021140798299755537313195536801943453350362561819558211970867611016363310191
token = b'7z6ogbH3IBfDB5GeRqNhtKPolAIzDEQf'

m1 = bytes.fromhex("0001")
r1, s1 = 374206065450677219009091168339402568554592631873, 61402709599680816402488157637690241581940226153

m2 = bytes.fromhex("0002")
r2, s2 = 374206065450677219009091168339402568554592631873, 658284244037568811382463639043553062719199211685

dsa = DSA(p, q, g, y)

# 우선 k 부터 구하기
h_m1 = bytes_to_long(sha1(m1).digest())
h_m2 = bytes_to_long(sha1(m2).digest())
k = inverse(s1 - s2, q) * (h_m1 - h_m2) % q

# x 구하기
x = inverse(r1, q) * (k * s1 - h_m1) % q

# k값 검증
k_p = inverse(x, q)
print(f"k: {k}")
print(f"k_p: {k_p}")
if k == k_p:
    print("correct k")
else:
    print("different k")
    exit(1)

# x값 검증
if dsa.sign(m1, k, x) == (r1, s1):
    print("correct x")
else:
    print("different x")

# token의 sign 구하기
print(f"token sign: {dsa.sign(token, k, x)}")
print("token hex: ", str(token.hex()))

```
