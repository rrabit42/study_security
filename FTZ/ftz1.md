# FTZ 1  
## 문제설명  
level2 권한에 setuid가 걸린 파일을 찾아라.  

## 문제 풀이  
### setuid  
- setuid가 설정된 파일 실행 시, 특정 작업 수행을 위하여 일시적으로 파일 **소유자의 권한**을 얻게 된다.  
- 즉, 소유자가 root인 파일에 setuid가 설정되어 있을 때, 일반 사용자가 그 file을 실행하게 되면 그 순간 잠시동안 파일의 소유자인 root의 권한을 빌려오는 것이다.  


- setuid 설정을 하는 이유  
> 계정의 password 변경을 할 때, passwd 명령어(/usr/bin/passwd => passwd 명령어 실행파일)로 패스워드를 지정하고, 변경 시 /etc/passwd, /etc/shadow 파일(계정 사용자의 정보를 보관하고 있는 파일들)의 내용이 변경된다.  
> /etc/passwd => 644: root만 수정 가능  
> /etc/shadow => 000: root만 수정 가능  
- 즉, root가 아닌 일반 사용자는 passwd를 변경할 수 없다?!  
> 방법은 일반 사용자여도 자신의 passwd를 원하는대로 바꿀 수 있도록 setuid를 설정해 주는것!  
> passwd 변경 실행파일이 있는 /usr/bin/passwd를 보자!  
> rw"s", setuid 비트가 설정될 때 [사용자접근권한]의 실행 권한 자리에 실행권한이 있으면 소문자 s로, 실행권한이 없으면 대문자 S로 표시된다.  
> 즉, passwd는 setuid 비트가 적용된 것을 확인할 수 있다. 따라서 이 파일의 소유자인 root의 권한을 얻어 수행할 수 있다.  


- setuid 설정 방법  
> 기호모드(u+s) : user에 setuid 적용  
> 숫자모드(4000) : setuid 적용수는 4이다.

### 명령어  
- 이 문제는 level2 권한으로 setuid가 걸린 파일을 찾으라는 것  
- setuid가 설정된 file 혹은 directory 찾기 명령어  
> ```find [파일을 검색할 디렉토리 경로] -user [소유자] -perm [접근권한]```  
> ```
> find / -user root -perm -4000
> 
> find : 찾기 명령어  
> / : 최상위 폴더로부터
> -user root : 소유자는 root이며
> -perm : permission은 4000인 것을 찾는다
> ```  


### 풀이과정  
- ```find / -user level2 -perm -4000 2> /dev/null ``` 
- 2> dev/null은 2(표준에러)를 /dev/null(휴지통)에 넣는다는 의미  
- 그 결과 ```/bin/ExecuteMe```라는 파일을 찾을 수 있다.  
- 해당 파일을 실행시키면 my-pass와 chmod 제외한 한가지 명령어를 실행시켜준다고 한다.  
- ```/bin/bash``` : 쉘을 실행시켜달라고 하자  
- 그 후 my-pass하면 level2의 비밀번호가 나온다.  
- "hacker or cracker"

## 연관된 정보들  
* setgid  
* sticky-bit
