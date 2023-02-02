# x86 Assembly  
기계어(Machine Code) <- (어셈블러; 통역사) <- 어셈블리 언어(Assembly Language)  
그 반대는 역어셈블러(Disassembler) 사용  

컴퓨터의 언어로 작성된 소프트웨어에서 취약점을 발견해야함  
어셈블리어만 이해할 수 있다면 역어셈블러를 사용하여 소프트웨어 분석 가능  

ISA(명령어 집합 구조) 만큼 많은 수의 어셈블리어가 존재.  

## x64 어셈블리 언어 기본 구조  
한국어: 주어, 목적어, 서술어 등으로 이뤄진 문법구조  
x64 어셈블리: 동사에 해당하는 **명령어(Operation Code, Opcode)**, 목적어에 해당하는 **피연산자(Operand)**  

### 명령어  
|의미|명령 코드|
|:---:|:---:|  
|데이터 이동(Data Transfer)| mov, lea |  
|산술 연산(Arithmetic)|inc, dec, add, sub|  
|논리 연산(Logical)|and, or, xor, not|  
|비교(Comparison)|cmp, test|  
|분기(Branch)|jmp, je, jg|  
|스택(Stack)|push, pop|  
|프로시져(Procedure)|call, ret, leave|  
|시스템 콜(System call)|syscall|  

* 데이터 이동: 어떤 값을 레지스터나 메모리에 옮기도록 지시  
<img width="640" alt="image" src="https://user-images.githubusercontent.com/46364778/216042383-036771ff-cae4-40df-8b46-483744683fb2.png">  

* 산술 연산: 덧셈, 뺄셈, 곱셈, 나눗셈 연산을 지시  
<img width="627" alt="image" src="https://user-images.githubusercontent.com/46364778/216212238-82f55d8b-c0b3-4382-9c1f-957d53bb04ac.png">  

* 논리 연산: and, or, xor, neg 등의 비트 연산을 지시. 비트 단위로 이뤄지는 연산들  
```and dst, src``` : dst와 src의 비트가 모두 1이면 1, 아니면 0  
```or dst, src``` : dst와 src의 비트 중 하나라도 1이면 1, 아니면 0  
```xor dst, src``` : dst와 src의 비트가 서로 다르면 1, 같으면 0  
```not op``` : op의 비트 전부 반전  

XOR 연산을 동일한 값으로 두 번 실행할 경우, 원래 값으로 돌아감 -> 이 성질 이용해 XOR cipher라는 단순 암호 개발됨  

* 비교 : 두 피연산자의 값을 비교하고, 플래그 설정  
```cmp op1, op2``` : 두 피연산자를 빼서 크기 비교, 연산의 결과를 op1에 대입하지는 않음. 0이 된다면 ZF 설정  
```test op1, op2``` : 두 피연산자에 AND 비트연산 취함. 연산의 결과는 op1에 대입하지 않음.  

* 분기 : rip를 이동시켜 실행 흐름을 바꿈  
```jmp addr``` : addr로 rip 이동시킴  
```je addr``` : 직전에 비교한 두 연산자가 같으면 점프(jump if equal)  
```jg addr``` : 직전에 비교한 두 연산자 중 전자가 더 크면 점프(jump if greater)  

* 스택  
```push val``` : val을 스택 최상단에 쌓음  
<img width="634" alt="image" src="https://user-images.githubusercontent.com/46364778/216272099-829beb89-5a4f-4004-9666-12a2e8ccd4dd.png">  
<img width="626" alt="image" src="https://user-images.githubusercontent.com/46364778/216272157-aeb37033-10af-4de4-9f24-17b95ea0b1fd.png">  
여기서 8은 8바이트=64비트  

* 프로시저 : 특정 기능을 수행하는 코드 조각  
반복되는 연산을 프로시저 호출로 대체 -> 전체 코드의 크기 줄일 수 있음.  
기능 별로 코드 조각에 이름을 붙일 수 있게 되어 코드의 가독성을 크게 높일 수 있음  

```호출(Call)``` : 프로시저를 부르는 행위  
```반환(Return)``` : 프로시저에서 돌아오는 것  

프로시저를 호출할 때는 프로시저를 실행하고 나서 원래의 실행 흐름으로 돌아와야 하므로,
**call 다음의 명령어 주소(return address, 반환 주소)를 스택에 저장하고 프로시저로 rip를 이동시킨다**  
x64 어셈블리어에는 프로시저 호출과 반환을 위한 call, leave, ret 명령어 있음  

```call addr``` : addr에 위치한 프로시저 호출  
```leave``` : 스택프레임 정리  
```ret``` : return address로 반환  
<img width="1308" alt="image" src="https://user-images.githubusercontent.com/46364778/216273361-3fad6638-1029-451c-8792-ab9ac5330b6e.png">
<img width="600" alt="image" src="https://user-images.githubusercontent.com/46364778/216274185-375a7fe8-725b-4391-9444-929b5b64b651.png">  

stack에서 | 기준 왼쪽은 주소, 오른쪽은 그 주소에 들어있는 값  

> 스택프레임?  
> 스택: 함수별로 자신의 지역변수 또는 연산과정에서 부차적으로 생겨나는 임시 값들을 저장하는 영역.  
> 함수 별로 서로가 사용하는 스택의 영역을 명확히 구분하기 위해 스택 프레임 사용  
> 우분투 18.04에서 함수는 호출될 때 자신의 스택프레임을 만들고, 반환할 때 이를 정리  

* 시스템 콜  
하단에 따로 설명  

### 피연산자  
3가지 종류  
* 상수(Immediate Value)  
* 레지스터(Register)  
* 메모리(Memory); []으로 둘러싸인 것으로 표현, 앞에 크기 지정자(Size Directive) TYPE PTR이 추가될 수 있음(ex. BYTE, WORD, DWORD, QWORD; 각각 1,2,4,8 바이트)  

|메모리 피연산자|설명|  
|:---:|:---:|  
|QWORD PTR [0x8048000]|0x8048000의 데이터를 8바이트만큼 참조|  
|DWORD PTR [0x8048000]|0x8048000의 데이터를 4바이트만큼 참조|  
|WORD PTR [rax]|rax가 가르키는 주소에서 데이터를 2바이트 만큼 참조|  

> 자료형 WORD의 크기가 2바이트인 이유  
> 초기 IA-16 아키텍처대로 WORD 자료형의 크기를 16비트로 유지. 크기 변경하면 기존의 프로그램들이 새로운 아키텍처와 호환되지 않을 수 있기 떄문  
> 대신 새로 DWORD, QWORD 자료형 추가로 만듦  


### 시스템 콜  
운영체제는 연결된 모든 하드웨어 및 소프트웨어에 접근, 제어 가능  
해킹으로부터 이 막강한 권한을 보호하기 위해 커널 모드, 유저 모드로 권한 나눔  

> 유저모드에서 커널 모드의 시스템 소프트웨어에게 어떤 동작을 요청하기 위해 사용됨

소프트웨어 대부분은 커널의 도움 필요  
ex) . 예를 들어, 사용자가 cat flag를 실행하면, cat은 flag라는 파일을 읽어서 사용자의 화면에 출력해 줘야 합니다.  
그런데 flag는 파일 시스템에 존재하므로 이를 읽으려면 파일시스템에 접근할 수 있어야 합니다.   
유저 모드에서는 이를 직접 할 수 없으므로 커널이 도움을 줘야 합니다.  
여기서, 도움이 필요하다는 요청을 시스템 콜이라고 합니다.  
유저 모드의 소프트웨어가 필요한 도움을 요청하면, 커널이 요청한 동작을 수행하여 유저에게 결과를 반환합니다.  

x64 아키텍처에서는 시스템 콜을 위해 ```syscall``` 명령어 있음  

#### 커널 모드  
운영체제가 전체 시스템을 제어하기 위해 시스템 소프트웨어에 부여하는 권한  
ex) 파일 시스템, 입력/출력, 네트워크 통신, 메모리 관리 등 모든 저수준 작업은 사용자 모르게 커널모드에서 진행  
시스템의 모든 부분을 제어할 수 있음 -> 해커가 커널 모드까지 진입하게 되면 시스템은 거의 무방비 상태  

#### 유저 모드  
운영체제가 사용자에게 부여하는 권한  
ex) 브라우저, 유튜브, 게임, 프로그래밍 등, 리눅스에서 루트권한으로 사용자를 추가하고, 패키지를 내려 받는 행위  
유저모드에서는 해킹이 발생해도 권한 제한적  

<img width="611" alt="image" src="https://user-images.githubusercontent.com/46364778/216276442-f6b2d0b5-d4d7-415e-851b-16ba37e9ae80.png">  

#### syscall  
시스템 콜은 함수. 필요한 기능과 인자에 대한 정보를 레지스터로 전달 -> 커널이 이를 읽어서 요청 처리  
리눅스, x64 아키텍처 -> rax로 무슨 요청인지 나타내고, 아래의 순서대로 필요한 인자 전달  

<img width="605" alt="image" src="https://user-images.githubusercontent.com/46364778/216276873-da670b36-ace6-40eb-8b2b-69f7e2a8312a.png">  

#### x64 syscall 테이블  
검색해서 찾기  
중요한 몇가지만  
<img width="645" alt="image" src="https://user-images.githubusercontent.com/46364778/216277111-c43f33b8-42a0-4fc9-ad8c-c70da43d653c.png">  


---

Quiz: x86 Assembly 1 풀이  
<img width="600" alt="image" src="https://user-images.githubusercontent.com/46364778/216285902-cc77a902-86f3-4402-bc88-35f01071fed3.png">  

* Byte 만 불러오므로 rcx = 0x00일 때는 dl = 0x67  
* rcx = 0x01 일 때는 dl = 0x55 (0x400000 + rcx = 0x400001) 이므로  
* rcx가 0x19보다 커질때까지 반복되므로 0x20 = 32가 될때까지, 즉 0x30을 32개 바이트에 xor 하면 된다 -> memory에 있는 모든 바이트에서 0x30 xor하기  

```
memory = [
    '0x67', '0x55', '0x5c', '0x53', '0x5f', '0x5d', '0x55', '0x10', '0x44', '0x5f', '0x10', '0x51',
    '0x43', '0x43', '0x55', '0x5d', '0x52', '0x5c', '0x49', '0x10', '0x47', '0x5f', '0x42', '0x5c',
    '0x54', '0x11', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'
]
xor = '0x30'
result = ''

for m in memory:
  hex = int(m,16) ^ int(xor,16)
  # print(hex)
  w = chr(hex)
  # print(w)
  result += w

print(result)
```  

Quiz: x86 Assembly 2 풀이  
