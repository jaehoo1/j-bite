def solution(my_string: str, is_prefix: str) -> int:
    if my_string.find(is_prefix) == 0:
        return 1
    return 0