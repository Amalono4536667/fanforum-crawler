from typing import Optional


def join(data: list) -> Optional[str]:
    tmp = ''.join(data).strip()
    return None if not tmp else tmp
