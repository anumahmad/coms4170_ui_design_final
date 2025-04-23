from flask import Flask, render_template

app = Flask(__name__)

quiz_data = [
    {
        "image": "pdf_images/page_15_img_1.jpeg",
        "question": "Offside?",
        "correct": "yes"
    },
    {
        "image": "pdf_images/page_15_img_1.jpeg",
        "question": "Offside?",
        "correct": "yes"
    },
    {
        "image": "pdf_images/page_15_img_1.jpeg",
        "question": "Offside?",
        "correct": "yes"
    },
    {
        "image": "pdf_images/page_15_img_1.jpeg",
        "question": "Offside?",
        "correct": "yes"
    },
    {
        "image": "pdf_images/page_15_img_1.jpeg",
        "question": "Offside?",
        "correct": "yes"
    },
    {
        "image": "pdf_images/page_15_img_1.jpeg",
        "question": "Offside?",
        "correct": "yes"
    },
    {
        "image": "pdf_images/page_15_img_1.jpeg",
        "question": "Offside?",
        "correct": "yes"
    },
    {
        "image": "pdf_images/page_15_img_1.jpeg",
        "question": "Offside?",
        "correct": "yes"
    },
    {
        "image": "pdf_images/page_15_img_1.jpeg",
        "question": "Offside?",
        "correct": "yes"
    },
]
    
        
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/quiz/<int:num>")
def quiz(num):
    # Load quiz data and pass the nth question to quiz.html
    return render_template("quiz.html", question=quiz_data[num], qnum=num)

@app.route("/drag")
def drag():
    return render_template("drag.html")

if __name__ == "__main__":
    app.run(debug=True)
