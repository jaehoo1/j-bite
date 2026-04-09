# 자신의 row 비교

## 문제 정보

- 사이트 : leetcode.com
- 문제 번호 : 180
- 문제 제목 : Consecutive Numbers
- 문제 요약 : 하나의 테이블 Logs에서 column num이 3번 이상 연속해서 나오는 수 찾기 (중복 제거)
- 나의 결과 : 수행 시간 495ms, Beats율 : 79.41%
- 강의 수강 후 개선 결과 : 485ms, Beats율 : 86.58%

## 접근 방법

1. 연속한 column의 자신의 값 비교 -> 자기자신 join
2. 자기 자신 join을 2번 진행해서 num 값이 다 같은 경우 출력

```
select DISTINCT l3.num as ConsecutiveNums
from Logs l3
    inner join (select l1.id as l1_id, l1.num as l1_num, l2.num as l2_num
                from Logs l1
                    inner join Logs l2 on l1.id = l2.id + 1) sub on l3.id = sub.l1_id + 1 and sub.l1_num = sub.l2_num
where sub.l1_num = sub.l2_num
    and sub.l2_num = l3.num
```

## 강의 개선 방법

- 서브 쿼리 형식의 방법을 한번에 inner join을 3테이블 하는 방법으로 변경

```
select DISTINCT l3.num as ConsecutiveNums
from Logs l1
    inner join Logs l2 on l1.id + 1 = l2.id and l1.num = l2.num
    inner join Logs l3 on l1.id + 2 = l3.id and l1.num = l3.num
```
