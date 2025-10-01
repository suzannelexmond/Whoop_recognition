from flask import Flask, request, jsonify
from operator import itemgetter
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow cross-origin requests

scores = []  # in-memory list (will reset if server restarts)

@app.route("/submit-score", methods=["POST"])
def submit_score():
    data = request.json
    scores.append({
        "name": data.get("name", "Unknown"),
        "score": data.get("score", 0)
    })
    # sort high-to-low
    scores.sort(key=itemgetter("score"), reverse=True)
    return {"status": "ok"}

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    return jsonify(scores)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
