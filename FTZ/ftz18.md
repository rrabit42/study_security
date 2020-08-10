# FTZ 18  
## 문제 설명  

* 이 문제를 정확히 이해하려면 네트워크 소켓프로그래밍에서 사용되는 다중입출력에 관한 함수들 공부를 해야한다!  

```
#include <stdio.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
void shellout(void);

int main()
{
  char string[100];
  int check;
  int x = 0;
  int count = 0;
  fd_set fds;
  
  printf("Enter your command: ");
  # 출력 버퍼 비우기
  fflush(stdout);
  
  while(1)
    {
      if(count >= 100)
        printf("what are you trying to do?\n");
      if(check == 0xdeadbeef)
        shellout();
        
      # check이 0xdeadbeef가 아닐 경우
      else
        {
          FD_ZERO(&fds);
          FD_SET(STDIN_FILENO,&fds);
           # 지금 표준 입력만 set되어 있고, 읽을 수 있는 상태이므로 I/O가 가능한 개수인 1이 리턴될 것이다. 즉, if I/O가 가능한 fd가 있는지 확인
          if(select(FD_SETSIZE, &fds, NULL, NULL, NULL) >= 1)
            {
              # fileno(stdin)==1이므로 fds의 index 1에 fd가 set되어 있는지!
              if(FD_ISSET(fileno(stdin),&fds))
                {
                  # stdin에서 1byte를 읽어온다
                  read(fileno(stdin),&x,1);
                  switch(x)
                    {
                      case '\r':            # \r, \n 입력시 비프음 \a 출력
                      case '\n':
                        printf("\a");
                        break;
                      case 0x08:            # 0x08 입력이 들어오면 count 값 1감소, 문자를 지운다. count가 인덱스로 문자를 저장하는데 사용되기 때문.
                        count--;
                        printf("\b \b");
                        break;
                      default:              # 그 외는 모두 일반 문자처럼 string 버퍼에 저장
                        string[count] = x;
                        count++;
                        break;
                    }
                }
            }
        }
    }
}

void shellout(void)
{
  setreuid(3099,3099);                      # level19 ruid, euid 설정
  execl("/bin/sh","sh",NULL);               # 쉘 실행
}
```  

### fd_set 구조체  

fd_set 구조체는 File Descriptor(이하 FD)를 저장하는 구조체이다.  
> fd_set은 여러개의 fd(file descriptor)를 select 함수에서 읽기/쓰기/오류에 대한 event발생 여부 체크 모록을 관리하고 select 실행후에 event가 발생한 fd인지 여부를 기록하는 구조체
안에 내용을 보면 그냥 배열로 여기면 편하다.  
1024bits = 128byte 크기를 가지는 비트배열이다.  

구조체 내용은 OS마다 조금씩 다른 듯 하다.  

> fd_set 구조체에 2와 5의 FD 를 저장한다고 하면,  
> 두번째 비트와 다섯번째 비트가 1로 변경된다.  
> 값 저장은 FD_SET 매크로를 쓴다.  
```
fd_set testFds ;
FD_SET(2, &testFds) ;
FD_SET(5, &testFds) ;
```  
> 위 testFds 구조체의 배열값을 출력해 보면,  
> 0 1 0 0 1 0 0 0 0 ~~~  
> 위와 같이 2번째와 5번째 비트가 1 로 세팅된다.  


### fflush() 함수

int fflush ( FILE *fp); 파일 스트림 버퍼를 비우는 함수  
반환값: 성공 시 0, 에러 시 EOF  
**출력 스트림 버퍼**에 남아있는 내용을 출력 스트림에 출력하는 동작을 수행한다. 하지만 입력 스트림에서 어떻게 동작해야 하는지는 표준 문서에서 정의하지 않고 있다.  
입력버퍼를 비우고 싶을 때는 fflush 함수를 사용하는게 아니라,  
입력버퍼를 읽어들이고 출력을 하지 않으면 된다!  

* execl  
```
execl("/bin/ls", "ls", "-a", 0)
```  

> /bin/ls 경로에 있는 ls -a 라는 명령어를 실행한다는 뜻이다.  
> 뒤에 0(null)은 인자의 끝을 의미한다.  

따라서 문제에서 ```execl("/bin/sh","sh",NULL);``` 는  
/bin/sh 경로에 있는 sh 명령어를 실행한다는 의미이다.  

### FD_ZERO() 함수  

구조체를 초기화 해주는 함수다.  
언급했듯이 fd_set 구조체의 주요 변수는 배열이다.  
fd_set testFds; 와 같이 선언만 하고 안에 배열값을 찍어보면 쓰레기값이 있을 수 있기에 초기화는 항상 필수다.  

### FD_SET() 함수  

FD_SET은 fd_set에 fd를 추가한다.  
```void FD_SET(int fd, fd_set *set);```  

**파라미터**  

> fd
> - set에 추가할 file descriptor  

> set
> - fd를 추가할 fd_set  
> - read용/write용/예외용에 대한 set이 있으며, 각각의 set에 fd를 추가할 수 있다.  


### STDIN_FILENO  

프로그램이 프로세스로 메모리에서 실행을 시작 할 때, 기본적으로 할당되는 파일 디스크립터들이 있다.  
바로 표준 입력(Standard Input), 표준 출력(Standard Output), 표준 에러(Standard Error)이다.  
이들에게 각각 0, 1, 2 라는 정수가 할당되며, POSIX 표준에서는 STDIN_FILENO, STDOUT_FILENO, STDERR_FILENO로 참조된다.  
이 매크로는 <unistd.h> 헤더 파일에서 찾아 볼 수 있다.  
0이 아닌 정수로 표현되는 파일 디스크립터는 0 ~ OPEN_MAX 까지의 값을 가질 수 있으며, OPEN_MAX 값은 플랫폼에 따라 다르다.  

### select() 함수  

```int select(int nfds, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);```  
select함수는 socket / pipe 등에서 동시에 여러개의 I/O를 대기할 경우에 특정한 fd에 blocking되지 않고 I/O를 할 수 있는 상태인 지를 모니터링하는 함수다.  
이를 통하여 I/O 가능한 fd이면, I/O 함수를 호출하면 된다.  

**파라미터**  

> nfds  
> -  FD_SET()함수로 설정한 fd값들 중에서 가장 큰 fd값 + 1을 설정해야 합니다.  

> readfds  
> - FD_SET(fd, readfds)로 설정한 fd들이 데이터를 읽을 수 있는 상태일 때까지 대기하게 하고,  
> select 함수가 return된 후에는 readfds에 읽을 수 있는 상태에 있는 fd를 제외하고  
> 모두 clear됩니다.  
> - FD_ISSET(fd, readfds)으로 읽을 수 있는 상태에 있는 fd인지를 확인하여  
> 0이 아닌값이 return되면 읽을 수 있는 상태에 있는 fd입니다.  

> writefds  
> - FD_SET(fd, writefds)로 설정한 fd들이 데이터를 쓸 수 있는 상태일 때까지 대기하게 하고,  
> select 함수가 return된 후에는 writefds에 쓸 수 있는 상태에 있는 fd를 제외하고  
> 모두 clear됩니다.  

> - FD_ISSET(fd, writefds)으로 쓸 수 있는 상태에 있는 fd인지를 확인하여  
> 0이 아닌값이 return되면 쓸 수 있는 상태에 있는 fd입니다.  

> exceptfds  
> - FD_SET(fd, exceptfds)로 설정한 fd들이 오류 상태일 때까지 대기하게 하고,  
> select 함수가 return된 후에는 오류상태가 아닌 fd들은 exceptfds에서 모두 clear됩니다.  
> - FD_ISSET(fd, exceptfds)으로 오류 상태에 있는 fd인지를 확인하여 0이 아닌값이 return되면 오류 상태인 fd입니다.  

> timeout
> - readfds, writefds, exceptfds 들이 timeout 시간동안 모두 상태변화가 없으면 select함수를 종료시킵니다.  
> - timeout이 NULL이면 timeout이 없이 계속 대기합니다.  
> - struct timeval은 sys/time.h에 선언되어 있으며, 마이크로초 단위의 timeout을 설정을 지원합니다.  
```
struct timeval {
  long    tv_sec;         /* seconds */
  long    tv_usec;        /* microseconds */
};
```
> timeout의 구조체는 const가 아니므로 내부적으로 소요된 시간만큼 count down되며,  
> timeout 시간이 지나면 tv_sec, tv_usec 이 각각 0이 됩니다.  
> 만약 timeout이 되기전에 select가 return 되었다면 소요된 시간 만큼 차감되어 tv_sec, tv_usec에 저장됩니다.  

**반환값**  

> 0보다 큼  
> - readfds, writefds, exceptfds에 대한 처리가능 상태인 fd의 전체 건수를 return 합니다.  

> 0
> - timeout이 발생하였으며, 처리 가능 상태인 fd가 하나도 없습니다.  

> -1
> - 오류가 발생하였으며, 상세한 오류 내용은 errno에 저장됩니다.  

> EBADF : 설정된 fd 중에서 유효하지 않은 fd가 있음. (한개라도 있으면)  
> EINTR : signal이 catch되어 select()가 중단됨  
> EINVAL : nfds 가 -값이거나 timeout의 tv_sec, tv_usec값이 잘못 설정됨.  
> ENOMEM : 처리를 위한 내부 메모리 할당이 실패함.  

## FD_SETSIZE  

*정확히는 __FD_SET_SIZE라는 이름으로 시스템에 정의되어있는 것 같다.*  
__FD_SET_SIZE는 #define을 이용해서 1024을 치환한 상수 값이다.  

## fileno() 함수  
```
#include <stdio.h>
int fileno(FILE *stream);
```
FILE *에는 실제로 system call I/O를 위한 file descriptor가 할당되어 있습니다. 이 fd값을 얻는 함수입니다.  
그러나 system call I/O 함수랑 Stream함수를 혼용하여 사용하면 예기치 못한 오류가 발생할 수 있습니다. 부득이하게 fd를 사용해야 한다면, 쓰기용 stream의 경우 fflush(3)를 먼저하고 fd로 작업을 하는 것이 좋습니다. stream을 통해서 할 수 없는 기능에 대해서만 fd를 얻어서 처리하도록 해야 합니다.

**파라미터**  

> stream
> - fd를 얻을 stream 변수  

**반환값**  

> 0  
> - 정상적으로 fd값을 반환하으며, 반환된 값이 fd입니다.  

> -1  
> - 오류가 발생하였으며, 상세한 오류 내용은 errno에 저장됩니다.  

> EBADF : 주어진 stream이 유효하지 않습니다.  

### FD_ISSET() 함수  
```void FD_ISSET(int fd, fd_set *set);```  
fd_set은 여러개의 fd(file descriptor)를 select 함수에서 읽기/쓰기/오류에 대한 event발생 여부 체크 모록을 관리하고 select 함수 실행후에는 event가 발생한 fd인지 여부를 기록하는 구조체입니다.  
fd_isset함수는 fd_set에 fd가 포함되어 있는 지를 확인하는 함수입니다.  
select 함수가 호출된 후에는 처리가 가능한 fd만 남게되므로 읽기 또는 쓰기 준비가 되어 있는 지 여부를 알 수 있습니다.  

**파라미터**  

> fd  
> - set에 존재하는지 알고 싶은 file descriptor  

> set  
> - 읽기/쓰기/오류에 대한 모니터링을 할 fd 목록을 관리하는 구조체  
 
**반환값**  

> 0
> - fd가 set에 설정되지 않았습니다.  
> select 함수 호출 후 FD_ISSET 호출한 경우이며 처리할 수 있는 상태가 아닙니다.  

> 0이 아님
> - fd가 set에 설정되어 있습니다.  
> - select 함수 호출 후 FD_ISSET 함수를 호출한 경우이면 처리할 수 있는 상태입니다.  

### read() 함수  
```
#include <unistd.h>
ssize_t read (int fd, void *buf, size_t len)
```

**파라미터**  

> int fd  
> open() 시스템 콜로 열린 파일을 가리키는 파일 지정 번호  

> void* buf  
> 파일에서 읽은 데이터를 저장할 메모리 공간  

> len  
> 읽을 데이터의 크기(Byte 단위)  

**반환값**  

> ssize_t  
> 파일 읽기 성공 : 0 보다 큰 수  
> 읽을 데이터 없을 시 : 0 (EOF : End Of File 파일의 끝을 만났을 때)  

## 문제 풀이  

1. 대략적인 스택 구조를 놓고 생각해보자.  

|string [100]|
|:---:|
|check [4]|
|x=0 [4]|
|count=0 [4]|
|fds [128]|

목표는 check에 0xdeadbeef 값을 넣어 shellout() 함수를 실행시키는 것이다.  
하지만 string[100]보다 check 변수가 뒤에 존재해 일반적인 BOF로는 문제를 해결하기 힘들다.  

버퍼의 문자수를 조절해주는 count 변수가 0x08 입력이 들어오면 1 감소한다는 점을 이용하자.  
배열의 인덱스가 -가 되도록 하면 앞의 메모리에 접근이 가능하다!  
string[100] 뒤에 존재하는 check 변수에 접근이 가능하다는 것이다. [Out-of-boundary](https://github.com/rrabit42/study_security/blob/master/SystemHacking/2.Memory%20Corruption%20-%20C%20(1).md)  

* string[100]에서 check까지 거리를 확인하여 그만큼 0x08 변수를 입력하여 인덱스를 -로 이동시켜 string뒤에 있는 check에 0xdeadbeef를 덮어 씌우자! => 정확한 스택구조 파악이 관건  

2. gdb를 이용해 attackme를 분석해보자.  
<img width="316" alt="1" src="https://user-images.githubusercontent.com/46364778/89817408-0b007700-db83-11ea-96eb-b7a881fd728b.PNG">  
<img width="302" alt="2" src="https://user-images.githubusercontent.com/46364778/89817407-0a67e080-db83-11ea-88d6-1dea9daa1bc0.PNG">  
<img width="314" alt="3" src="https://user-images.githubusercontent.com/46364778/89817406-0a67e080-db83-11ea-857c-796eac5bc640.PNG">  
<img width="314" alt="4" src="https://user-images.githubusercontent.com/46364778/89817400-0936b380-db83-11ea-9815-7ca54a5aee27.PNG">

~~ㅎ..어차피 표준입력 받는건데 왜 저렇게 소켓프로그래밍으로 꼬았을까 이해가 안갔는데 어셈블리 복잡하게 하려는 속셈이었니..~~  



## 그외  

### exec 계열의 함수  
[출처](https://bbolmin.tistory.com/35)  

![1](https://user-images.githubusercontent.com/46364778/89810897-c2dc5700-db78-11ea-8e6f-8e12e3940a45.jpg)  

exec 뒤에 붙은 문자에 따라 분류해보자.  

* l, v : argv인자를 넘겨줄 때 사용합니다. (l일 경우는 char *로 하나씩 v일 경우에는 char *[]로 배열로 한번에 넘겨줌)  
* e : 환경변수를 넘겨줄 때 사용합니다. (e는 위에서 v와 같이 char *[]로 배열로 넘겨줍니다.)  
* p : p가 있는 경우에는 환경변수 PATH를 참조하기 때문에 절대경로를 입력하지 않아도 됩니다. (위에서 system함수 처럼)  

### I/O 통지모델의 할아버지 select  
[출처](https://ozt88.tistory.com/21)  

select는 싱글쓰레드로 다중 I/O를 처리하는 멀티플렉싱 통지모델의 가장 대표적인 방법이다. 해당 파일 디스크립터가 I/O를 할 준비가 되었는지 알 수 있다면, 그 파일 디스크립터가 할당받은 커널Buffer에 데이터를 복사해주기만 하면된다. 이런 목적하에 통지모델은 파일디스크립터의 상황을 파악할 수 있게 하는 기능을 할 수 있어야한다. select는 많은 파일 디스크립터들을 한꺼번에 관찰하는 FD_SET 구조체를 사용하여 빠르고 간편하게 유저에게 파일 디스크립터의 상황을 알려준다.  

* FD_SET  

FD_SET은 하나의 FD(파일 디스크립터)의 상태를 하나의 비트로 표현한다. 파일 디스크립터의 번호는 고유하기 때문에, 파일 디스크립터의 번호를 인덱스로하여 해당 비트가 어떤 값을 가지고 있느냐에 따라서 준비상황을 통지 받을 수 있는 것이다. 먼저 파일 디스크립터의 번호를 FD_SET에 등록하면 해당 비트의 값이 1로 저장된다. 그리고 I/O처리 준비가 되면 SELECT를 통해 해당 비트의 값을 갱신하고 프로세스는 변경된 값을 보고 커널 버퍼에 데이터를 복사하면 되는 것이다. 귀찮은 비트연산을 단순화하여 다음의 메크로를 제공한다.  

```
FD_ZERO(fd_set* set);        //fdset을초기화
FD_SET(int fd, fd_set* set);  //fd를 set에 등록
FD_CLR(int fd, fd_set* set);  //fd를 set에서 삭제
FD_ISSET(int fd, fd_set* set);//fd가 준비되었는지 확인
```  

* select  

select는 read/ write/ error 3가지 I/O에 대한 통지를 받는다. 또한 select에 timeout을 설정하여 대기시간을 설정할 수 있다. signature 는 다음과 같다.  

```
int select( int maxfdNum, //파일 디스크립터의 관찰 범위 (0 ~ maxfdNum -1)
            fd_set *restrict readfds, //read I/O를 통지받을 FD_SET의 주소, 없으면 NULL
            fd_set *restrict writefds,//write I/O를 통지받을 FD_SET의 주소, 없으면 NULL
            fd_set *restrict errorfds,//error I/O를 통지받을 FD_SET의 주소, 없으면 NULL
            struct timeval *restrict timeout //null이면 변화가 있을 때까지 계속 Block, 
                                             //아니면 주어진 시간만큼 대기후 timeout.
           );
//반환값 : 오류 발생시 -1, timeout에 의한 반환은 0, 정상 작동일때 변경된 파일 디스크립터 개수
```  

FD의 개수가 계속해서 바뀔 수 있으므로, 전체 파일 디스크립터의 개수를 저장하는 변수가 필요하다. 그리고 인자로 넘긴 FD_SET의 값은 변경되므로, 관찰할 FD의 목록이 변하지 않는다면 select로 넘기는 FD_SET은 복사된 값을 넘기는 것이 현명하다.  





