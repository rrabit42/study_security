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
