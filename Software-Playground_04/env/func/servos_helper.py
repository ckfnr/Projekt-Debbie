def add_until_limit(start: int, increment: int, limit: int) -> int:
    result: int = start + increment
    return limit if (increment > 0 and result > limit) or (increment < 0 and result < limit) else result
