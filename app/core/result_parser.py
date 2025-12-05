from typing import List


def parse_result_lines(raw: str) -> List[str]:
    """Basic parser stub that splits on newlines."""
    return [line.strip() for line in raw.splitlines() if line.strip()]

