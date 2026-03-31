
from typing import Dict, List
from utils import normalize_title, record_title


def linear_search(records: List[Dict[str, str]], query: str) -> List[Dict[str, str]]:
    normalized_query = normalize_title(query)
    matches = []
    for record in records:
        if normalize_title(record_title(record)) == normalized_query:
            matches.append(record)
    return matches
