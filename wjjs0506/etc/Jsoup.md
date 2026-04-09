# Jsoup

## Jsoup 이란?

자바 언어 기반 HTML 파싱 및 조작 기능을 제공하는 라이브러리

**주요 기능**
- 웹 스크래핑 및 HTML 문서처리
- 데이터 추출 및 수정

## 주로 사용하는 기능

### HTML 파싱

HTML 문서를 읽고, JAVA에서 사용할 수 있는 구조로 변환

아래와 같이 파싱할 사이트의 url을 넣어주면 DOM 구조를 추적하여 Java에서 사용가능한 Document 형식의 객체로 변환한다.

```java
// Get 방식 호출
Document doc = Jsoup.connect(url).get();

// Post 방식 호출
Document doc = Jsoup.connect(url)
                    .data("query", "Java")
                    .userAgent("Mozilla")
                    .cookie("auth","token")
                    .timeout(3000)
                    .post();
```

***참고**  
url은 http과 https만을 지원한다.

### 요소 접근

**CSS 선택자**

특정 CSS 선택자를 이용해 특정 HTML 요소를 가져올 수 있다.

```java
Elements links = doc.select("a[href]");
```

**속성 추출**

선택한 요소에 대해서 속성을 추출 할 수 있다.

```java
String href = link.attr("href");
```

**텍스트 추출**

선택한 요소에 대해서 텍스트을 추출 할 수 있다.

```java
String text = link.text();
```

**HTML 수정 및 생성**

html의 요소에 대한 수정 및 생성이 가능하다.

```java
// 속성 값 변경
link.attr("href", "newUrl");

// 요소 생성
Element temp = doc.createElement("div");
temp.text("new Element");
doc.body().appendChild(temp);
```