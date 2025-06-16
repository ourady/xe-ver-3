from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    quiz_name = data.get('quiz_name')
    user = data.get('user')
    score = data.get('score')

    if not quiz_name or not user or score is None:
        return jsonify({"error": "Invalid data"}), 400

    result = {"quiz_name": quiz_name, "user": user, "score": score}
    results_file = "quiz_results.json"

    if os.path.exists(results_file):
        with open(results_file, 'r') as file:
            results = json.load(file)
    else:
        results = []

    results.append(result)

    with open(results_file, 'w') as file:
        json.dump(results, file, indent=4)

    return jsonify({"message": "Score submitted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=False, port=5000)
