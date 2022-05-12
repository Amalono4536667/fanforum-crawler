from typing import Optional


def join(data: list, default_value=None) -> Optional[str]:
    tmp = ''.join(data).strip()
    return tmp if tmp else default_value
