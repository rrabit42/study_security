# FTZ 3  
## 문제 설명  
다음 코드는 autodig의 소스이다.  

```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv){

    char cmd[100];

    if( argc!=2 ){
        printf( "Auto Digger Version 0.9\n" );
        printf( "Usage : %s host\n", argv[0] );
        exit(0);
    }

    strcpy( cmd, "dig @" );        // 문자열 복사, 두번째 인자를 첫번째 인자로 덮어쓰기 복사
    strcat( cmd, argv[1] );        // 문자열 덧붙이기, 두번째 인자를 첫번째 인자(문자열)에 덧붙인다
    strcat( cmd, " version.bind chaos txt");

    system( cmd );                 // 시스템 명령어 실행

}
```  
이를 이용하여 level4의 권한을 얻어라.  
  
more hints.  
- 동시에 여러 명령어를 사용하려면?  
- 문자열 형태로 명령어를 전달하려면?  

## 문제 풀이  
### 풀이 과정  
1. 문제 해석  
autodig 프로그램의 인자 값은 프로그램 이름 포함 2개가 필요하다.  
cmd 배열에 'dig @[인자값] version.bind chaos txt'를 저장하고 system 함수에 전달해서 실행한다.  
2. 아무리 둘러봐도 autodig란 함수가 없다. find 명령어를 통해 auto dig를 찾자.  
```find / -name "autodig" 2> /dev/null```  
그러자 ```/bin/autodig``` 란 경로가 나타난다.  

3. autodig가 어떤 파일인지 확인해보자!!  
```find / -user level4 -perm -4000 2>/dev/null```  
소유주가 level4이고 setuid가 설정된 파일을 검색하니 ```/bin/autodig``` 파일이 출력되었다!  

4. /bin/경로로 이동하여 autodig 프로그램을 실행한다. 그 후 아무 문자열이나 넣어서 해당 프로그램을 실행시켜보자.  
```cd /bin```  
```./autodig asdf```  
asdf를 따옴표로 묶지 않아서 asdf란 service를 실행시키게 된다.  
> **dig [@server] [domain] [query type]**  
> dig는 Domain Information Groper의 약자로 DNS로부터 정보를 가져올 수 있는 툴이다.  DNS 네임서버 구성과 도메인 설정이 완료된 후, 일반 사용자의 입장에서 설정한 도메인 네임에 대한 DNS 질의응답이 정상적으로 이루어지는지를 확인 점검하는 경우에 많이 사용한다.  

5. 네임서버 정보 확인은 우리가 의도한 방향이 아니므로, 힌트를 확인해서 다시 풀어보자.  
* 동시에 명령어를 사용하려면 세미콜론(;)로 구분해주면되고,  
* 문자열 형태로 명령어를 전달하려면 double quote("")로 명령어를 묶어주면 된다.  

5. level4의 권한을 얻으려면 우선 쉘을 획득해야 하므로 /bin/sh 명령어가 들어가야 할 것이다.  
```./autodig "/bin/sh;"```  
그럼 쉘이 떨어진다! 그리고 비밀번호를 알아내는 명령어는 FTZ에서 my-pass이므로 ```my-pass```를 입력하면  
비밀번호 "such my brain"이 나온다!  

## 연관된 정보들  
* dig  
* 다중 명령어  
1. 세미콜론(;)  
하나의 명령어 라인에서 여러 개의 명령을 실행(하나의 명령어 다음에 추가)  
첫 번째 명령이 실패하여도 두 번째 명령은 반드시 실행이 됨  

2. 파이프(|)  
앞에서 나온 명령 결과를 두 번째 명령에서 사용  

3. 더블 엠퍼센드(&&)  
첫 번째 명령이 에러 없이 정상적으로 종료했을 경우에만 두 번째 명령을 수행  

4. 더블 버티컬바(||)  
첫 번째 명령의 결과에서 에러가 발생하더라도 각각의 모든 명령을 수행  


