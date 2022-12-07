# SingleByteXor  
단일 바이트 xor 복호화 하기  
~~역시 해킹은 윈도우가 답인가.. 윈도우는 이미 xor 복호화 프로그램이 있더라..~~  

```
hint = "54586b6458754f7b215c7c75424f21634f744275517d6d"
hint = bytes.fromhex(hint)

for i in range(256):
    line = ''
    for j in hint:
        line += str(chr(i ^ j))
    if line[:2] == 'DH':  # flag 찾기
        print(line)
```
