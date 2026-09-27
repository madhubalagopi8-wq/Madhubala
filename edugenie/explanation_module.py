import os
import warnings
from dotenv import load_dotenv
from gemini_client import generate_ai_content

warnings.filterwarnings("ignore")
load_dotenv()

# Global variables as described in the PDF specification
explain_tokenizer = None
explain_model = None
_model_initialized = False

def init_lamini():
    """Initializes local LaMini-Flan-T5 model if enabled."""
    global explain_tokenizer, explain_model, _model_initialized
    if _model_initialized:
        return explain_model is not None
    _model_initialized = True

    # If user explicitly enables downloading the 3GB weights
    use_local = os.getenv("USE_LOCAL_LAMINI", "false").lower() == "true"
    if not use_local:
        return False

    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        import torch
        print("Loading local MBZUAI/LaMini-Flan-T5-783M model...")
        explain_tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
        explain_model = AutoModelForSeq2SeqLM.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
        print("LaMini-Flan-T5 loaded successfully.")
        return True
    except Exception as e:
        print(f"Notice: Local model could not be loaded ({e}). EduGenie will use Gemini for explanations.")
        return False

def explain_topic(topic: str) -> str:
    """Explains a topic in simple and clear terms for a school student."""
    # 1. Try local LaMini-Flan-T5 if initialized
    if init_lamini() and explain_tokenizer is not None and explain_model is not None:
        try:
            input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
            inputs = explain_tokenizer(input_text, return_tensors="pt")
            outputs = explain_model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )
            explanation = explain_tokenizer.decode(outputs[0], skip_special_tokens=True)
            return explanation
        except Exception as e:
            print(f"Local inference warning: {e}. Falling back to Gemini.")

    # 2. Cloud inference using Gemini
    try:
        prompt = f"Explain the concept of '{topic}' in a simple and clear way for a school student. Keep it concise, friendly, and easy to understand in one or two short paragraphs."
        return generate_ai_content(prompt)
    except Exception as ex:
        return f"⚠️ Error in Explanation: {ex}"