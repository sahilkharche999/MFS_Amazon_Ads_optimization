import json


def parse_ai_json(raw):
    try:
        return json.loads(raw)
    except:
        cleaned = raw.strip()
        cleaned = cleaned.replace("```json", "").replace("```", "")
        return json.loads(cleaned)
