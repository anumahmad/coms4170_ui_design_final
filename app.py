from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/drag")
def drag():
    return render_template("drag.html")

if __name__ == "__main__":
    app.run(debug=True)
