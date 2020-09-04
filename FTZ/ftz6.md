# FTZ 6  
## 문제 설명  

<img width="500" alt="1" src="https://user-images.githubusercontent.com/46364778/92227733-a87c6b80-eee1-11ea-86ab-f54f456ea38c.PNG">  

갑자기 이렇게 뜬다. 여기서 엔터를 누르면  

<img width="350" alt="2" src="https://user-images.githubusercontent.com/46364778/92227726-a7e3d500-eee1-11ea-931f-188abdfaf351.PNG">  

이 화면으로 넘어가는데 Ctrl+c를 누르면 위와 같이 종료가 되지 않는다고 나온다.  
아무튼, 메뉴를 선택하면 나오는 다음 문구는 telnet을 시도할 때 나오는 문구다.  
메뉴를 선택하면 조건에 맞는 ip값이 전달되고 텔넷 명령어가 시작되는 것.  
즉, 1번 메뉴를 눌렀을 때 system("telent 203.245.15.76")이라는 명령어가 실행되는 것이다.  

<img width="300" alt="3" src="https://user-images.githubusercontent.com/46364778/92228019-2a6c9480-eee2-11ea-82a3-deae6f0556cf.PNG">  

어느 것을 선택해도 연결이 되지 않는다.  

> 오래 기다려도  

```
telent: connect to address 203.245.15.76: Connection refused  
Connection closed by foreign host
```  
> 이렇게 출력된다. 한마디로 무쓸모.  

## 문제 풀이  
### 풀이 과정  
1. 풀이는 아주 간단하다.  
첫번째 사진 화면에서 Ctrl+c를 누르면 level6의 쉘로 접속할 수 있다.  

2. 그리고 쉘에서 ```ls```을 치면 **password**라는 수상한 파일이 발견된다.  
출력해보자.  

3. ```cat password```  
Level7 password is "come together".  

### 문제 탐구  
**시스템 인터럽트**와 관련이 있는 문제다.  
System Interrupt는 프로세스간에 주고 받는 신호이다.  
인터럽트를 유발하는 시그널 목록을 우선 보자.  
<img width="350" alt="4" src="https://user-images.githubusercontent.com/46364778/92228397-c72f3200-eee2-11ea-84f8-55a1be77ba9b.PNG">  

> * 프로세스 종료  
2)SIGINT -> 일반종료, Ctrl+C  
15)SIGTERM -> 일반 종료  
9)SIGKILL -> 강제 종료, Ctrl+Z  
> * 프로세스 정지  
19)SIGSTOP  
> * 프로세스 재시작  
18)SIGCONT  

운영체제와 다른 프로세스에 시그널을 보내는 것은 일종의 정보 공유 기능에 해당하므로 프로그램에 따라 인터럽트 처리가 필수인 경우가 많다.  
또한 시그널은 소스코드에서 사용할 수 있게 *signal.h*이라는 헤더 파일에 정의되어있다.  
*signal.h* 헤더파일의 위치는 다음과 같다. ```/usr/include/asm/signal.h```  

#텔넷 접속 서비스# 선택지에서 접속이 되지 않는 이유를 확인하기 위해서 DNS 역조회를 이용해 도메인을 확인해보자.  

## 연관된 정보들  
* [출처](https://marcokhan.tistory.com/98?category=745849)  
* [PC 통신](https://ko.wikipedia.org/wiki/PC%ED%86%B5%EC%8B%A0)  
> BBS(Bulletin Board System)  
> 보통 게시판이라는 뜻으로 쓰이는 약어  
PC 통신이 몰락한 후 인터넷 초창기에도 게시판이라는 용어와 동일하게 쓰였지만 현재는 거의 쓰이지 않으며 BBS 대신 보드(Board)라고 많이 부른다. 물론, 여전히 도메닝 등에선 자주 볼 수 있다.  

bbs란 예전에 PC통신 할 때 텔넷으로 접속하던 게시판이라고 생각하면 된다.  
하이틸, 나우누리, 천리안이 가장 유명했던 bbs들이었다.  



