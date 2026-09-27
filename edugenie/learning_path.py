import traceback
from gemini_client import generate_ai_content

def get_learning_recommendations(topic: str) -> str:
    """Generates structured learning recommendations for a topic as specified in Milestone 2."""
    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (videos, articles, or books).
Include beginner, intermediate, and advanced levels if needed. Format clearly with headings and bullet points.
"""
    try:
        recommendations = generate_ai_content(prompt)
        return recommendations
    except Exception as e:
        traceback.print_exc()
        return f"Error occurred: {str(e)}"

def create_learning_path(topic: str):
    return get_learning_recommendations(topic)