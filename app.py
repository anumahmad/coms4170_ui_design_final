from flask import Flask, render_template, request, jsonify, redirect, url_for

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

user_answers = []
        
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/quiz/<int:num>")
def quiz(num):
    if num >= len(quiz_data):
        return redirect(url_for('quiz_result'))
    return render_template("quiz.html", question=quiz_data[num], qnum=num)

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.get_json()
    answer = data["answer"]
    qnum = data["question_number"]
    
    correct = quiz_data[qnum]["correct"]
    is_correct = (answer == correct)

    if len(user_answers) <= qnum:
        user_answers.append(answer)
    else:
        user_answers[qnum] = answer

    return jsonify({"correct": is_correct})

@app.route("/drag")
def drag():
    return render_template("drag.html")

@app.route("/quiz_result")
def quiz_result():
    score = 0
    for i, answer in enumerate(user_answers):
        if answer == quiz_data[i]["correct"]:
            score += 1
    return render_template("quiz_result.html", score=score, total=len(quiz_data))

if __name__ == "__main__":
    app.run(debug=True)
