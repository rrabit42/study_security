# Textbook-RSA write up  
댓글에서 CCA(Chosen Ciphertext Attack, 선택 암호문 공격)을 사용하라는 힌트를 얻고 이리저리 찾아봄  

## RSA 알고리즘에 대한 CCA 공격 원리  
[출처1](https://hororolol.tistory.com/473)  
[출처2](https://roytravel.tistory.com/113)  

<img width="761" alt="image" src="https://user-images.githubusercontent.com/46364778/205741480-6cd97e39-3f6a-4d5a-962f-000ae866b854.png">  
<img src="https://user-images.githubusercontent.com/46364778/205742796-06b08ab9-6699-4718-aab3-16e7e0a5337e.png">    

* 공격자가 ciphertext를 선택  
* 선택한 ciphertext에 대해서 private key를 가진 사람한테 decryption 요청~~(ex) 사용자가 핸드폰 잠시 두고 간 사이에 공격자가 몰래 Decryption 시도해보기ㅋㅋㅋ)~~  
* 그 결과 공격자는 {Ciphertext, Plaintext} 쌍을 얻게 됨  
* 공격자가 이전에 선택한 Ciphertext 이외의 것을 한 개라도 복원하면 공격자 승리  

## 익스코드  
나는 terminal에서 직접 입력하고, 결과를 파이썬 실행 사이트에 복붙하고 노가다해서 플래그를 획득했지만, 아래와 같이 코드를 짤 수 있다고 한다.  

```
from pwn import *
from Cypto.Util.number import bytes_to_lomg, inverse, long_to_bytes

context.log_level="DEBUG"

p = remote('host3.dreamhack.games', 9403)

p.sendlineafter('info\n', "3")
p.recvuntil("N: ")
n = int(p.recvline()[:-1])
p.recvuntil("e: ")
e = int(p.recvline()[:-1])
p.recvuntil("FLAG: ")
flag_enc = int(p.recvline()[:-1])

# log.info("N: " + str(n))
# log.info("e: " + str(e))
# log.info("FLAG: " + str(flag_enc))

exploit_flag = (pow(2, e) * flag_enc) % n

log.info("Exploit flag: " + str(exploit_flag))

p.sendlineafter("info\n", "2")
p.sendlineafter("(hex): ", hex(exploit_flag)[2:])

double_flag = int(p.recvline()[:-1])
flag = double_flag // 2

log.info("REAL FLAG: " + str(long_to_bytes(flag)))
```  

나의 노가다를 굳이 코드로 쓴다면 아래와 같을 듯(input 값으로 복붙할 수 있게)  
```
#!/usr/bin/python3
from Crypto.Util.number import bytes_to_long, inverse, long_to_bytes

N = int(input('N:'))
e = int(input('e:'))
flag_enc = int(input('flag_enc:'))
flag_enc프라임 = flag_enc*pow(2, e, N)%N
print('give this:', long_to_bytes(flag_enc프라임).hex())
print('flag:', long_to_bytes(int(input('give decrypt:'))*inverse(2, N)%N))
# 2로 나누는 것은 2의 역원을 곱하는 것이다.
```

## 출처  
* https://hackingisly.tistory.com/284  
* https://blog.naver.com/PostView.naver?blogId=apple8718&logNo=222256582723&categoryNo=0&parentCategoryNo=0&viewDate=&currentPage=79&postListTopCurrentPage=&from=postList&userTopListOpen=true&userTopListCount=5&userTopListManageOpen=false&userTopListCurrentPage=79  



