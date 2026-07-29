import os
import json
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://bazaarlink.ai/api/v1",
    api_key=os.environ.get("BAZAARLINK_API_KEY"),
)

# auto:free routes to whichever free model is currently available on
# BazaarLink, so you're not tracking specific model names/costs.
MODEL = "auto:free"

SYSTEM_PROMPT = """You are a flashcard generator. You will be given a student's raw class notes.
Turn them into clear, concise question-and-answer flashcard pairs that test understanding of the
key concepts (not just fill-in-the-blank recall of exact sentences).

Rules:
- Return ONLY valid JSON. No preamble, no markdown code fences, no explanation.
- The JSON must be a list of objects, each with exactly two keys: "question" and "answer".
- Keep questions specific and answers short (1-3 sentences).
- Generate as many cards as the notes reasonably support (skip generating cards for filler content).
- Do not invent facts that are not in the notes.

Example output format:
[
  {"question": "What is Newton's second law?", "answer": "Force equals mass times acceleration (F = ma)."},
  {"question": "What is the unit of force in SI?", "answer": "The newton (N)."}
]
"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    notes = (data or {}).get("notes", "").strip()

    if not notes:
        return jsonify({"error": "No notes provided."}), 400

    try:
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=2000,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": notes},
            ],
        )

        raw_text = response.choices[0].message.content.strip()

        # Safety net: strip accidental code fences if the model adds them anyway
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.lower().startswith("json"):
                raw_text = raw_text[4:].strip()

        cards = json.loads(raw_text)

        # Basic validation so a malformed response doesn't break the frontend
        cleaned = []
        for card in cards:
            if isinstance(card, dict) and "question" in card and "answer" in card:
                cleaned.append({"question": str(card["question"]), "answer": str(card["answer"])})

        if not cleaned:
            return jsonify({"error": "Model returned no valid flashcards. Try again."}), 502

        return jsonify({"cards": cleaned})

    except json.JSONDecodeError:
        return jsonify({"error": "Model did not return valid JSON. Try again."}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
