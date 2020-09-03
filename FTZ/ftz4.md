# FTZ 4  
## 문제 설명  
```누군가 /etc/xinetd.d/에 백도어를 심어놓았다.!```  

## 문제 풀이  
* 백도어는 시스템에 존재하게 되면 공격자가 일반 보안 액세스 컨트롤을 우회하고 시스템에 액세스 할 수 있는 악성코드의 유형  

### 풀이 과정  
1. 일단 /etc/xinetd.d/ 에 대한 정보를 알아보자.  
```ls -l /etc/xinetd.d/```  
그러자 /etc/xinetd.d/ 디렉토리 파일 중에 이름이 ```backdoor```이라는 파일이 있음을 알 수 있다.  
권한은 **-r--r--r--  1 root  level4** 이렇게 되어있는데,
읽기 권한만 주어져있고, level4 유저가 파일 소유주로 되어 있다.  

2. ```cat backdoor```로 백도어 파일 내용을 확인해보자.  
```
service finger
{
        disable = no
        flags           = REUSE
        socket_type     = stream
        wait            = no
        user            = level5
        server          = /home/level4/tmp/backdoor
        log_on_failure  += USERID
}
```  
* 리눅스 사용자 정보 확인 명령어인 finger의 데몬 설정 정보가 나왔다.  
정보 해석은 아래와 같다.  

```
service finger                                     //서비스의 이름, /etc/services 파일에 등록된 이름과 같아야함
{
        disable = no                                // xinetd의 제어를 받을 것인가 결절, Yes-제어 안받음, No-제어 받음
        flags           = REUSE                     // 해당 서비스 포트가 사용 중인 경우 해당 포트의 재사용을 허가
        socket_type     = stream                    // socket 타입을 TCP/IP 프로토콜로 선택, stream(TCP), dgram(UCP)
        wait            = no                        // 해당 서비스가 이미 연결된 상태에서 또 다른 연결 요청이 들어오면 대기 시간 없이 응답할 것인지 유무(yes: xinetd가 요청되어 있는 한 데몬이 끝날 때까지 다른 요청을 받지 않음, no: 각 요청에 대해 데몬이 동작)
        user            = level5                    // 해당 데몬은 level5의 권한으로 설정됨을 의미, 데몬의 UID
        server          = /home/level4/tmp/backdoor // xinetd에 의해 실행될 데몬의 파일 위치
        log_on_failure  += USERID                   // 해당 서비스의 가동에 문제가 발생하면 userid에 로그 기록
}
```  
> xinetd란 서비스에 접속을 요청할시에, xinetd가 중간에 개입하여 허가된 사용자인지를 검사한다. 허가된 사용자가 맞다면, 해당 서비스를 요청해주는 일종의 검문소 역할.  
> 자세한 설명은 geundi님의 블로그(http://geundi.tistory.com/43) 를 참고  

아래와 같은 메커니즘을 통해 level5의 권한으로 해당 프로그램을 실행시키게 됨  
![d](https://user-images.githubusercontent.com/46364778/92147461-27c45d80-ee56-11ea-87e2-dfeadb0371c7.PNG)  

* finger 서비스를 실행하게 되면 level5 권한으로 서비스가 실행된다. 이를 이용해 level5 쉘을 획득하면 될 것 같다.  
* finger 서비스를 실행하면 xinetd에 의해 **/home/level4/tmp/backdoor** 에 위치한 데몬 파일이 실행된다고 한다.  


3. /home/level4/tmp 디렉토리로 이동해보자.  
해당 디렉토리 안에 아무런 파일이 존재하지 않는다. 이 상태에서 finger 서비스를 구동해도 xinetd에 의해 실행될 파일이 없기 아무 것도 일어나지 않을 것이다.  

```finger``` 명령어를 그냥 쳐보자.  
백도어가 실행되는 것이 아닌 finger의 원래 기능으로 실행되는 듯. finger 명령어라고 해서 다 xinetd를 거치는 것은 아니다.  

기본 finger 서비스의 경우 disable 옵션이 yes 라서 외부에서 접속할 경우엔 실행되지 않는다. 하지만 backdoor 서비스는 disable이 no 로 설정이되어있어 외부에서 접속할 경우엔 backdoor 서비스가 실행된다.  

finger 명령어는 외부 서버의 유저들의 정보도 가져올 수 있는 기능이 있는데,
finger [user]@[host] 명령어를 사용하면 된다.  

backdoor 를 실행시켜야 원하는 기능을 실행시킬 수 있으므로 finger @localhost를 하면 우리가 지정한 backdoor가 실행된다.  

4. 그러면 backdoor 역할의 파일을 임의로 만들어 finger 서비스 구동 시 xinetd에 의해 그 파일이 데몬으로 실행되도록 만들자!  
```
//backdoor.c  

#include <stdlib.h>
#include <stdio.h>

int main(void)
{
  system("my-pass");
  return 0;
}
```  
system 함수를 사용해 backdoor 실행 시, level5의 권한으로 실행되므로  
my-pass 명령어를 통해 level5의 패스워드를 출력하도록 한다!  

5. 컴파일하자  
```gcc -o backdoor backdoor.c```  
6. 이제 finger 서비스 구동 시 xinetd가 실행할 파일 backdoor을 만들었으니, finger 서비스를 실행시켜보자!  
```finger @localhost```  

7. 비밀번호는 what is your name?  

~~근데 난 왜 안되냐... system("id"); 하면 Broken pipe 뜸...~~  
~~system("cat /home/level4/hint; id") 이 명령어는 또 잘됨 왜이래...~~  


## 연관된 정보들  
### finger  
finger은 리눅스에서 사용자의 계정 정보를 확인하는 명령어이다.  
* finger 옵션  
-s : 사용자의 로그온 이름, 실제 이름, 터미널 이름, 로그온 시간 등을 보여준다.  
-l : -s 옵션 정보에 몇 가지를 추가하여, 여러 줄에 걸쳐서 보여준다.  
-p : -l 옵션 정보에서 .plan과 .project 파일을 보이지 않는다.  
옵션이 주어지지 않으면, 기본적으로 -l 옵션을 사용한 것으로 간주된다.  

* 명령어  
```finger``` : finger만 치면 현재 시스템에 로그인 되어 있는 사용자들을 보여준다.  
```finger user명``` : user을 적고 host명을 명시하지 않으면, finger는 로컬에 접속하게 된다.  
```finger @host명``` : host명만 적고 user를 명시하지 않으면, 해당 서버의 접속해 있는 모든 유저의 정보를 출력한다.  
```finger user명 @host명``` ```finger @host명 user명``` : user명과 호스트명을 이런식으로 기입하면 원격 서버의 사용자계정정보 확인하는 것이 된다.  

* 참고  
finger 명령어는 지정된 계정사용자 정보를 /etc/passwd 파일에서 읽어서 보여주는 것이다.  

### Daemon  
* 멀티태스킹 운영체제에서 데몬(deamon)은 사용자가 직접적으로 제어하지 않고, 백그라운드에서 돌면서 여러 작업을 하는 프로그램  
* 특정 서비스를 위해 백그라운드 상태에서 계속 실행되는 서버 프로세스  
* 시스템에 관련된 작업을 하는 후위 프로세스(background process)  
* 보통 데몬을 뜻하는 'd'를 이름 끝에 달고 있으며, 일반적으로 프로세스로 실행  
* 서비스 요청이 없을 때는 후위 프로세스로서 유휴(idle) 상태에 들어가 시스템의 CPU를 차지하지 않지만 메모리와 기타 자원을 상당수 차지  
* 데몬은 부팅 중에 메모리에 로딩되어 컴퓨터가 종료될 때까지 상주  
* 데몬은 대개 부모 프로세스를 갖지 않는다.  
PPID = 0  
프로세스 트리에서 init 바로 아래에 위치  
* 데몬이 되는 방법  
fork off and die : 자식 프로세스를 fork하여 생성하고 자식을 분기한 자신을 죽이면 init이 고아가 된 자식 프로세스를 자기 밑으로 데려간다.  
* 시스템이 켜지며 시작되는 데몬들  
네트워크 요청, 하드웨어 동작, 타 프로그램에 반응하는 일을 함  
* 몇몇 리눅스의 devfsd처럼 하드웨어 설정이나 cron처럼 주기적인 작업을 실행하기도 함  

### Deamon 종류  
**단독으로 실행되는 데몬(standalone)**  
- 단독으로 메모리에 상주하고 있는 방식
- 웹서비스처럼 클라이언트의 서비스 요청이 많은 경우에 유용  
- 항상 램에 상주하므로 좀 더 빠른 서비스가 가능 -> 자주 사용되는 데몬이라면 문제가 없지만 어쩌다 한번 가끔 사용데몬은 자원(메모리)의 낭비를 초래  
- 개별 서비스별로 서버 프로세스(데몬)가 동작하는 방식으로 속도가 빠른 장점이 있지만 서버 리소스도 많이 점유하고 있는 단점이 있다.  

ex) httpd, named, sendmail, crond, gated, netfs, nfs, lpd, mcserv, rcd, syslog, squid, amd, portmap, routed, dhcp, gpm, kerneld, network, ruserd ...  


**슈퍼데몬 inet에서 관리하는 데몬**  
> inet  
> * Internet Superserver  
> * 자주 실행되지 않는 데몬들을 통들어 관리해 슈퍼데몬이라 함  

- 슈퍼데몬이라는 것이 있는데, 슈퍼데몬이 메모리에 상주해 있으면서 슈퍼데몬에서 관리하는 데몬이 호출될 경우 그 데몬을 잠깐 메모리에 올렸다가 처리가 끝나면 다시 종료시킨다.  
- 슈퍼 데몬을 이용하여 개별 서비스를 동작시킴  
- 일반 데몬처럼 프로세스가 항상 떠있지 않고, 클라이언트의 요청이 있는 경우에만 데몬을 실행  
- standlone보다는 응답시간은 좀 걸리지만 메모리가 절약(간헐적으로 사용되는 많은 데몬들을 효율적으로 운용할 수 있음)  
- 커널 2.4버전(리눅스 7.x버전 이후)에서는 xinetd라는 이름의 슈퍼데몬이 작동  

> 환경설정은 /etc/xinetd.conf와 /etc/xinetd.d 디렉토리의 각 서비스파일에서 관리  
ex) telnet, ftp, finger, login, auth, shell, tcpd  


### inetd [Internet Services daemon]  
* xinetd의 이전 버전  
* 네트워크 접속을 제어(들어온 접속 요청들을 해당 프로그램에 전달한다)  
* inetd는 tcpd와 같이 사용된다  
* 예를 들어, 이런 순차적인 방식으로 inetd는 동작한다  
> inetd가 관리하는 포트에 접속 요청 들어옴  
> inetd는 tcpd 프로그램에게 요청을 넘김  
> tcpd는 hosts.{allow|deny} 파일의 규칙에 따라 허락 여부를 결정  
> 여기서 허락된 요청에 대해 서버 프로세스(예를 들면, ftp)가 시작  



### xinetd [Extended Internet Services daemon]  
* 커널 2.4 이후 버전  
* 접속을 시도하면, **허가된 사용자인지 검증** 후에 서비스 프로그램에 연결을 넘긴다  
* TCP, UDP, RPC 서비스에 대한 접근을 제어  
* 시간 별 접근 제어 기능  
* 접속 성공이나 실패에 대한 완벽환 로그기록  
* RFC1413에 기반한 유저관리 구현  
* 서비스 거부 공격(DoS)을 능률적으로 견제  
> 동시에 실행될 수 있는 똑같은 서버의 개수 제한  
> * 서버의 전체개수에 대한 제한  
> * 로그 파일 크기의 제한(로그가 넘치지 않도록 합니다.)  

* Xinetd모드의 서비스 흐름도(telnet의 경우)  
> * 외부에서 telnet 서비스 요청이 들어온다.  
> * xinetd 데몬이 /etc/xinetd.conf에 등록되어 있는 telnet 프로그램을 호출한다.  
ex) telnet  stream  tcp nowait  root  /usr/sbin/telnetd telnetd  
> * 외부의 telnet 요청과 내부 프로그램을 연결시켜 서비스 요청에 대한 처리를 해주게 된다.  



**설정 파일의 설정 사항**  
- service : 서비스 이름  
- disable : 해당 서비스의 실행 여부를 결정한다. yes : 실행안함, no : 실행  
- socket_type : 서비스 소켓 유형을 설정한다. 일반적으로 tcp경우 stream, udp의 경우 dgram을 설정한다.  
- wait : 서비스 요청 처리 중 다음 요청이 들어오면 이를 즉시 처리할 것인지(no) 이전 요청이 완료될 때까지 대기할 것인지(yes) 설정한다.  
- user : 어떤 사용자로 서비스를 실행할지 설정한다.  
- server : 서비스 실행 파일 경로를 설정한다. 반드시 절대경로로 설정한다.  
- server_args : 실행 프로그램의 인자로 설정파일 경로를 작성한다.  
- cps : 연결요청을 제한하기 위한 설정으로 첫 번째 인자는 초당 연결 개수를 의미하고 두 번째 인자는 초당 연결 개수를 초과하면 일시적으로 서비스가 중지되는데 서비스 일시 중지 후 재시작할 때까지 대기하는 시간을 의미한다.  
- instances : 동시에 서비스할 수 있는 서버의 최대 개수를 지정한다.  
- per_source : 출발지 IP를 기준으로 최대 서비스 연결 개수를 지정한다.  
- only_from : 특정 주소 또는 주소 대역만 접근을 허용한다.  
- no_access : 특정 주소 또는 주소 대역의 접근을 차단한다.  
- access_times : 지정한 시간 범위 내에서만 접근을 허용한다.  
- log_on_failure : 서버 접속에 실패했을 경우 로그파일에 기록할 내용을 설정한다.  
- log_on_success : 서버 접속에 성공했을 경우 로그파일에 기록할 내용을 설정한다.  

**설정 파일**  
> ```/etc/xinetd.conf```  
글로벌 설정파일  
슈퍼데몬이 관리하는 모든 서비스에 해당 설정이 적용된다.  
![a](https://user-images.githubusercontent.com/46364778/92142014-2c851380-ee4e-11ea-9b3e-b3ad03f3008b.png)  
![b](https://user-images.githubusercontent.com/46364778/92142009-2bec7d00-ee4e-11ea-8c86-16177d7c39cb.png)  
기본 값으로 설정되어있는 /etc/xinetd.conf 설정파일  
includedir을 통해 이 파일은 전체 설정 파일이고, 추가적인 서비스 설정파일이 /etc/xinetd.d 디렉토리 안에 있다는 것을 확인할 수 있다.  

> ```/etc/xinetd.d```  
각 서비스 별 설정 파일  
각 서비스 별 설정을 따로 설정해서 적용시킬 수 있다.  
![c](https://user-images.githubusercontent.com/46364778/92142223-77069000-ee4e-11ea-9ead-1a2e8b990b73.png)  
예시로 /etc/xinetd.d 디렉토리 안에 있는 FTP 서비스 설정사항파일 확인  
위에 작성된 설정은 필수 설정이다. 추가적인 설정 가능  


[출처1](https://sungpil94.tistory.com/206)  
[출처2](https://blog.naver.com/PostView.nhn?blogId=lay126&logNo=220417778760&proxyReferer=https:%2F%2Fwww.google.com%2F)



