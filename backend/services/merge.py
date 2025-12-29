"""
Merge Service - Stateless merge logic
All data passed in, nothing stored
"""

from typing import Optional


def analyze(current: dict, incoming: dict) -> dict:
    """
    Analyze merge and categorize changes.
    
    Args:
        current: Current memory from frontend
        incoming: New data to merge
    
    Returns:
        {
            "new": [...],
            "update": [...],
            "skip": [...],
            "summary": {"new": n, "update": n, "skip": n}
        }
    """
    result = {
        "new": [],
        "update": [],
        "skip": []
    }
    
    for key, value in incoming.items():
        entry_type = value.get("type", "") if isinstance(value, dict) else value.type
        desc = value.get("desc", "") if isinstance(value, dict) else value.desc
        
        if key not in current:
            # New entry
            result["new"].append({
                "key": key,
                "type": entry_type,
                "desc": desc
            })
        else:
            current_entry = current[key]
            current_type = current_entry.get("type", "") if isinstance(current_entry, dict) else current_entry.type
            current_desc = current_entry.get("desc", "") if isinstance(current_entry, dict) else current_entry.desc
            
            if current_desc != desc or current_type != entry_type:
                # Exists but different
                result["update"].append({
                    "key": key,
                    "type": entry_type,
                    "desc": desc,
                    "old_type": current_type,
                    "old_desc": current_desc
                })
            else:
                # Identical
                result["skip"].append({
                    "key": key,
                    "type": entry_type,
                    "desc": desc
                })
    
    result["summary"] = {
        "new": len(result["new"]),
        "update": len(result["update"]),
        "skip": len(result["skip"])
    }
    
    return result


def apply_merge(
    current: dict,
    incoming: dict,
    selected_new_keys: list[str],
    selected_update_keys: list[str]
) -> tuple[dict, dict]:
    """
    Apply merge and return new memory state.
    
    Args:
        current: Current memory
        incoming: New data
        selected_new_keys: Keys to add
        selected_update_keys: Keys to update
    
    Returns:
        (merged_memory, stats)
    """
    # Create copy of current
    merged = {}
    for key, value in current.items():
        if isinstance(value, dict):
            merged[key] = {"type": value.get("type", ""), "desc": value.get("desc", "")}
        else:
            merged[key] = {"type": value.type, "desc": value.desc}
    
    added_count = 0
    updated_count = 0
    
    for key, value in incoming.items():
        entry_type = value.get("type", "") if isinstance(value, dict) else value.type
        desc = value.get("desc", "") if isinstance(value, dict) else value.desc
        
        if key not in current and key in selected_new_keys:
            # Add new entry
            merged[key] = {"type": entry_type, "desc": desc}
            added_count += 1
        elif key in current and key in selected_update_keys:
            # Update existing entry
            merged[key] = {"type": entry_type, "desc": desc}
            updated_count += 1
    
    total_items = len(incoming)
    skipped_count = total_items - added_count - updated_count
    
    stats = {
        "added": added_count,
        "updated": updated_count,
        "skipped": skipped_count
    }
    
    return merged, stats


def validate_import_data(data: dict) -> tuple[bool, Optional[str]]:
    """
    Validate import data structure.
    
    Returns:
        (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Invalid format. Expected an object with keys."
    
    for key, value in data.items():
        if not isinstance(key, str) or not key.strip():
            return False, "Invalid key: keys must be non-empty strings."
        
        if not isinstance(value, dict):
            return False, f"Invalid entry for '{key}'. Each entry must be an object."
        
        if "type" not in value or not value["type"]:
            return False, f"Invalid entry '{key}'. Missing 'type' field."
        
        if "desc" not in value or not value["desc"]:
            return False, f"Invalid entry '{key}'. Missing 'desc' field."
    
    return True, None