# 완주하지 못한 선수

## 문제정보

- 사이트 : pg (프로그래머스 코딩테스트 사이트)
- 문제 번호 : 1845
- 문제 분류 : Map
- 난이도 : level 1

## 문제 풀이

### 생각한 문제 조건

1. 자료형 제한 조건
   - 1<= participant <= 100,000
   - completion : participant - 1
2. 용어 정의
3. 문제의 다른 조건

   - 동명이인이 있을 수 있다.

   > **💬 생각 노트**
   > 해당 자료형에 있는 지 없는 지 찾는 것이므로 배열보단 Map을 선택하였다.
   > 동명이인이 있을 수 있으니 map의 value 값을 통해 완주한 사람을 구분하였다.

### 내가 짠 코드

```java
import java.util.HashMap;

public class PG42576 {

    public static void main(String[] args) {
        String[] participant = {"leo", "kiki", "eden"};
        String[] conpletion = { "eden", "kiki"};
        System.out.println(solution(participant, conpletion));
    }

    public static String solution(String[] participant, String[] completion) {
        String answer = "";
        HashMap<String, Integer> map = new HashMap<>();
        for (String s : participant) {
            map.put(s, map.getOrDefault(s, 0) + 1);
        }
        for (String s : completion) {
            if (map.containsKey(s)) {
                if(map.get(s) > 1) {
                    map.put(s, map.get(s) - 1 );
                } else {
                    map.remove(s);
                }
            }
        }

        for (String s : map.keySet()) {
            answer = s;
            break;
        }
        return answer;
    }
}
```

## 의문점 및 개선 한 코드

completion이 무조건 participant에 있고 갯수가 1개 작으니 아래 코드와 같이 개선이 가능하다

```java
public String solution(String[] participant, String[] completion) {
        HashMap<String, Integer> map = new HashMap<>();

        // 1. 모든 참가자 카운트업 (+)
        for (String p : participant) map.put(p, map.getOrDefault(p, 0) + 1);

        // 2. 완주자 카운트다운 (-)
        for (String c : completion) map.put(c, map.get(c) - 1);

        // 3. 값이 0이 아닌(1인) 사람 찾기
        for (String key : map.keySet()) {
            if (map.get(key) != 0) return key;
        }
        return "";
    }
```

## 참고
