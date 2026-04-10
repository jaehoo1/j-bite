# Jar & War

**목차**  
[들어가기 전](#자바-웹-어플리케이션)  
[1.Servlet](#Servlet)  
[2.작성방법](#작성방법)

## Jar (Java Archive)

Jar는 여러 클래스와 리소스를 묶어서 압축한 파일이다.  
JVM 위에서 직접 실행되거나 다른 곳에서 사용하는 라이브러리(모듈)의 형태로 제공된다.

> [Jar 직접 실행할 경우]
>
> 1. `main()` 메소드가 필요하다.
> 2. `MANIFEST.MF` 파일에 실행할 메인 메서드가 있는 클래스를 지정해 두어야 한다.  
>    ![MANIFEST 사진](/assets/images/wjjs0506/spring/jar_&_war/manifest.png)

## War (Web Application Archive)

이름대로 Web Application을 위한 압축 파일로 Jar의 클래스와 리소스 외에 HTML과 같은 정적 리소스 및 웹 어플리케이션 실행에 필요한 설정 파일 및 라이브러리 등을 포함하고 있다.

Jar가 JVM 위에서 실행되듯이, War는 웹 어플리케이션 서버(tomcat 등) 위에서 실행된다.

[War의 구조]

- WEB-INF
  - classes : 실행 클래스 모음
  - lib : 라이브러리 모음
  - web.xml : 웹 서버 배치 설정 파일 (생략 가능, servlet3.0 이상 -> Annotation으로 사용 가능)
- index.html : 정적 리소스
