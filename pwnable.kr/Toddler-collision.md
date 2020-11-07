# Toddler's Bottle - collision  

## 문제 설명  
```  
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
        int* ip = (int*)p;
        int i;
        int res=0;
        for(i=0; i<5; i++){
                res += ip[i];
        }
        return res;
}

int main(int argc, char* argv[]){
        if(argc<2){
                printf("usage : %s [passcode]\n", argv[0]);
                return 0;
        }
        if(strlen(argv[1]) != 20){
                printf("passcode length should be 20 bytes\n");
                return 0;
        }

        if(hashcode == check_password( argv[1] )){
                system("/bin/cat flag");
                return 0;
        }
        else
                printf("wrong passcode.\n");
        return 0;
}
```  

## 문제 풀이  
0.  
flag 파일은 col_pwn의 소유자 권한과 그룹 권한만 읽을 수 있도록 되어 있다.
col 프로그램에 col_pwn으로 setuid가 붙어있으니 col프로그램을 익스플로잇해서 쉘을 얻거나 flag파일을 출력하도록 하자.  

1.  
argv[1]로 사용자가 넘겨준 값을 check_password()에 넣어준 값이 hashcode 0x21DD09EC와 같으면 flag가 출력된다고 한다.  
그렇다면 우선 check_password() 함수를 해석해야 한다.  

* ```int* ip = (int*) p;```: 들어온 char형의 입력값을 int형으로 변환하고 ip로도 가리키겠다는 뜻.  
* ```for(i=0; i<5; i++)```: p의 길이는 5가 아니라 20일 것이다. argv[1]이 strlen 함수를 거쳐 20이 되지 않으면 통과를 하지 못하기 때문이다.  
그렇다면 왜 5일까! strlen은 char(1byte) 일때 20byte인 것이고, ip는 int 형이니 4byte 자료형이므로 int가 5개 있는 것이기 때문이다!  

그러면 argv[1]를 4byte씩 쪼개서 더한 값이 0x21DD09EC가 되면 된다.  

2.  
20byte가 어떻게 구성되나 생각을 해봤더니 그냥  
0x0000....00021DD09EC 즉, 0으로 16byte를 채우고 4byte가 hashcode면 되지 않나?  

```
./col `python -c 'print "\x00"*16+"\xEC\x09\xDD\x21"'`
```  

그랬더니 ```passcode length should be 20 bytes```가 뜬다.  
20개 입력했는데 왜저러지 생각했는데 0x00이 숫자로는 0이 맞지만 문자로는 null 문자이다!  
그래서 strlen 입장에서는 문자열이 곧바로 null로 시작하니 문자열 길이가 0이구나 생각한 것!  

3.  
그러면 0x00이 아닌걸로 만들어보자.  
총 5byte니까 4byte를 1로 만들자.  
(little endian으로 들어가니 0x00000001 도 쪼개면 0x00, 0x00.. 이렇게 되서 0x01010101 이렇게 들어가야 할듯)  
그리고 0x21DD09EC에서 0x01010101 * 4 값을 빼면 된다.  
계산기를 돌려보면 값이 0x1DD905E8이 나온다.  
```
./col `python -c 'print "\x01"*16+"\xE8\x05\xD9\x1D"'`
```  

4.  
그러면 성공적으로 flag가 출력된다.  
```
daddy! I just managed to create a hash collision :)
```  

+) 근데 이게 MD5랑 무슨 관련이지..?  


