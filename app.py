import os
from flask import Flask, jsonify, request, render_template
from subnetting_engine import (
    calculate_network,
    generate_exercise,
    check_answer,
    get_fallback_hint,
    explain_concept,
)

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

app = Flask(__name__)


def get_ai_hint(exercise: dict, step: int = 1) -> str:
    """Return AI hint if API key is configured; otherwise return a safe fallback."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return get_fallback_hint(exercise, step)

    try:
        client = OpenAI(api_key=api_key)
        prompt = (
            "You are a cybersecurity instructor teaching IPv4 subnetting. "
            "Give a helpful beginner-friendly hint for this exercise without solving it outright. "
            "Focus on the next logically correct step only.\n\n"
            f"Exercise: {exercise.get('prompt', '')}\n"
            f"Step: {step}"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return get_fallback_hint(exercise, step)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True) or {}
    ip = (data.get("ip") or "").strip()
    cidr = data.get("cidr")
    mask = (data.get("mask") or "").strip()

    if not ip:
        return jsonify({"error": "IP address is required."}), 400

    try:
        if cidr is not None:
            result = calculate_network(ip, cidr=int(cidr))
        elif mask:
            result = calculate_network(ip, mask=mask)
        else:
            return jsonify({"error": "CIDR or subnet mask is required."}), 400
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/api/generate-exercise", methods=["POST"])
def generate_new_exercise():
    data = request.get_json(silent=True) or {}
    exercise_type = data.get("exercise_type", "basic")
    exercise = generate_exercise(exercise_type)
    return jsonify(exercise)


@app.route("/api/check-answer", methods=["POST"])
def check_user_answer():
    data = request.get_json(silent=True) or {}
    exercise = data.get("exercise")
    user_answer = data.get("answer") or {}

    if not exercise:
        return jsonify({"error": "Exercise data is required."}), 400

    result = check_answer(exercise, user_answer)
    return jsonify(result)


@app.route("/api/hint", methods=["POST"])
def hint():
    data = request.get_json(silent=True) or {}
    exercise = data.get("exercise") or generate_exercise("basic")
    step = int(data.get("step", 1))
    return jsonify({"hint": get_ai_hint(exercise, step)})


@app.route("/api/explain", methods=["POST"])
def explain():
    data = request.get_json(silent=True) or {}
    concept = (data.get("concept") or "IPv4 subnetting").strip()
    return jsonify({"explanation": explain_concept(concept)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
