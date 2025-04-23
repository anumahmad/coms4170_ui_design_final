from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

lessons = {
    "1": {
        "lesson_id": "1",
        "title": "What is Offside?",
        "text": "A player is in an offside position if, at the moment the ball is played to them, they are closer to the opponent’s goal line than both the ball and the second-to-last defender.",
        "image": "pdf_images/base_2.png",
        "next_lesson": "2"
    },
    "2": {
        "lesson_id": "2",
        "title": "Active Involvement",
        "text": "The player must also be actively involved in play (e.g., receiving the ball or interfering with play).",
        "image": "pdf_images/base_3.png",
        "next_lesson": "3"
    },
    "3": {
        "lesson_id": "3",
        "title": "Opponent’s Half",
        "text": "They must also be in the opponent’s half of the field.",
        "image": "pdf_images/base_4.png",
        "next_lesson": None  # Ends with quiz
    } 
}

quiz_data = [
    {
        "image": "pdf_images/question0.png",
        "question": "Offside?",
        "correct": "yes",
        "feedback": "The player in question is closer to the opponent’s goal line than both the ball and the second-last defender at the moment the ball is played to them!"

    },
    {
        "image": "pdf_images/question1.png",
        "question": "Offside?",
        "correct": "yes",
        "feedback": "The player in question is closer to the opponent’s goal line than both the ball and the second-last defender at the moment the ball is played to them!"

    },
    {
        "image": "pdf_images/question2.png",
        "question": "Offside?",
        "correct": "no",
        "feedback": "The player in question is in their own half! They are onside."
    },
    {
        "image": "pdf_images/page_24_img_1.jpeg",
        "question": "Offside?",
        "correct": "yes",
        "feedback": "The player in question is closer to the opponent’s goal line than both the ball and the second-last defender at the moment the ball is played to them!"
    },
    {
        "image": "pdf_images/page_27_img_1.jpeg",
        "question": "Offside?",
        "correct": "no",
        "feedback": "The player in question is NOT closer to the opponent’s goal line than both the ball and the second-last defender at the moment the ball is played to them! They are onside."
    },
]

user_answers = [] 
        
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/learn")
def learn_intro():
    return redirect(url_for('learn_lesson', lesson_id="1"))

@app.route("/learn/<lesson_id>")
def learn_lesson(lesson_id):
    lesson = lessons.get(lesson_id)
    if not lesson:
        return redirect(url_for("learn_intro"))
    return render_template("lesson.html", lesson=lesson)


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
    feedback = quiz_data[qnum]["feedback"]
    is_correct = (answer == correct)

    if len(user_answers) <= qnum:
        user_answers.append(answer)
    else:
        user_answers[qnum] = answer

    return jsonify({
        "correct": is_correct,
        "feedback": feedback
    })

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
