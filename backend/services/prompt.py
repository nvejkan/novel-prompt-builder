"""
Prompt Service - Stateless prompt building
All data passed in, nothing stored
"""

import json

DEFAULT_INSTRUCTION = (
    "Continue this story. Maintain consistency with the characters, "
    "locations, and details provided in MEMORY CONTEXT."
)

DEFAULT_EXTRACT_TYPES = ["character", "location", "item", "event"]


def build_augmented_prompt(
    story: str,
    matched_keys: list[str],
    memory: dict,
    instruction: str = None
) -> str:
    """
    Build an augmented prompt with memory context.
    
    Args:
        story: User's story input
        matched_keys: Keys to include in context
        memory: Full memory dict from frontend
        instruction: Custom instruction (optional)
    
    Returns:
        Complete augmented prompt
    """
    parts = []
    
    # Build matched entries from memory
    if matched_keys and memory:
        matched_entries = {}
        for key in matched_keys:
            if key in memory:
                entry = memory[key]
                if isinstance(entry, dict):
                    matched_entries[key] = entry
                else:
                    matched_entries[key] = {"type": entry.type, "desc": entry.desc}
        
        if matched_entries:
            parts.append("[MEMORY CONTEXT]")
            parts.append(json.dumps(matched_entries, indent=2, ensure_ascii=False))
            parts.append("")
    
    # Add story input
    if story and story.strip():
        parts.append("[STORY INPUT]")
        parts.append(story.strip())
        parts.append("")
    
    # Add instruction
    parts.append("[INSTRUCTION]")
    parts.append(instruction.strip() if instruction and instruction.strip() else DEFAULT_INSTRUCTION)
    
    return "\n".join(parts)


def build_extraction_prompt(story: str, types: list[str]) -> str:
    """
    Build a prompt for extracting data from a story.
    
    Args:
        story: Story text to extract from
        types: List of types to extract
    
    Returns:
        Extraction prompt for Gemini
    """
    if not types:
        types = DEFAULT_EXTRACT_TYPES
    
    types_list = ", ".join(types)
    
    prompt = f"""Analyze the following story and extract all {types_list}.

Return the data as a JSON object with this exact format:
{{
  "Name of Entity": {{"type": "category", "desc": "Summarized narrative description"}},
  "Another Entity": {{"type": "category", "desc": "Summarized narrative description"}}
}}

Rules:
- Use the actual name as the key
- "type" should be one of: {types_list}
- "desc" should be a summarized narrative of EVERYTHING related to the entity:

  For CHARACTERS/PERSONS:
  - Physical appearance (face, hair, eyes, body type, height, distinguishing features)
  - Clothing and accessories typically worn
  - Personality traits and temperament
  - Background and history
  - Objectives, goals, and motivations
  - Relationships with other characters
  - Skills, abilities, or powers
  - Current status or situation

  For LOCATIONS/PLACES:
  - Where it is located (geography, region, relative position)
  - What it looks like (architecture, landscape, atmosphere, colors, lighting)
  - What it is used for (purpose, function)
  - Who owns or controls it
  - Notable features or landmarks within
  - History or significance
  - Current condition or state
  - Mood or feeling it evokes

  For ITEMS/OBJECTS:
  - What it is (type of object)
  - What it looks like (size, shape, color, material, markings)
  - What makes it special or unique
  - What it does or how it functions
  - Who owns or created it
  - History or origin
  - Current location or status

  For EVENTS:
  - What happened
  - When and where it occurred
  - Who was involved
  - Why it happened (causes)
  - What were the consequences
  - Significance to the story

- Write descriptions as flowing narrative paragraphs, not bullet points
- Include ALL details mentioned in the story about each entity
- If information is not provided in the story, do not invent it
- Extract ALL relevant {types_list} mentioned in the story
- Do not include any markdown formatting, only return valid JSON

IMPORTANT: Output MUST be in the SAME LANGUAGE as the input story. 
If the story is in Thai, output in Thai.
If the story is in Japanese, output in Japanese.
If the story is in English, output in English.
Match the language of the story exactly.

Story:
{story}"""
    
    return prompt