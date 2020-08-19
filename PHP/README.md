# PHP  

## PHP의 원리

* 웹브라우저에서 index.html을 적어줌  
이 요청을 받은 웹서버(우리는 아파치)는 확장자인 html을 보면 이걸 직접 처리할 수 있다는걸 알아서  
서버 컴퓨터의 하드디스크나 ssd에 설치되어있는 htdocs디렉토리 안의 index.html 파일을 읽어서 웹브라우저에게 전송  
웹브라우저는 그 코드의 내용을 분석해서 화면에 표현해줌  
=> 언제나 똑같은 정보를 보여줌(정적)  


* 웹브라우저에서 index.php를 적어줌  
웹서버는 확장자가 php인건 자기 소관이 아니라는걸 앎  
그래서 php를 처리할 수 있는 php라는 프로그램에게 위임한다.  
php라는 프로그램은 htdocs라는 디렉토리 안의 index.php파일을 열어서 이걸 php 문법에 따라 해석해서 최종적으로 html 파일을 생산해냄.  
이 html파일을 웹서버가 웹브라우저에게 전송  
=> php가 <?php ... ?> 안에 있는 문법을 해석할 때마다 리로드할 때 마다 그 안에 있는 정보가 달라질 수 있음(동적으로 정보 생성)  
=> php가 해석하기 원하면 저 꺽쇄안에 반드시 넣어줘야함!  


## PHP의 데이터 타입  
https://www.php.net/manual/en/language.types.intro.php  


* Number & Arithmetic Operator  
숫자와 산술 연산자  

```
<!doctype html>
<html>
<body>
  <h1>Number & Arithmetic Operator</h1>
  <h2>1+1</h2>    // html은 연산자 계산하지 않고 그대로 출력
  <?php
    echo 1+1;     // 2
  ?>
  <h2>2-1</h2>
  <?php
    echo 2-1;     // 1
  ?>
  <h2>2*2</h2>
  <?php
    echo 2*2;     // 4
  ?>
  <h2>4/2</h2>
  <?php
    echo 4/2;     // 2
  ?>
</body>
</html>
```  

* Number & Arithmetic Operator  
문자열과 문자열의 처리  

```
<!doctype html>
<html>
<body>
  <h1>String & String Operator</h1>
  <?php
    echo "Hello \"w\"ord";
  ?>
  <h2>concatenation operator</h2>
  <?php
    echo "Hello "."world";        // 문자열 결합, concatenation operator
  ?>
  <h2>String length function</h2>
  <?php
    echo strlen("Hello world");   // 문자열의 길이
   ?>
</body>
</html>
```  

+ single quote('')와 double quote("")의 차이  
```
<?php
 // 변수삽입
 $name = "friday"; //삽입 될 변수
 $single = 'Hello $name';
 $double = "Hello $name"; //가독성을 위해 보통 "Hello {$name}" 처럼 사용
 
 echo $single;
 echo "<br/>";
 echo $double;
 
 //결과
 //Hello $name
 //Hello friday
 
 
 $single = 'Hello\n';
 $double = "Hello\n";
 
 echo $single;
 echo "<br/>";
 echo $double;
 
 //결과
 //Hello\n
 //Hello
?>
```  
> 이러한 결과는 PHP 내부적으로 문자열 처리 시 single quote는 입력된 내용을 모두 문자열로 처리하는 반면  
> double quote는 파싱이 필요한 데이터가 있는지 확인 후 변환하는 과정을 거처 문자열로 처리하게 되면서 나타나게 된다.  
> 즉, single quote는  있는 그대로 문자열로 처리, double quote 변환 작업 후 문자열로 처리 되는 특성을 가지고 있다.  

## 변수  
변수 이름 앞에 $를 붙인다.  

```
<!DOCTYPE html>
<html>
  <body>
    <h1>Variable</h1>
    <?php
    $name = "leezche";
    echo "Lorem ipsum dolor sit amet, consectetur ".$name." adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco ".$name." laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore egoing eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. by ".$name;
    ?>
  </body>
</html>
```  

