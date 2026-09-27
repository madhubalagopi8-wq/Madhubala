import sys
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_tests():
    print("=== Testing Milestone 2 & Milestone 3 Endpoints ===")
    
    # 1. GET /
    print("\n1. Testing GET / (HTML Interface)...")
    res = client.get("/")
    assert res.status_code == 200
    assert "EduGenie" in res.text
    assert "Ask EduGenie a Question" in res.text
    print("   [OK] Home page loaded properly.")

    # 2. GET /qa
    print("\n2. Testing GET /qa?question=Which is the largest ocean? ...")
    res = client.get("/qa", params={"question": "Which is the largest ocean?"})
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    print(f"   [OK] Answer received: {data['answer'][:80]}...")

    # 3. POST /explain
    print("\n3. Testing POST /explain {'topic': 'Photosynthesis'} ...")
    res = client.post("/explain", json={"topic": "Photosynthesis"})
    assert res.status_code == 200
    data = res.json()
    assert "explanation" in data
    print(f"   [OK] Explanation received: {data['explanation'][:80]}...")

    # 4. POST /summarize
    print("\n4. Testing POST /summarize ...")
    passage = "The Industrial Revolution was a period of major industrialization and innovation during the late 1700s and early 1800s. It began in Great Britain and quickly spread throughout the world."
    res = client.post("/summarize", json={"text": passage})
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data
    print(f"   [OK] Summary received: {data['summary'][:80]}...")

    # 5. POST /quiz
    print("\n5. Testing POST /quiz {'text': 'Pythagoras theorem'} ...")
    res = client.post("/quiz", json={"text": "Pythagoras theorem"})
    assert res.status_code == 200
    data = res.json()
    assert "quiz" in data
    assert isinstance(data["quiz"], list)
    print(f"   [OK] Quiz generated {len(data['quiz'])} questions successfully.")
    for i, q in enumerate(data["quiz"]):
        print(f"        Q{i+1}: {q.get('question')}")
        print(f"        Ans: {q.get('answer')}")

    # 6. GET /learn/recommendations
    print("\n6. Testing GET /learn/recommendations?topic=SQL ...")
    res = client.get("/learn/recommendations", params={"topic": "SQL"})
    assert res.status_code == 200
    data = res.json()
    assert "recommendation" in data
    print(f"   [OK] Learning path received ({len(data['recommendation'])} characters).")

    print("\n==========================================")
    print(" ALL 6 EDUGENIE MODULES ARE FULLY WORKING! ")
    print("==========================================")

if __name__ == "__main__":
    run_tests()
