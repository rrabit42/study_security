# PHP와 MySQL 연동  

1. Web browser에서 index.php request!  
2. Web server에서 그 요청을 받아서 확장자를 보니 ```.php```, 자기가 처리할 수 없어서 PHP라는 프로그램에게 index.php 처리를 위임  
3. PHP는 php 문법에 따라 요청을 처리  
4. PHP가 보다보니 sql문이 있음, 이것은 MySQL 서버에 sql문을 던짐  
5. MySQL 서버는 sql문을 동작시켜서 그 결과를 PHP에 알려줌  
6. PHP는 최종적으로 순수한 html 코드를 생성해서 Web Server에 넘겨줌  
7. Web Server가 Web browser에 response!  

> MySQL을 이용해 데이터를 보다 효율적으로 관리할 수 있다.  
> PHP는 이 맥락에서는 Web Server와 MySQL 서버를 이어주는 **미들웨어(Middleware)** 로서 동작하는 것.  

## MySQL  
### 기본 세팅  
* DB 생성    

```
CREATE DATABASE opentutorials;
```  

* Table 생성  
```
USE opentutorials;  // 어느 DB의 Table을 만들건지
```
```
CREATE TABLE topic (   
   id int(11) NOT NULL AUTO_INCREMENT,   
   title varchar(45) NOT NULL,   
   description text,   
   created datetime NOT NULL,   
   PRIMARY KEY(id) 
) ENGINE=InnoDB; //InnoDB가 Default라 엔진설정 안해도 자동으로 InnoDB로 설정될 것!  
```  

### PHP에서 MySQL 접속  
* php가 클라이언트로서 mysql 요청을 보내는 것!  
* 그동안 우리는 mysql monitor를 클라이언트로 mysql에 요청을 보냈었다.  

* PHP에서 MySQL API들을 제공하는데 이를 이용해 MySQL 서버에 접속할 수 있다.  
```{.php}
<?php
// mysqli
$mysqli = new mysqli("example.com", "user", "password", "database");
$result = $mysqli->query("SELECT 'Hello, dear MySQL user!' AS _message FROM DUAL");
$row = $result->fetch_assoc();
echo htmlentities($row['_message']);

// PDO(객체 사용, 다른 RDS를 사용할 때 PHP코드를 바꾸지 않고 변경 가능)
$pdo = new PDO('mysql:host=example.com;dbname=database', 'user', 'password');
$statement = $pdo->query("SELECT 'Hello, dear MySQL user!' AS _message FROM DUAL");
$row = $statement->fetch(PDO::FETCH_ASSOC);
echo htmlentities($row['_message']);

// mysql(old extension, not recommended)
$c = mysql_connect("example.com", "user", "password");
mysql_select_db("database");
$result = mysql_query("SELECT 'Hello, dear MySQL user!' AS _message FROM DUAL");
$row = mysql_fetch_assoc($result);
echo htmlentities($row['_message']);
?>
```  

#### mysqli  
* dual interface  
1. 함수를 이용해서 데이터베이스를 제어(우리가 사용) - procedural  
2. 객체를 이용해서 데이터를 제어 - object-oriented  

* mysql 서버 접속(호스트, 유저네임, 패스워드, DB이름)  
```{.php}
$connect = mysqli_connect('localhost', 'root', '111111', 'opentutorials');
```  
* DB서버에 sql문 전송하여 데이터 요청(mysqli_connect의 result, sql문)  
```{.php}
$result = mysqli_query($conn, $sql);
mysqli_query($conn, "
    INSERT INTO topic (
        title,
        description,
        created
    ) VALUES (
        'MySQL',
        'MySQL is ....',
        NOW()
    )");
```  
* mysqli_error()를 이용해 디버깅  
> mysqli_query()함수 : query문을 서버로 전송하는 함수  
> SELECT, SHOW, DESCRIBE, EXPLAIN 같은 쿼리문이 성공하면 ```mysql_result``` 객체를 return  
> 나머지 쿼리가 성공하면 TRUE return  
> 실패하면 FALSE return  

> mysqli_connect_errno() : mysql server에 접속하는 과정에서의 에러 탐지  

따라서 mysqli_error()함수는 mysqli_query(), mysqli_connect_errno()를 이용해 어떤 sql문에서 실패했는지 원인 규명을 할 수 있게 되는 것이다.  
```
<?php
$conn = mysqli_connect("localhost", "root", "111111", "opentutorials");
$sql  = "
    INSER INTO topic (
        title,
        description,
        created
    ) VALUES (
        'MySQL',
        'MySQL is ....',
        NOW()
    )";
$result = mysqli_query($conn, $sql);
if($result === false){
    echo mysqli_error($conn);
}
?>
```

최종 코드  
```{.php}
<?php
// mysql 서버 접속(호스트, 유저네임, 패스워드, DB이름)
$connect = mysqli_connect('localhost', 'root', '111111', 'opentutorials');


// DB서버에 sql문 전송하여 데이터 요청(msqli_connect의 result, sql문)
$sql = "SELECT * FROM topic";
$result = mysqli_query($conn, $sql);

// 받은 데이터로 요청 처리
$list = '';
while($row = mysqli_fetch_array($result)){
  $list = $list."<li><a href=\"index.php?id={$row['id']}\">{$row['title']}</a></li>";
}
?>
```  

### 데이터 생성(INSERT)  
```{.php}
<?php
$conn = mysqli_connect(
  'localhost',
  'root',
  '111111',
  'opentutorials');
$sql = "
  INSERT INTO topic
    (title, description, created)
    VALUES(
        '{$_POST['title']}',
        '{$_POST['description']}',
        NOW()
    )
";
$result = mysqli_query($conn, $sql);
if($result === false){
  echo '저장하는 과정에서 문제가 생겼습니다. 관리자에게 문의해주세요';
  error_log(mysqli_error($conn));
} else {
  echo '성공했습니다. <a href="index.php">돌아가기</a>';
}
?>
```  

### 데이터 읽어오기(SELECT)  
```{.php}
<?php
$conn = mysqli_connect(
  'localhost',
  'root',
  '111111',
  'opentutorials');
$sql = "SELECT * FROM topic";
$result = mysqli_query($conn, $sql);
var_dump($result->num_rows);
```  
* **지시자(->, object operator)** 를 이용하여 객체의 속성에 접근  
```
// Create a new instance of MyObject into $obj
$obj = new MyObject();

// Set a property in the $obj object called thisProperty
$obj->thisProperty = 'Fred';

// Call a method of the $obj object named getProperty
$obj->getProperty();
```
* 참고로 **=>(double arrow operator)** 는 배열의 값을 지정할 때 쓴다.  
```{.sql}
$myArray = array(
    0 => 'Big',
    1 => 'Small',
    2 => 'Up',
    3 => 'Down'
);

// 연관 배열: 인덱스를 문자열로 사용하여 그 값에 의미를 붙여 사용하는 방식
$prices = array(
    'Tires'=>100,
    'Oil'=>10,
    'Spark Plugs'=>4
);
```

#### mysqli_fetch_array  
* mysql 서버가 응답한 결과를 php 배열로 변환  
* mysqli_fetch_* : 결과를 php 타입으로 변환해서 사용할 수 있게 도움  
```{.php}
<?php
$conn = mysqli_connect(
  'localhost',
  'root',
  '111111',
  'opentutorials');
$sql = "SELECT * FROM topic WHERE id = 19";
$result = mysqli_query($conn, $sql);
$row = mysqli_fetch_array($result);

// column의 이름을 통해 데이터를 가져옴: 연관배열, 인덱스를 통해 가져옴: (default)배열 
echo '<h1>'.$row['title'].'</h1>';
echo $row['description'];
```  
* 배열 출력:  
```
print_r(mysqli_fetch_array($result));
```  
* 여러 행 가져오기  
```{.php}
<?php
$conn = mysqli_connect(
  'localhost',
  'root',
  '111111',
  'opentutorials');
  
echo "<h1>single row</h1>";

$sql = "SELECT * FROM topic WHERE id = 19";
$result = mysqli_query($conn, $sql);
$row = mysqli_fetch_array($result);

echo '<h2>'.$row['title'].'</h2>';
echo $row['description'];
echo "<h1>multi row</h1>";

$sql = "SELECT * FROM topic";
$result = mysqli_query($conn, $sql);

// while문을 돌 때마다 다음 행(row, 데이터)을 읽어옴  
while($row = mysqli_fetch_array($result)) {
  echo '<h2>'.$row['title'].'</h2>';
  echo $row['description'];
}
```  

### 보안  
#### 입력 공격의 차단  
* 입력 공격 차단 - filtering  
```
$filtered_id = mysqli_real_escape_string($_GET['id']);  
```
* 출력 공격 차단 - escaping  

#### SQL injection 차단(입력 공격)  
```mysqli_multi_query($conn, $sql);``` : 복수의 sql문을 실행시켜주지만 보안적인 문제가 아주 많음  

ex)
```{.sql}
// 일반 sql문
INSERT INTO topic(title, description, created) VALUES('Hehe', 'haha', NOW() )

// 공격(시간을 NOW()가 아닌 내가 설정한 시간으로)
// ; 으로 끝나고 뒤에 '--'를 이용해 NOW()를 주석처리 시킨다.
INSERT INTO topic(title, description, created) VALUES('Hehe', 'haha', '2018-1-1 00:00:00');-- ', NOW() )
```  
즉, 화면의 input에서 description 입력할 때 **haha', '2018-1-1 00:00:00');** 이렇게 쓰면 저렇게 sql문이 생성되서 들어가는것! 다중 sql문 입력을 허용할 때 이 공격이 가능하다.  

따라서 ```mysqli_query();```를 쓰자!  

#### Cross site scripting 차단(출력 공격)  
```htmlspecialchars()``` 함수를 이용해 <script> tag 등 문법적인 역할이 있는 문자들을 해석하지 않고 그대로 출력해준다.  
   ex) <,> -> &lt, &gt





