# Toddler's Bottle - input  
## 문제 설명  
```
Mom? how can I pass my input to a computer program?
```   
아래는 /home/input2/input.c 파일  
```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(int argc, char* argv[], char* envp[]){
        printf("Welcome to pwnable.kr\n");
        printf("Let's see if you know how to give input to program\n");
        printf("Just give me correct inputs then you will get the flag :)\n");

        // argv
        if(argc != 100) return 0;
        if(strcmp(argv['A'],"\x00")) return 0;
        if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
        printf("Stage 1 clear!\n");

        // stdio
        char buf[4];
        read(0, buf, 4);
        if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
        read(2, buf, 4);
        if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
        printf("Stage 2 clear!\n");

        // env
        if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
        printf("Stage 3 clear!\n");

        // file
        FILE* fp = fopen("\x0a", "r");
        if(!fp) return 0;
        if( fread(buf, 4, 1, fp)!=1 ) return 0;
        if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
        fclose(fp);
        printf("Stage 4 clear!\n");

        // network
        int sd, cd;
        struct sockaddr_in saddr, caddr;
        sd = socket(AF_INET, SOCK_STREAM, 0);
        if(sd == -1){
                printf("socket error, tell admin\n");
                return 0;
        }
        saddr.sin_family = AF_INET;
        saddr.sin_addr.s_addr = INADDR_ANY;
        saddr.sin_port = htons( atoi(argv['C']) );
        if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
                printf("bind error, use another port\n");
                return 1;
        }
        listen(sd, 1);
        int c = sizeof(struct sockaddr_in);
        cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
        if(cd < 0){
                printf("accept error, tell admin\n");
                return 0;
        }
        if( recv(cd, buf, 4, 0) != 4 ) return 0;
        if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
        printf("Stage 5 clear!\n");

        // here's your flag
        system("/bin/cat flag");
        return 0;
}
```  


## 문제 풀이  

0.  
늘 그렇듯 코드해석이 우선이다.  
총 5개의 stage를 clear하면 flag를 알 수 있다.  

**stage 1: argv**  
argc 즉, 인자의 개수는 100이어야 하고,  
argv['A']가 '\x00',  
argv['B']가 '\x20\x0a\x0d'이면 된다.  

**stage 2: stdio**  
표준입력(0)으로 buf에 4byte를 읽어온다.  
그리고 메모리 블럭을 비교하는데,  
buf와 '\x00\x0a\0x00\xff'가 같아야 하고,  
다시 표준에러(2)를 통해 buf에 4byte를 읽어온다.  
buf와 '\x00\x0a\x02\xff'가 같아야한다.  

**stage 3: env**  
\xde\xad\xbe\xef라는 환경변수에 \xca\xfe\xba\xbe 값을 넣어주면 된다.  

**stage 4: file**  
\x0a라는 파일을 파일포인터 fp를 이용해 read 모드로 연다.  
그리고 fp를 이용해 buf에 4byte 문자를 1개 읽어온다.  
buf에 읽어온 글자는 \x00\x00\x00\x00 이 4byte여야 한다.  

**stage 5: network**  
sd에 tcp 소켓 생성, 포트번호는 argv['C']값을 정수로 바꾼 값이다. (참고로 INADDR_ANY는 0.0.0.0주소로 모든 사용 가능한 주소로부터 기다리겠다는 뜻)  
(주소가 바인드가 안되면 return 1, 비정상적인 종료)  
그리고 sd에서 요청을 기다린다. 대기열 크기는 1이다.  
대기큐에 있는 소켓과 연결한다. 이때 그 소켓과 통신하는 파일 지정자 cd를 할당한다.  
cd를 통해 buf로 4byte를 받는다.  
buf와 \xde\xad\xbe\xef를 비교한다.  

----

1.  
요구사항이 많으므로 스크립트를 짜서 한번에 입력을 넣자.  
익스플로잇에 필요한 함수들이 pwntools에 다수 포진해 있으므로, python의 pwntools 모듈을 사용한다.~~나도 처음써본다~~  

```cd /tmp/input```  
```vi test.py```  
현재 위치에서는 코드를 작성할 수 없으므로 /tmp 폴더에서 작성해준다.  

```
from pwn import *

# stage 1  
argv_arr = [str(i) for i in range(100)]
argv_arr[ord('A')] = '\x00'
argv_arr[ord('B')] = '\x20\x0a\x0d'

# stage 2
with open('./stderr', 'a') as f:
  f.write('\x00\x0a\x02\xff')

# stage 3
envs = {'\xde\xad\xbe\xef':'\xca\xfe\xba\xbe'}

# stage 4
with open('./\x0a', 'a') as f:
  f.write('\x00\x00\x00\x00')

# stage 5
argv_arr[ord('C')]='22222'

# 이제 만들어준 값들을 적용한 프로세스를 input 실행파일에서 실행시킨다.
target = process(executable = '/home/input2/input', argv=argv_arr, stderr=open('./stderr'), env=envs)

# stage 2의 표준입력
target.sendline('\x00\x0a\x00\xff')

# stage 5의 메세지 전송(상대 소켓을 해줄 소켓을 만들고 메세지 보낸다)
conn = remote('localhost', 22222)
conn.send('\xde\xad\xbe\xef')
target.interactive()
```  
### 코드에 사용한 함수 정리  
* argvs를 i로 채우는데 i를 문자로 바꿔서 채움.  
* ord(): 특정 문자를 아스키값으로 변환하는 함수  
* python의 with 문법  
```
# 전
file_data = open('file.txt')
print(file_data.readline(), end="")
file_data.close()

# 후(close를 자동으로 해줌)
with open('file.txt) as file_data:
  print(file_data.readline(), end="")
```  

* open 함수에서 a: append모드, 파일 존재하지 않으면 새로 생성  
* process(executable='실행위치', argv='인자(리스트)', env='환경변수(딕셔너리)' 등): process 클래스의 인스턴스를 만드는 것으로 elf 파일을 실행시킬 수 있다.  
```r = process("파일이름")```을 실행하면 해당 프로그램을 실행시키고, 입력을 대기하게 된다.  
이후 실행된 프로그램에는 r 변수를 통해 접근할 수 있다.  

* process.send('str1') : scanf, read에 값을 전달할 때 \n 포함 없이 전달  
* process.sendline('str1') : gets에 값을 전달할 때 \n 포함해서 전달  
* interative(): 쉘과 직접적으로 명령을 전송, 수신할 수 있는 함수  

```
p = remote("localhost", 8888)
p.interative()
```  

---


2.  
pwntools은 파이썬의 모듈이다.  
리눅스에 설치를 해줘야하~지만 나는 putty로 해서 그런지 과정이 필요 없었다.  
/tmp/input에서  
```python test.py```하니까 아래와 같이 떴다! ㅎㅎ  
<img width="455" alt="2" src="https://user-images.githubusercontent.com/46364778/99767917-4679ec80-2b47-11eb-949a-cc83c6d8b61d.PNG">  

3.  
flag는 
Mommy! I learned how to pass various input in Linux :)  


## 의문점  
왜 if문장에서 return 0을 해주지.  
보통 그러면 main함수를 정상적으로 끝내기 위해서 return 0을 사용하는데  
이 문제는 return 0을 해도 main이 끝나지 않고 오히려 정상적으로 넘어간다. 
```if(!fp) return 0;``` fp가 할당이 안되어도(오류) return 0을 해주고,  
```if(strcmp(~~)) return 0;``` 문제에서 원하는 입력을 해줘도 return 0을 해줌..  
도대체 뭘까?  


