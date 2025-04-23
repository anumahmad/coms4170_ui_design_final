from flask import Flask, render_template, request, jsonify, redirect, url_for

import logging

# Configure logging to a file
logging.basicConfig(filename='events.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

app = Flask(__name__)

slide_logs = []

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

@app.route("/log_slide", methods=["POST"])
def log_slide():
    data = request.get_json()
    slide_logs.append(data)  # save slide name and timestamp
    print("Slide log:", data)  # optional for debugging
    return jsonify({"status": "ok"})


@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route('/log_event', methods=['POST'])
def log_event():
    data = request.get_json()
    event_type = data.get('event_type')
    slide_number = data.get('slide_number')
    timestamp = data.get('timestamp')
    user_id = session.get('user_id', 'anonymous')  # You can use session or any unique ID

    # Log the event data into a file
    logging.info(f"Event: {event_type}, Slide: {slide_number}, Time: {timestamp}, User: {user_id}")
    
    return '', 204

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
