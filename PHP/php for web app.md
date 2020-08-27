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
