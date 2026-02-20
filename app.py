from flask import Flask, render_template, request, jsonify, session
from model import get_response
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    """Handle user login"""
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    
    # Simple validation - accept any non-empty email and password
    if email and password:
        session["user_email"] = email
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    """Handle user logout"""
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"})

@app.route("/ask", methods=["POST"])
def ask():
    """Handle chat messages"""
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    
    if not user_msg:
        return jsonify({"success": False, "reply": "Please provide a message"}), 400
    
    bot_reply = get_response(user_msg)
    return jsonify({"success": True, "reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
