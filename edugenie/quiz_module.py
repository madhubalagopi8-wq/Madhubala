import re
import json
from gemini_client import generate_ai_content

def clean_json_block(text: str) -> str:
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip())
    match = re.search(r"(\[.*\])", cleaned, re.DOTALL)
    if match:
        return match.group(1).strip()
    return cleaned.strip()

def generate_quiz(text: str) -> list:
    """Generates 3 multiple choice questions from text or topic as specified in Milestone 2."""
    prompt = f"""You are a quiz generator.

From the following topic or passage, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON**, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage/Topic:
{text}
"""
    try:
        quiz_text = generate_ai_content(prompt)
        cleaned_text = clean_json_block(quiz_text)
        return json.loads(cleaned_text)
    except Exception as e:
        return [{"error": f"Error generating quiz: {e}"}]