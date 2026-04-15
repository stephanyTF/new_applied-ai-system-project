import os
import json
from datetime import date, timedelta

import google.genai as genai

GEMINI_MODEL_NAME = "gemma-3-1b-it"


def generate_pet_tasks(pets: list, api_key: str = None) -> list:
    """
    Use Gemini (gemma-3-1b-it) to generate 3 task suggestions per pet.

    Returns a list of dicts with keys:
      pet_name, description, duration (int minutes), priority, date (ISO str), start_time (HH:MM str)
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=key)

    today = date.today()
    tomorrow = today + timedelta(days=1)

    pet_info = [{"name": p.get_name(), "type": p.get_type()} for p in pets]

    prompt = f"""You are Co-Tasker, a pet care planning assistant.

Create pet care tasks for these pets:
{json.dumps(pet_info)}

Dates available: today={today.isoformat()}, tomorrow={tomorrow.isoformat()}

For EACH pet make exactly 3 tasks:
- Task 1: General (e.g. "Feed <Name>")
- Task 2: Species-specific (e.g. dog="Walk <Name>", cat="Scoop <Name>'s Litter Box", fish="Clean <Name>'s Tank")
- Task 3: Another species-specific (e.g. dog="Bathe <Name>", cat="Brush <Name>", fish="Check <Name>'s Filter")

Return ONLY a JSON array with {len(pets) * 3} objects total. Each object must have:
- "pet_name": string (exact name from input)
- "description": string (the task name)
- "duration": integer (minutes; feeding=10, walk=30, vet=60, grooming=20, tank=15)
- "priority": string ("high", "med", or "low")
- "date": string ("{today.isoformat()}" or "{tomorrow.isoformat()}")
- "start_time": string ("HH:MM" between "07:00" and "20:00", vary so tasks don't all conflict)

Example output format:
[{{"pet_name": "Buddy", "description": "Feed Buddy", "duration": 10, "priority": "high", "date": "{today.isoformat()}", "start_time": "08:00"}}]"""

    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt,
    )

    raw = (response.text or "").strip()

    # Small models often wrap JSON in markdown code fences — strip them
    if raw.startswith("```"):
        lines = raw.splitlines()
        # Drop the opening ```json (or ```) and the closing ```
        inner = lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
        raw = "\n".join(inner).strip()

    if not raw:
        raise ValueError(
            "The model returned an empty response. "
            "Double-check that your GEMINI_API_KEY is valid and that "
            f"the model '{GEMINI_MODEL_NAME}' is available on your account."
        )

    return json.loads(raw)
