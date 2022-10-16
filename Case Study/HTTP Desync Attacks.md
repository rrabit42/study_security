# HTTP Desync Attacks  
[공부 대상](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn)  

## 개요  
HTTP 요청은 전통적으로 격리된(isolated) 독립 실행형(standalone) entity로 간주됨.  
그러나 원격의 인증되지 않은 공격자가 이러한 격리를 뚫고 요청을 다른 요청에 연결하는 (잊혀진) 기술.  

이 공격을 이용하여 악의적인 영역으로 라우팅하고, 유해한 응답을 호출하고, 자격 증명을 공개적으로 유인하라는 피해자의 요청을 섬세하게 수정하는 방법을 보여줄 예정.  
또한 프론트엔드에 배치된 모든 신뢰를 악용하고 내부 API에 대한 최대 권한 액세스 권한을 얻고 웹 캐시를 감염시키며 PayPal의 로그인 페이지를 손상시키기 위해 요청에 백엔드 재조립(reassembly) 사용하는 방법 시연할 것.  

**HTTP Request Smuggling** 을 이용한 공격  

HTTP Desync Attack은 Black Hat과 DEF CON에서 처음 소개됨. [동영상 자료](https://www.youtube.com/watch?v=w-eJM2Pc0KI&themeRefresh=1)  

## Core concepts  



## 질문  
* xPost는 에러가 나는데 xGet은 되는 이유?  
* 클라이언트의 CN? (상호 TLS 인증 형식, 액세스 제어 메커니즘의 일부로 사용)  
* Web Cash Poisoning  
웹 서버들은 어떤 요청에서 캐시되고 어떤 데이터를 제공해줄지 기록함.  
요청을 식별하는(캐시를 불러와야할 요청인지?) 값이 Cache Key.  
캐시 키는 웹 요청(Request)에서 일부를 떼어내어서 만들고 이에 상응하는 Response를 저장.  
고로, Request의 모든 부분을 확인하지는 않음.  

Web Poisoning은  
1. Cache Key로 사용되지 않은 헤더, 파라미터 등 데이터를 식별한다.  
2. 해당 값이 Response에 미치는 영향 체크  
3. (영향을 끼치는 경우) 공격코드가 Response 되도록 Cache 저장(단순히 해당 값에 공격 코드를 넣고 요청 전달)  

https://useegod.com/2021/12/06/web_cache_poisoning/  
https://www.hahwul.com/2018/12/31/web-cache-poisoning-attack-with-header-xss/  
https://www.hahwul.com/cullinan/web-cache-poisoning/  

* 헤더의 X-Forwarded-Host 와 X-Forwarded For 란?  
요청이 어디서부터 건너왔는지 알려주는 헤더.  
실제 세상에서는 클라이언트(요청) - 서버(응답)와 같은 2단 구조보다는 클라이언트(요청) - 중개 서버 - 중개 서버 - 중개 서버 - ... - 최종 서버(응답) 이런 다단 구조가 더 많음.  

이 때 중개 서버를 거치면서 헤더들이 변조되고, 요청을 누가 보냈는지 애매해지기도 함.  
X-Forwarded 헤더 시리즈는 원래 요청이 누구였는지를 밝혀줌(물론 이것도 공격자에 의해 조작될 수 있음)  
```
X-Forwarded-For: 1.2.3.4, 5.6.7.8, 9.10.11.12
X-Forwarded-Host: www.zerocho.com
X-Forwarded-Proto: https
```. 
For는 현재까지 거쳐온 서버의 IP에 대한 정보를 가지고 있습니다. 1.2.3.4가 원래 서버 아이피라면 나머지는 중개 서버 아이피. Host는 원래 서버의 호스트명. Proto는 원래 서버의 프로토콜.  

사실 Forwarded 헤더가 표준 헤더. 위 세 가지를 모두 처리할 수 있음.  
```Forwarded: for=1.2.3.4; host=www.zerocho.com; proto=https; by=5.6.7.8, 9.10.11.12```  

https://www.zerocho.com/category/HTTP/post/5b611b9e33b4636aa8bb1fc4  




## 참고자료  
https://velog.io/@thelm3716/HTTP-request-smuggling  
https://www.hahwul.com/2019/08/12/http-smuggling-attack-re-born/  


