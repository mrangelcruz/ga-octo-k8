import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    bg_color = os.getenv("BG_COLOR", "#ffffff")  # default to white if not set
    return render_template("index.html", bg_color=bg_color)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
