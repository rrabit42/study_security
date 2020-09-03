# FTZ 8  
## 문제 설명  
```
level9의 shadow 파일이 서버 어딘가에 숨어있다.
그 파일에 대해 알려진 것은 용량이 "2700"이라는 것 뿐이다.
```  

## 문제 풀이  
### 풀이 과정  

1. find 명령어를 써야지 암!  
find에서 -size 옵션을 주면 파일 크기를 기준으로 검색할 수 있다.  

> ```find ./* -size +N``` : N 이상 크기의 파일을 검색한다.  
> ```find ./* -size -N``` : N 이하 크기의 파일을 검색한다.  
> ```find ./* -size N``` : N 크기의 파일을 검색한다.  

> **사이즈 단위**  
> * b : 블록단위  
> * c : byte  
> * k : kbyte  
> * w : 2byte 워드  
> * 아무런 단위도 붙이지 않은 경우 디폴트 값: b  

2. ```find / -size 2700 2>/dev/null``` 하니까 결과가 안나옴  
```find / -size 2700c 2>/dev/null```을 해보자.  
```
/var/www/manual/ssl/ssl_intro_fig2.gif
/etc/rc.d/found.txt
/usr/share/man/man3/IO::Pipe.3pm.gz
/usr/share/man/man3/URI::data.3pm.gz
```  
이런 결과가 출력된다.  

3. 여기서 이름으로 cat하라고 알려주는 found.txt 내용을 확인하자.  
```cat /etc/rc.d/found.txt```  
```
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524
```  
호오.. 암호화 되어 있는 듯 하다.  

4. shadow 구조에 따르면 ```$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.``` 이게 Encrypted password 부분이다.  
그리고 이 구조를 다시한번 분해해보면, 첫번째 부분이 $1, 즉 MD5 방식으로 암호화 되어있음을 알 수 있다.  

5. MD5 복호화를 하려고 했는데 해쉬도 과정에 있어서 안될 것 같다.  
=> crack 툴을 써야한다!!  

> **John the Ripper(존 더 리퍼)**  
> Solar Designer가 개발한 Unix계열 password crack tool이다.  
> 사용자 명과 비슷한 암호 검색, 단어의 조합, 숫자 조합, 알파벳+숫자의 조합, 특수문자 조합 등등 여러 시도를 통해 패스워드를 크랙한다.  
> 무료 도구이며, UNIX 계열 크래킹도구이지만 DOS, Win9x, NT, 2000 등의 플랫폼도 지원한다.  
> 속도를 높이기 위해 Intel MMX기술이나 AMD K6 프로세서의 특수 기능들을 이용한 최적화된 코드를 집어넣기도 하였다.  
> http://www.openwall.com/john/ 에서 개발버전, 안정버전, linux용, windows용 등을 다운 받을 수 있다.  

이제 우리 실습 환경에서 다운 받아 보자.  
쉘에서  

6. ```wget http://www.openwall.com/john/j/john-1.8.0.tar.gz``` : wget으로 복사한 주소를 입력해 다운 받는다. 정상적으로 설치가 완료되면 john-1.8.0.tar.gz파일이 생성될 것.  
7. ```tar zxvf john-1.8.0.tar.gz``` : tar 압축 풀기  
8. 압축 풀면 john-1.8.0 디렉토리가 생성될 것이다. 안에는 README, /doc, /run, /src와 같은 파일들이 있고, README에는 프로그램에 대한 설명이 들어있다.  
9. ```cd src``` : src 디렉토리로 이동  
10. 존 더 리퍼 프로그램을 사용하려면 먼저 컴파일을 해야하는 make 명령어로 컴파일 가능한 버전을 확인한다.  
대부분 linux-x86-64나 linux-x86-any로 컴파일하면 되는데  
```make linux-x86-64```  
```make linux-x86-any```  
둘 다 오류가 난다면 다음과 같이 클린 옵션을 주어 컴파일 하면 오류없이 컴파일이 된다.  
```make clean linux-x86-64```  
11. 컴파일이 정상적으로 완료되면 run 디렉토리에 john 실행파일이 생긴다. 그러면 프로그램을 사용할 준비가 끝난것이다!  
12. ```vi pass.txt```에 ```level9:$1$vkY6sSlG$6RyUXtNMEVGsfY7Xf0wps.:11040:0:99999:7:-1:-1:134549524``` 값을 넣는다.  
13. ```./john pass.txt``` : 암호화된 부분이 복호화되어 출력된다.  
+) ```./john -show pass.txt``` : 패스워드가 크랙된 원문을 보려면 -show 옵션으로 실행하면 된다.  

14. 비밀번호는 apple 이다.  
~~나는 실습환경에서는 되지 않아서 윈도우에 해당 크랙툴은 다운받아서 했다..~~  

## 연관된 정보들  
### shadow 파일  
패스워드를 암호화하여 보호하기 위해 만들어진 것으로 기존의 /etc/passwd 파일에 있던 비밀번호를 shadow 파일에 암호화하여 저장하게 된다.  
> /etc/passwd 는 파일이 암호화되어있지만 누구나 읽을 수 있기 때문에 암호를 해독하고 사용하는게 어렵지 않다.  
shadow 파일은 일반적으로 root만이 읽을 수 있는 권한(400)이 존재하기 때문에 더 안전하다.  
또한 패스워드에 대한 만료, 갱신 기간, 최소 기간 등의 시간 상의 관리 정책을 저장하고 있다.  

**shadow 패스워드의 기능**  
* 실제로 암호화된 패스워드들을 일반 사용자는 보지 못하도록 /etc/shadow 파일에 저장할 수 있다.  
* Encrypted group 패스워드들과 group administrator에 대한 정보를 대체되는 파일에 저장할 수 있다.  
* 사용자의 패스워드의 최대 길이를 8자에서 16자로 늘려준다.  
* 패스워드가 일정 기간 경과하면 사용자로 하여금 패스워들ㄹ 바꾸도록 한다.  

**vi /etc/shadow 구조**  

> root:$6$5H0QpwprRiJQR19Y$bXGOh7dIfOWpUb/Tuqr7yQVCqL3UkrJns9.7msfvMg4ZO/PsFC5Tbt32PXAw9qRFEBs1254aLimFeNM8YsYOv. : 16431 : 0 : 99999 : 7 : : :  

```|-1-|———————2———————|-3-|-4-|-5-|-6-|-7-|-8-|```  

각 항목별 구분은 :(콜론) 으로 구분되어있으며 콜론과 콜론 사이 각 필드에는 다음과 같은 구조로 구성되어 있습니다.  

1. Login Name : 사용자 계정
2. Encrypted : 패스워드를 암호화시킨 값  
3. Last Changed : 1970년부터 1월 1일부터 패스워드가 수정된 날짜의 일수를 계산  
4. Minimum : 패스워드가 변경되기 전 최소사용기간(일수)  
5. Maximum : 패스워드 변경 전 최대사용기간(일수)  
6. Warn : 패스워드 사용 만기일 전에 경고 메시지를 제공하는 일수  
7. Inactive : 로그인 접속차단 일 수  
8. Expire : 로그인 사용을 금지하는 일 수 (월/일/연도)  
9. Reserved : 사용되지 않음  

*여기서 2번 항목 앞쪽 부분을 잘 보시면 $ 로 구분이 지어져 있습니다.
이 구분은 다음과 같은 값이 적용됩니다.  

```[$Hashid $Salt $Hash value]```  
* Hashid  
어떤 scheme 를 이용해 hash 를 했는지 보여줍니다.  
아래 표와 같이 어떤 scheme를 사용했느냐에 따라 id 값이 달라지며 주로 많이
사용되는것은 $1, $5, $6 입니다.  
![passwd-5](https://user-images.githubusercontent.com/46364778/92240752-192e8280-eef8-11ea-80b6-ab8b5678804e.jpg)  

* Salt  
해시는 단 방향 함수 입니다.
다시 말하면, A->B는 가능하지만 B->A는 불가능하다는 뜻입니다.  
결국 해시를 하고 난 값을 가지고 해시 하기 전의 값을 못 구한다는 뜻 입니다.  
그래서 이를 공격하기 위해서 해커들은 레인보우테이블을 미리 구해둡니다.  
레인보우테이블은 모든 해시 쌍들을 구해놓은 것으로,
이를 통해 해시값들을 대입하여 고속으로 패스워드를 크랙할 수 있게합니다.  
일반 사용자는 아무리 비밀번호를 어렵게 해도 이에 대한 해시 값 만 해커가 대입을 한다면 패스워드가 노출될 수 밖에 없습니다.  
그래서 이를 좀 더 어렵게 하기 위해 salt를 넣습니다.  
salt는 해시를 하기 전에 랜덤 한 값을 참고하는데,
해커가 salt값을 모른다면 레인보우테이블을 가지고 있어도 의미가 없습니다.  
해당 salt 따른 값이 아니기 때문입니다.  

* Hash value  
hash value는 hashid에 따른 해시방법과 salt값을 가지고 hash function을 수행한 결과입니다.  

~~크으 사기초에서 배운 내용들~~  

[출처](http://blog.plura.io/?p=3284)






