# Toddler's Bottle - mistake  

## 문제 설명  
<img width="442" alt="1" src="https://user-images.githubusercontent.com/46364778/98458999-9ff22b00-21d9-11eb-9009-4a9959585c6b.PNG">  

```
#include <stdio.h>
#include <fcntl.h>

#define PW_LEN 10
#define XORKEY 1

void xor(char* s, int len){
        int i;
        for(i=0; i<len; i++){
                s[i] ^= XORKEY;
        }
}

int main(int argc, char* argv[]){

        int fd;
        if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
                printf("can't open password %d\n", fd);
                return 0;
        }

        printf("do not bruteforce...\n");
        sleep(time(0)%20);

        char pw_buf[PW_LEN+1];
        int len;
        if(!(len=read(fd,pw_buf,PW_LEN) > 0)){
                printf("read error\n");
                close(fd);
                return 0;
        }

        char pw_buf2[PW_LEN+1];
        printf("input password : ");
        scanf("%10s", pw_buf2);

        // xor your input
        xor(pw_buf2, 10);

        if(!strncmp(pw_buf, pw_buf2, PW_LEN)){
                printf("Password OK\n");
                system("/bin/cat flag\n");
        }
        else{
                printf("Wrong Password\n");
        }

        close(fd);
        return 0;
}
```  

## 문제 풀이  
0.  
문제를 해석해보자.

* ```int open(const char * FILENAME, int FLAGS[, mode_t MODE])```  
char *FILENAME: 대상 파일 이름  
int FLAGS : 파일에 대한 열기 옵션  
그 외: O_CREAT 옵션 사용 시 파일이 생성될 때 지정되는 파일의 권한이다.  
return 값은 정상적으로 open하면 file descriptor의 값이 반환되고, 실패하면 -1이 반환된다.  

* operator priority 때문에 크기 비교(<)를 먼저한다. open()함수는 성공하니 file descriptor를 반환할 것이고, 반환 값은 양수이다.  
때문에 크기 비교에서 false값(C에서 false는 0이다)이 fd에 최종적으로 들어가게 된다.  
**연산자 우선순위에서 =가 대부분 제일 낮기 때문에 마지막으로 판단해주면 된다.**  

* ```len=read(fd,pw_buf, PW_LEN) > 0)```: fd의 10byte를 읽어들여 11byte의 char형 배열인 pw_buf에 저장한다.  
read 함수가 성공하면, 읽어들인 길이만큼 len에 저장한다. 실패하면 read error 출력 ...
**여기서 fd가 0이고, 0이면 표준입력이므로 사용자에게서 입력을 받게 된다!**  

* 그리고 다시 11byte char형 배열 pw_buf2에 사용자 입력을 받는다.  
pw_buf2는 xor()함수를 거치는데, 여기서 각 원소는 XORKEY 즉, 1과 XOR한 값으로 배열이 바뀌게 된다.  

* 그리고 pw_buf와 pw_buf2를 10byte 비교했을 때 같으면 flag를 출력해준다.  

1.  
그냥 요지는 pw_buf에 pw_buf2에 1과 xor한 값으로 넣어주면 된다는거 아닌가!  
그래서 A..10개랑 @..10개를 넣어주면 된다.  
0은 0x30 110000  
1은 0x31 110001(X, 이건 문자 1)  

A는 0x41 이므로 1000001  
@는 0x40 이므로 1000000  

[참고](https://www.ibm.com/support/knowledgecenter/ko/ssw_aix_71/network/conversion_table.html)  









