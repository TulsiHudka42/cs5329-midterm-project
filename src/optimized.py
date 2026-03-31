
from typing import Dict, List
from utils import normalize_title, record_title


def build_index(records: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    index: Dict[str, List[Dict[str, str]]] = {}
    for record in records:
        key = normalize_title(record_title(record))
        index.setdefault(key, []).append(record)
    return index


def indexed_search(index: Dict[str, List[Dict[str, str]]], query: str) -> List[Dict[str, str]]:
    return index.get(normalize_title(query), [])
