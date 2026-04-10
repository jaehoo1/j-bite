# 폰켓몬

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

### 내가 짠 코드

```java
import java.util.HashSet;

public class PG1845 {

    public static void main(String[] args) {
        int[] nums = {3,3,3,2,2,2};
        solution(nums);
    }

    public static int solution(int[] nums) {
        int answer = 0;
        HashSet<Integer> set = new HashSet<Integer>();
        for (Integer i : nums) {
            set.add(i);
        }
        answer = Math.min(nums.length / 2, set.size());
        return answer;
    }
}
```

## 의문점 및 개선 한 코드

1. HashSet 리사이징 개선

HashSet은 내부적으로 배열을 사용하기 때문에 크기 변경('리사이징')이 어려워 nums의 크기를 아는 경우 `HashSet<Integer> set = new HashSet<Integer>();`과 같은 코드보단 `HashSet<Integer> set = new HashSet<>(nums.length)`와 같은 코드로 초기 용량을 잡아주는 것이 성능에 이점이 많다.

2. 코드 개선 (명확한 한줄)

```Java
int answer = 0;
        HashSet<Integer> set = new HashSet<Integer>();
        for (Integer i : nums) {
            set.add(i);
        }
        answer = Math.min(nums.length / 2, set.size());
        return answer;
```

와 같은 코드를 `return (int) Math.min(nums.length / 2, Arrays.stream(nums).distinct().count());` 이와 같이 표현 가능하다.

한 줄로 만드는 것이 무조건 좋은 것은 아니지만(실제로 내가 짠 방식이 속도 면에선 더 빠를 때가 많기도 하다) 두 방식 모두 알아 둘 것!

## 참고
