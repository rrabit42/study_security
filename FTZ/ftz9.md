# FTZ 9  
## 문제 설명  
```
다음은 /usr/bin/bof의 소스이다.

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

main(){

  char buf2[10];
  char buf[10];

  printf("It can be overflow : ");
  fgets(buf,40,stdin);

  if ( strncmp(buf2, "go", 2) == 0 )
   {
        printf("Good Skill!\n");
        setreuid( 3010, 3010 );
        system("/bin/bash");
   }

}

이를 이용하여 level10의 권한을 얻어라.
```  

BOF 기초 문제다. buf에는 10 byte만 할당되어 있는데 fgets함수에서 40byte나 할당 해준다.  
이를 통해 buf2에도 접근 가능해 if문을 통과할 수 있을 것 같다.  

## 문제 풀이  
### 풀이 과정  

1. 우선 스택 구조를 대충 파악해보자.  

|ret[4]|  
|:---:|
|sfp [4]|  
|buf2 [10]|  
|buf [10]|  

2. fgets() 함수를 이용해 buf를 채울 때 buf2 처음에 "go"가 들어가도록 채우면 된다.  
따라서 먼저 이렇게 입력을 해보았다.  
```/usr/bin/bof```  
```AAAAAAAAAAgo```  

3. if문이 실행되지 않는다. buf와 buf2 사이에 dummy값이 존재해서 그런 것 같다.  
gdb로 분석해서 dummy값을 알아낼 수도 있지만,  
> ```cp ./hint ./tmp/code.c```  
> ```gcc -o /tmp/code /tmp/code.c```  
> [ebp-40]에서 문자열 입력을 받고, [ebp-24]에서 문자열 비교를 한다.  
> 따라서 [ebp-40]은 buf의 위치, [ebp-24]는 buf2의 위치이므로, 둘 사이는 16byte 거리가 있고, buf가 10byte 공간을 차지하므로 dummy는 6byte.  

충분히 추측할 수 있다.  
메모리에 공간을 할당할 때 Full Word Boundary에 맞춰 16의 배수로 할당이 되므로, buf[10]과 buf2[10]은 16byte가 할당이 되었을 것이다. 그렇다면 사용하지 않는 6byte의 공간이 존재하므로, buf와 buf2 사이에는 6byte의 dummy가 존재하게 된다.  

4. 따라서 ```AAAAAAAAAABBBBBBgo``` 입력! 그럼 level10의 쉘이 내려오고, ```my-pass``` 명령어을 통해 비밀번호를 알 수 있다.  
* interesting to hack!  

---

### GDB 이용해서 해석하기  
[출처](https://blog.dork94.com/96)  

```gdb code```  
```set disassembly-flavor intel```  
```disas main```  

<img width="338" alt="a" src="https://user-images.githubusercontent.com/46364778/92610758-07cbe880-f2f3-11ea-9a1c-43e4721dfa84.PNG">  

* fgets 함수 호출 전에 스택에 [ebp-40] 위치 값을 eax에 불러오고 이를 push를 이용해 스택에 저장한다.(함수에 인자로 전달하기 위해)  
* strncmp 함수 호출 전에 스택에 [ebp-24]위치 값을 eax에 불러오고 이를 push를 이용해 스택에 저장한다.(함수에 인자로 전달하기 위해)  
* 참고로 main+60의 push 0x804856a는 go가 저장되어 있는 위치로 보인다.  
<img width="196" alt="ㅠ" src="https://user-images.githubusercontent.com/46364778/92611837-2bdbf980-f2f4-11ea-8229-20ad4663c2d6.PNG">  

**스택에 함수의 인자를 전달할 때는 소스코드에서 전달하는 인자의 역순으로 전달한다.**  

어쨌든 [ebp-40] 위치에 있는 것은 fgets() 인자로 들어가는 buf고,  
[ebp-24] 위치에 있는 것은 strncmp() 인자로 들어가는 buf2다.  

따라서 buf와 buf2 사이에 16byte가 존재함을 알 수 있다.  


## 연관된 정보들  
* 메모리구조  
<img width="170" alt="g" src="https://user-images.githubusercontent.com/46364778/92572675-b5250900-f2bf-11ea-8b77-ad0f68560871.PNG">  

따라서 높은 주소에 buf2가 할당되고, 그 아래에 buf가 할당됨.  
그리고 buf에 값을 입력해서 넘치게 된다면 아래부터 buf가 차곡차곡 채워져서 위로 넘치게 되는 것이다!  
**메모리의 번지가 낮은 쪽부터 채우기 때문!**  

|dummy [6]|  
|:---:|
|buf2 [10]|  
|dummy [6]|  
|buf [10]|  

* int strcmp(const char* str, const char* str2)  
str1, str2: 비교할 문자열

* int strncmp(const char* str1, const char* str2, size_t n);  
str1, str: 비교할 문자열  
n: 비교할 문자열 길이(만약 음수를 넣으면 unsigned int 타입에서 언더플로우가 일어나기 때문에 최대값이 들어가므로 매개변수로 들어온 문자열을 끝까지 비교하게 된다.)  
[출처](https://blockdmask.tistory.com/391)  

* word  
컴퓨터는 32bits, 64bits가 있으며,  
32bit 컴퓨터인 경우 1word=32bit 즉 4byte가 되고,  
64bit 컴퓨터인 경우 1word=64bit 즉 8byte가 된다.  

* 컴퓨터가 한번에 처리할 수 있는 명령 크기  
Half word: 2byte  
Full word: 4byte  
Doulbe word: 8byte  

### gdb 명령어  
[출처](https://movefast.tistory.com/102)  
```x/[개수][표시형식][단위크기] <주소/함수이름>```  
지정된 위치의 메모리데이터를 지정된 형식으로 출력  

* 표시형식: d, o, x, t, f, s, i 등  
* 단위 크기: b, h, w, g  

ex)  
x/x <주소> : <해당 주소>의 내용물을 바이트 단위로 출력  
x/10x: opcode 10개 출력  
x/10i : 명령어 10개 출력  
x/10s : 문자열 10개 출력  
x/10wx : word단위로 10개 출력  
x/s, x/i, ... etc  


ex)  
mov $eax, [0xbfffefc4] : 대괄호는 포인터를 의미  
- 대괄호 없이 0xbfffefc4일 경우 그 주소의 내용이다.  
- 포인터는 그 주소에 저장된 포인터주소가 참조하는 주소의 내용물을 저장하는 것.  
- '*'기호 사용 : x/s *0xbfffefc4 처럼 한단계 더 보아야함  

ex)  
레지스터도 포인터처럼 사용해서 내용물을 볼 수 있다.  
- x/s $eax : eax에 저장된 내용(주소일수도있음)  
- x/s *$eax : eax에 저장된 포인터가 가리키는 내용  



