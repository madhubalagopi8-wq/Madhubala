from gemini_client import generate_ai_content

def summarize_text(text: str) -> str:
    """Summarizes text into concise, easy-to-understand language as specified in Milestone 2."""
    try:
        prompt = f"Summarize the following text in simple language:\n\n{text}"
        summary = generate_ai_content(prompt)
        return summary
    except Exception as e:
        return f"⚠️ Error in Summary: {e}"