import json
import re

def parse_raw_output(raw_output: str, state: dict):
    # Extract the first {...} JSON block
    match = re.search(r"\{[\s\S]*\}", raw_output)
    if match:
        json_str = match.group(0)
    else:
        json_str = "{}"

    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError:
        parsed = {"intent": "chat", "params": {}}

    return {**state, "intent": parsed.get("intent", "chat"), "params": parsed.get("params", {})}