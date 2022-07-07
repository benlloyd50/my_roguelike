
def is_null_or_space(_str: str) -> bool:
    """Returns True if `_str` is empty string or any amount of whitespace"""
    return _str == "" or _str.isspace()

def clamp(n, minn, maxn):
    """Returns the value `n` in the range of `minn` to `maxn`"""
    return max(min(maxn, n), minn)