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

## 함수  

> php는 웹을 위한 언어이기 때문에 웹에서 사용할만한 여러가지 기능을 제공  
> 따라서 줄바꿈 <br> 태그 대신 nl2br()함수를 사용할 수 있다.  
> ```nl2br() : Inserts HTML line breaks before all newlines in a string```  

```
...
    <?php
      $str = "Lorem ipsum dolor sit amet, consectetur adipisicing elit.
      <br>
      sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.";
      echo $str;
    ?>
...
    <?php
      echo strlen($str);
     ?>
...
    <?php
      echo nl2br($str);
    ?>
...
```  

> ```file_get_contents() : Reads entire file into a string```  

```
...
  <body>
    <h1>WEB</h1>
    <ol>
      <li><a href="index.php?id=HTML">HTML</a></li>
      <li><a href="index.php?id=CSS">CSS</a></li>
      <li><a href="index.php?id=JavaScript">JavaScript</a></li>
    </ol>
    <h2>
      <?php
        echo $_GET['id'];
      ?>
    </h2>
    <?php
      echo file_get_contents("data/".$_GET['id']);
     ?>
  </body>
...
```  

## 비교 연산자  

### [Comparison Operators](https://www.php.net/manual/en/language.operators.comparison.php)  
|Example|Name|Result|
|:---:|:---:|:---:|
|$a == $b|Equal|TRUE if $a is equal to $b after type juggling(자동 형변환).|
|$a === $b|	Identical|TRUE if $a is equal to $b, and they are of the same type.|
|$a != $b|Not equal|TRUE if $a is not equal to $b after type juggling.|
|$a <> $b|Not equal|TRUE if $a is not equal to $b after type juggling.|
|$a !== $b|Not identical|TRUE if $a is not equal to $b, or they are not of the same type.|
|$a < $b|Less than|TRUE if $a is strictly less than $b.|
|$a > $b|Greater than|TRUE if $a is strictly greater than $b.|
|$a <= $b|Less than or equal to|TRUE if $a is less than or equal to $b.|
|$a >= $b|Greater than or equal to|TRUE if $a is greater than or equal to $b.|
|$a <=> $b|Spaceship|An integer less than, equal to, or greater than zero when $a is less than, equal to, or greater than $b, respectively. Available as of PHP 7. (즉, $a - $b 값을 돌려준다)|


### [Type Juggling](https://blog.lael.be/post/1993)    
= 자동 자료형변환 = Auto Typecasting = Implicit Typecasting  

php는 엄청난 Type Juggling을 자랑한다.  
> if 및 while 구문에서 괄호 안에는 boolean 값이 나와야 한다. 1 은 boolean 값이 아니기 때문에 자동형변환이 일어난다. 1 은 true 로 변환되고, 2 도 true 로 변환되고, 0 은 false 로 변환된다. (0 이외의 값은 true 이다.)
> 즉, PHP에서는 while(1), while(true), while(‘hello’), while(object 변수), while(resource 변수) 모두 동일한 동작을 한다.  

```
ex. 
<?php
$_GET['countdown'] = '10';
$my_countdown = $_GET['countdown'];
for ($i = $my_countdown; $i >= 0; $i--) {
  var_dump($i);
  echo $i . " gogo!\n\n";
}
?>
```  
```
// 결과
string(2) "10"
10 gogo!

int(9)
9 gogo!

int(8)
8 gogo!
...
```  
> 변환 연산을 위해서 임시로 변한 것일 뿐 해당 값에는 변화가 없다.  즉 intval(’10’) >= 0  이 실행된 것이다.  
> echo 문을 만나면 $i 가 string 10인 경우를 제외하고는 echo strval($i) . ” gogo!” 가 실행된 것이다.  

```
<?php
$_GET['dollar'] = '150 달러';
$my_dollar = $_GET['dollar'];
$my_won = $my_dollar * 1100;
echo 'KRW : ' . $my_won . ' WON';
?>
```  
> $my_won = intval($my_dollar) * 1100;    이라는 구문으로 변환되어 실행되어 버린다.  
> intval(‘150 달러’) 는 integer 형 150 과 같다.  

* PHP 의 Type Juggling 에 대해 숙지(어려움)하고, 되도록 엄격한(strict) 코드를 작성하길 바란다. 엄격한 코딩을 위해서, 변수는 정보를 얻자마자 형태를 고정시키고 필터링 하는 것이 좋다.  


* var_Dump() : 변수의 정보를 출력하는 함수  
```var_dump( $var1, $var2, ... );```  
> ```int(1)``` : 정수이고, 값은 1입니다.  
> ```float(1.1)``` : 실수이고, 값은 1.1입니다.  
> ```string(5) "hello"``` : 5개의 문자로 이루어진 문자열이고, 값은 hello입니다.  
> ```array(2) { [0]=> int(1) [1]=> float(1.1) }``` : 2개의 값을 가진 배열이고, 첫번째 값은 정수 1, 두번째 값은 실수 1.1입니다.  
> ```bool(true)``` : boolean이고, 값은 true입니다.  


## 조건문  
프로그래밍은 시간의 순서에 따라, 위에서 아래로 순차적으로 실행된다는 것을 기억해라!  
```
if(expression)
	statement
```  

```
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>
    <h1><a href="index.php">WEB</a></h1>
    <ol>
      <li><a href="index.php?id=HTML">HTML</a></li>
      <li><a href="index.php?id=CSS">CSS</a></li>
      <li><a href="index.php?id=JavaScript">JavaScript</a></li>
    </ol>
    <h2>
      <?php
      if(isset($_GET['id'])){
        echo $_GET['id'];
      } else {
        echo "Welcome";
      }
      ?>
    </h2>
    <?php
    if(isset($_GET['id'])){
      echo file_get_contents("data/".$_GET['id']);
    } else {
      echo "Hello, PHP";
    }
     ?>
  </body>
</html>
```  
* isset() : Determine if a variable is set and is not NULL  

## 반복문  
```
while(expression)
	statement
```  

```
...
    <?php
    echo '1<br>';
    $i = 0;
    while($i < 3){
      echo '2<br>';
      $i = $i + 1;
    }
    echo '3<br>';
     ?>
...
```  

## 배열  

```
...
    <?php
    $coworkers = array('egoing', 'leezche', 'duru', 'taeho'); // 배열의 표현식
    echo $coworkers[1].'<br>';
    echo $coworkers[3].'<br>';
    var_dump(count($coworkers));
    array_push($coworkers, 'graphittie');  // 배열의 원소 추가
    var_dump($coworkers);
    ?>
...
```
