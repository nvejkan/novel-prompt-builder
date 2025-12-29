"""
Search Service - Stateless keyword matching
Memory is passed in, not stored
"""


def find_matches(text: str, memory: dict) -> list[str]:
    """
    Find all exact key matches in text.
    
    Args:
        text: Text to search in
        memory: Memory dict from frontend {key: {type, desc}}
    
    Returns:
        List of matched keys sorted by first occurrence position
    """
    if not text or not memory:
        return []
    
    keys = list(memory.keys())
    matches = []
    
    for key in keys:
        # Exact match - case sensitive
        if key in text:
            matches.append(key)
    
    # Sort by position in text (first occurrence)
    matches.sort(key=lambda k: text.index(k))
    
    return matches