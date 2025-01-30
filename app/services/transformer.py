import hashlib
import json
from typing import List


def generate_hash(list_1: List[str], list_2: List[str]) -> str:
    """Generate a unique hash for the input lists."""
    combined = json.dumps([list_1, list_2], sort_keys=True)
    return hashlib.sha256(combined.encode()).hexdigest()


def transform_string(s: str) -> str:
    """Simulate an external service transformation."""
    return s.upper()


def interleave_lists(list_1: List[str], list_2: List[str]) -> str:
    """Interleave two lists of strings."""
    result = []
    for s1, s2 in zip(list_1, list_2):
        result.extend([s1, s2])
    return ", ".join(result)
