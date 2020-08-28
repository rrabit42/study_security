# PHP for web app  
_php는 web app을 위해 고안된 언어_  

## URL 파라미터  
php app의 입력으로서 URL 파라미터(querystring, 쿼리스트링)를 사용하는 방법을 알아보자!  

* url에 ? 뒤에 파라미터를 주면 된다. 즉, ?key=value 쿼리스트링을 주면 됨  
* 여러개의 key를 넘겨주려면 &사용  
```ex. ?key1=value1&key2=value2```  
* 그리고 그걸 $_GET['key'] 인자로 받아온다  
```ex. 127.0.0.1/parameter?name=egoing```  

```
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
  </head>
  <body>
    안녕하세요. <?php echo $_GET['address']; ?>에 사시는 <?php echo $_GET['name']; ?>님
  </body>
</html>
```  

* 응용  
```
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>
    <h1>WEB</h1>
    <ol>
      <li><a href="index.php?id=HTML">HTML</a></li>
      <li><a href="index.php?id=CSS">CSS</a></li>
      <li><a href="index.php?id=JavaScrit">JavaScript</a></li>
    </ol>
    <h2>
      <?php
        echo $_GET['id'];
      ?>
    </h2>
    Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
  </body>
</html>
```  

## form  
### GET 방식  
* 메세지 header를 통해서만 전달  
* request라인의 URI 필드를 통해서 전달("?"를 구분자로 사용, 변수명과 값을 쌍으로 전달, 여러 데이터는 "&"로 구분)  
ex. http://127.0.0.1/index.php?title=php&author=kim  
* 전달할 수 있는 데이터 크기에 한계가 있음(헤더의 크기를 넘어갈 수 없다.)  
* 전달하려는 데이터가 외부에 노출되어서 보안상 취약하다.  
* ```Value = $_GET["변수명"]```  

### POST 방식  
* 메세지 body를 통해서 전달  
* 전달하려는 데이터의 크기 제한이 없다. 따라서 복잡한 형태의 자료를 전달할 때 유용하다.(스트림 형태로 전송되기 때문)  
* 전달하려는 데이터가 외부에 쉽게 노출되지 않는다.(GET과 달리 입력한 데이터가 URL 상에 보이지 않는다)  
* 반드시 form tag와 함께 쓰인다.  
* ```Value = $_POST["변수명"]```  

```
<!doctype html>
<html>
  <body>
    <form action="form.php" method="post">
      <p><input type="text" name="title" placeholder="Title"></p>
      <p><textarea name="description"></textarea></p>
      <p><input type="submit"></p>
    </form>
  </body>
</html>
```  

## 파일 모듈화  
자주 사용하는 특정 코드를 외부 php 파일로 분리하여 그 파일을 코드 안으로 불러와서 사용하는 것  
* 자주 사용되는 코드를 별도의 파일로 만들어서 필요할 때마다 재활용할 수 있다.  
* 코드를 개선하면 이를 사용하고 있는 모든 애플리케이션의 동작이 개선된다.  
* 코드 수정 시에 필요한 로직을 빠르게 찾을 수 있다.  
* 필요한 로직만을 로드해서 메모리의 낭비를 줄일 수 있다.  

즉, 코드의 재활용성을 높이고, 유지보수를 쉽게할 수 있다.  

### 로드 방법
PHP에서는 필요에 따라서 다른 PHP 파일을 코드 안으로 불러와서 사용할 수 있다.  
* include  
include는 외부의 php 파일을 로드할 때 사용하는 명령이다.  

```
<?php
include 'greeting.php';
echo welcome();
?>
```  

* include_once  
* require  
* require_once  

> include와 require의 차이점은 존재하지 않는 파일의 로드를 시도했을 때 include가 warning를 일으킨다면 require는 fatal error를 일으킨다는 점이다. fatal error는 warning 보다 심각한 에러이기 때문에 require가 include 보다 엄격한 로드 방법이라고 할 수 있다.  

> _once라는 접미사가 붙은 것은 파일을 로드 할 때 단 한번만 로드하면 된다는 의미다.  

## XSS(Cross site scripting)  

PHP에서 XSS를 방지하기 위한 두 가지 함수가 있다.  
사용자가 값을 입력하는 부분을 모두 이 함수들로 감싸주면된다.  

* htmlspecialchars() : 꺽쇠(<,>)를 html tag로 해석하지 않고, html에서 꺽쇠를 그대로 화면에 출력해주는 &lt, &gt로 해석함! 따라서 script가 그대로 출력된다.  
그러나 정말 필요한 내용도 날려버리기에 아래 함수를 주로 이용한다.  
* strip()_tags : 문자열에서 html 태그와 php 태그를 제거한다.  



```
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>XSS</title>
  </head>
  <body>
    <h1>Cross site scripting</h1>
    <?php
    echo htmlspecialchars('<script>alert("babo");</script>');
    ?>
  </body>
</html>
```  


## 파일 경로 보호  

공격자는 URL를 통해 민감한 파일의 내용을 볼 수 있도록 공격 할 수 있다.  
보호 방법은 아래와 같다.  
```
<?php
function print_description(){
  if(isset($_GET['id'])){
    $basename = basename($_GET['id']);
    echo htmlspecialchars(file_get_contents("data/".$basename));
  } else {
    echo "Hello, PHP";
  }
}
?>
```  
```
<?php
  unlink('data/'.basename($POST['id']); // id값을 받아서 해당 id에 해당하는 파일만 열 수 있도록!
  header('Location: /index.php'); // redirect
?>
```  
