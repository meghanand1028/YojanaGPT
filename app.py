from flask import Flask, render_template, request, jsonify
from chatbot_model import get_bot_response


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.form["message"]
    bot_reply = get_bot_response(user_msg)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
