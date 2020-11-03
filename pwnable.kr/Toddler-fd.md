# Toddler's Bottle - fd  

## 문제 설명  
```
Mommy! what is a file descriptor in Linux?

* try to play the wargame your self but if you are ABSOLUTE beginner, follow this tutorial link:
https://youtu.be/971eZhMHQQw

ssh fd@pwnable.kr -p2222 (pw:guest)
```  

## 문제 풀이  
0.  
putty로 접속한다.  
* host: fd@pwnable.kr  
* port: 2222
* id/pw: fd/guest  

1.  
접속하고 ls 해보니 fd, fd.c, flag 이렇게 세 파일이 있다.  
**fd.c**는 다음과 같다.  
```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
        if(argc<2){
                printf("pass argv[1] a number\n");
                return 0;
        }
        int fd = atoi( argv[1] ) - 0x1234;
        int len = 0;
        len = read(fd, buf, 32);
        if(!strcmp("LETMEWIN\n", buf)){
                printf("good job :)\n");
                system("/bin/cat flag");
                exit(0);
        }
        printf("learn about Linux file IO\n");
        return 0;

}
```  

2.  
bof 공격인가 하니, read에서 입력받는 버퍼가 32로 할당한 버퍼크기랑 같아서 아닌 것 같다.  
fd에 대한 문제라고 하니 file descriptor를 이용하는 문제일거다.  

일단 함수들을 살펴보자.  
* atoi() : char(ascii) to int, 문자열을 정수 타입으로  
* read(int fd, void *buf, size_t nbytes), 여기서 첫번째 인자는 파일 디스크립터를 받는다.  

버퍼와 LETMEWIN을 비교한다. 즉 read할 때 buf에 값을 LETMEWIN으로 채워줘야한다.  
그럼 read할때 fd가 아니라 내가 직접 입력한 값으로 넣게해주면 되지 않을까 하고 찾아보니,  

|파일 디스크립터|대상|  
|:---:|:---:|  
|0|표준입력 : Standard Input|  
|1|표준출력 : Standard Output|  
|2|표준에러: Standard Error|  

그럼 fd가 0이 되면 될 것 같다.  
fd를 어떻게 0으로 만드나 보니 ```fd = atoi( argv[1] ) - 0x1234;```  
즉 실행할 때 인자로 0x1234를 똑같이 주면 된다.  

```./fd 0x1234```하니 안된다ㅋㅋㅋㅋㅋ  

10진수로 바꿔야하나보다. 계산기를 통해 바꿔주면,  
```./fd 4660```  
됐다!!!!!!!!! 그러면 이제 내가 직접 입력을 넣어줄 수 있다.  
```LETMEWIN```  

good job과 함께 flag ```mommy! I think I know what a file descriptor is!!```가 출력되었다.  







