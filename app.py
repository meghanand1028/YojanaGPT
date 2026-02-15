from flask import Flask, render_template, request, jsonify
from chatbot_model import get_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.form["message"]
    reply = get_response(user_msg)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
