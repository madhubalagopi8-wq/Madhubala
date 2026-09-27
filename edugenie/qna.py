from gemini_client import generate_ai_content

def answer_question_with_gemini(question: str) -> str:
    """Answers student questions using Google Gemini as specified in Milestone 2."""
    try:
        prompt = f"Answer the following educational question accurately and concisely:\n\n{question}"
        answer = generate_ai_content(prompt)
        return answer
    except Exception as e:
        return f"⚠️ Error in QnA: {e}"

def get_answer(question: str) -> str:
    return answer_question_with_gemini(question)