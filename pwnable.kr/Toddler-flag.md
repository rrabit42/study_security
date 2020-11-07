# Toddler's Bottle - flag  

## 문제 설명  
<img width="446" alt="1" src="https://user-images.githubusercontent.com/46364778/98448635-c7f97400-2170-11eb-8980-c4d73593299e.PNG">  



## 문제 풀이  
0.  
```wget http://pwnable.kr/bin/flag```를 통해 파일을 다운받자. (나는 칼리리눅스 환경임)  

1.  
packed된 선물을 줬으니 풀어봐야 할 것 같다.  
실행 권한이 없길래 chmod를 통해 권한을 주고 일단 실행 시켜봤다.  
```
chmod 777 ./flag
./flag
```  
그랬더니  
```
I will malloc() and strcpy the flag there. take it.
```  
이라고 나온다. 대충 자기 분석하면 flag 나올거니 알아서 하라는 것 같다.  

2.  
gdb 돌려봤는데 아무것도 안나온다!  
그렇다! packed 되어 있다고 했는데 풀어줘야 한다니까?!  
악성코드 수업에서 packing 방식이 여러개가 있다고 했으니 얘가 어떤 방법으로 packing 되어 있는지 알아야 할 것 같다.  

구글링해보니 packing 방식 알 수 있는 툴도 있고 여러 방법이 있는데,  
포렌식 수업에서 사용한 **HxD** 도구를 이용해서 대충 구조를 보자.  

<img width="486" alt="2" src="https://user-images.githubusercontent.com/46364778/98448781-0c394400-2172-11eb-9d2b-c42a3e21f39a.PNG">  

ELF 파일 형식이고 UPX로 패킹되어 있음을 알 수 있다.  

3.  
UPX 언패킹하는 방법을 또 구글링해보았다.  
[http://upx.github.io/]() 에서 UPX packer를 다운받자.  
```
// unpacking 하는 법
upx -d [파일명]
upx -d [파일명] -o [다른 이름으로 저장할 때]
```  

4.  
이제 gdb를 통해 돌려보자!  
<img width="411" alt="3" src="https://user-images.githubusercontent.com/46364778/98449044-bf566d00-2173-11eb-966b-8117a36a0f75.PNG">  

### (방법1)  
보니까 <+32>에 flag 값을 옮긴다고 나와있다. flag은 0x6c2070에 저장되어 있다.  
```
x/s 0x6c2070
```  
하면 ```(fI``` 라는 문자열이 나온다. 혹시나해서 사이트에 입력해봤는데 오답!  
그럼 이게 flag가 아닌가보다.  
그래서 아래와 같이 메모리를 봤다.  
```
x/4wx 0x6c2070
```  
을 해보면 해당 주소에 ```0x00496628``` 이 저장되어 있음을 알 수 있다.  
그렇다면 이를 다시 한번 검색해보자  
```
x/4wx 0x00496628
```  
그러면 ```UPX...? sounds like a delivery service :)```라는 플래그가 나온다!  

+)  
```
x/s *0x6c2070
```  
걍 이렇게 바로 참조하고 있는 값 출력  

### (방법2)  
call을 두번 해주는데 한번은 malloc이고 하나는 strcpy일 것이다.  
지금 strcpy를 해주기 앞서서 rax에 있는 값을 rdi(Destination index 레지스터)로 옮기고 있다.  
즉, rax에 flag 값이 저장되어 있는 것이다.  

```
b *main+49
```  
strcpy하기 전에 break를 걸고,  
```
info reg rax
```  
0x6c96b0이 나오는데 이 곳이 가리키는 데이터를 복사할 것이라는 뜻이다.  
```
x/24x 0x6c96b0
```  
이 주소를 보면 뭔가가 채워져 있는데 string으로 보자.  
```
x/24s 0x6c96b0
```

flag가 출력된다!!  


### (방법3)  
<+32>에서 flag값을 옮기므로 <+39>에는 옮겨진 flag 값이 rdx에 저장되어 있을 것이다!  
따라서 39번째에 브레이크를 걸고 실행시켜보자.  
```
b *main+39

// 그리고 rdx 값을 확인해보자  
info reg 혹은 infor register $rdx
```  
그리고 실행시키면 플래그가 나온다!는데 저 화면이 뭔지 모르겠어서 [링크](https://pororiri.tistory.com/entry/pwnablekrflag%EB%A6%AC%EB%88%85%EC%8A%A4-upx-%EC%96%B8%ED%8C%A8%ED%82%B9) 첨부해둔다.    

* **0x6c2070 flag 설명**  
flag가 어딘가에 저장되어 있고 그것을 malloc()한 곳에 strcpy() 시킨다.  
rip는 다음 실행될 code text의 주소이다. 즉 program counter 인듯.  
```rip+0x2c0ee5``` 가 flag가 저장되어 있는 곳을 가리키고 있다. rip는 0x40118b이므로  
0x40118b + 0x2c0ee5 = 0x6c2070 즉, flag은 0x6c2070가 가리키는 곳이다.  

* gdb말고 ida를 이용하면 더 쉬워보인다카더라  

## 공부  
### Binary Packing  
실행 압축. 바이너리 패킹은 바이너리 디스어셈블을 방지하기 위한 리버싱 방지 기법이다.  
압축을 푸는 과정 업싱 일반 프로그램처럼 바로 실행이 가능하다.  
패킹이 되어 있는 바이너리는 원본 코드 분석을 할 수 없기 때문에 언패킹을 진행해줘야 한다.  
종류에는 UPX, Upack, ASPack, Petite, MEW, MPress, KKrunchy, RLPack Basic, FSG 1.33, FSG 2.0, nPack 등이 있다.  

참고자료: https://manggoo.tistory.com/3  
