from flask import Flask, render_template, request, jsonify, redirect, url_for, session

import logging

# print to console for data
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

slide_logs = []

app.secret_key = 'dev-key-123'

# Data for drag and drop section
drag_data = {
    "title": "Drag the Offside Plays",
    "description": "Sort these plays by dragging them to the correct category. Is the highlighted player in an offside position?",
    "images": [
        {
            "id": "drag1",
            "image": "dragVideos/DRAG_A_a-classic-example-640w.mp4",
            "is_offside": True,
            "feedback": "This is offside! The player is ahead of the second-last defender. In fact, this is a classic example!"
        },
        {
            "id": "drag2",
            "image": "dragVideos/DRAG_B_no-2-640w.mp4",
            "is_offside": False,  # Changed to False to match feedback
            "feedback": "This is not offside! Remember timing matters, as long as the player is onside at the moment the ball is passed, it is OK to then run into an offside position."
        },
        {
            "id": "drag3",
            "image": "dragVideos/DRAG_C_no-3-640w.mp4",
            "is_offside": False,
            "feedback": "This is not offside! What if the attacking player is even with the last defender when the pass is made, as is the case here? In that situation, the player is not offside. The player must be past the last defender to be offside, even if it is by a margin so slender that it can only be established after a replay. Or sometimes several."
        },
        {
            "id": "drag4",
            "image": "dragVideos/DRAG_D_an-offside-teammate-640w.mp4",
            "is_offside": True,
            "feedback": "This is offside! The player is ahead of the second-last defender and involved in play obstructing the goalkeeper's vision."
        },
        {
            "id": "drag5",
            "image": "dragVideos/DRAG_E_no-4-b-640w.mp4",
            "is_offside": False,
            "feedback": "This is not offside! In this case, the attacking player uninvolved in the action is far enough away to be considered what is called passively offside. As long as this player stays out of the play, the red team can continue the attack."
        }
    ]
}

# Data for the learn section
learn_data = {
    "title": "What is the Offside Rule?",
    "intro": {
        "main_title": "What is the Offside Rule?",
        "column1_title": "What is the Offside Rule even for?",
        "column1_content": "If you've ever watched a football match, you've probably heard the term \"offside\" thrown around, often followed by some groans, cheers, or VAR jokes (a system that uses video footage to assist on-field referees in making decisions).",
        "column2_title": "Why?",
        "column2_content": "In simple terms, the offside rule exists to prevent players from hanging around the opponent's goal waiting for an easy chance to score. It keeps the game fair and strategic. It can get a bit technical, which is why even VAR (Video Assistant Referee) sometimes takes ages to decide.",
        "bubble1": "VAR works for [ rival team ] confirmed.",
        "bubble2": "By the time VAR makes a decision, I'll be at the World Cup."
    },
    "slides": [
        {
            "id": 0,
            "title": "What is the Offside Rule?",
            "text": "A player is in an <strong>offside position</strong> if, at the moment the ball is played to them:",
            "rules": [],
            "image": "pdf_images/base_learning.png",
            "button_text": "SEE RULE"
        },
        {
            "id": 1,
            "title": "What is the Offside Rule?",
            "text": "A player is in an <strong>offside position</strong> if, at the moment the ball is played to them:",
            "rules": [
                "<strong>1.</strong> They are <strong>closer to the opponent's goal line</strong> than both the ball <em>and</em> the <strong>second-to-last defender</strong>."
            ],
            "image": "pdf_images/base_2.png",
            "button_text": "SEE RULE"
        },
        {
            "id": 2,
            "title": "What is the Offside Rule?",
            "text": "A player is in an <strong>offside position</strong> if, at the moment the ball is played to them:",
            "rules": [
                "<strong>1.</strong> They are <strong>closer to the opponent's goal line</strong> than both the ball <em>and</em> the <strong>second-to-last defender</strong>.",
                "<strong>2.</strong> They are <strong>actively involved in play</strong> (e.g., receiving the ball or interfering with play)."
            ],
            "image": "pdf_images/base_3.png",
            "button_text": "SEE RULE"
        },
        {
            "id": 3,
            "title": "What is the Offside Rule?",
            "text": "A player is in an <strong>offside position</strong> if, at the moment the ball is played to them:",
            "rules": [
                "<strong>1.</strong> They are <strong>closer to the opponent's goal line</strong> than both the ball <em>and</em> the <strong>second-to-last defender</strong>.",
                "<strong>2.</strong> They are <strong>actively involved in play</strong> (e.g., receiving the ball or interfering with play).",
                "<strong>3.</strong> They are in the <strong>opponent's half of the field</strong>."
            ],
            "image": "pdf_images/base_4.png",
            "button_text": "START QUIZ"
        }
    ]
}

quiz_data = [
    {
        "header": "Section 1: Offside - Yes or No",
        "image": "pdf_images/question0.png",
        "question": "Is this an offsides play?",
        "correct": "yes",
        "feedback": "This is an offsides play because the player in question is closer to the opponent’s goal line than both the ball and the second-last defender at the moment the ball is played to them!"

    },
    {
        "header": "Section 1: Offside - Yes or No",
        "image": "pdf_images/question1.png",
        "question": "Is this an offsides play?",
        "correct": "yes",
        "feedback": "This is an offsides play because the player in question is closer to the opponent’s goal line than both the ball and the second-last defender at the moment the ball is played to them!"

    },
    {
        "header": "Section 1: Offside - Yes or No",
        "image": "pdf_images/question2.png",
        "question": "Is this an offsides play?",
        "correct": "no",
        "feedback": "This is an onsides play because the player in question is in their own half! Remember: a play can only be offsides if the offensive team is NOT in their own half at the time of the pass."
    },
    {
        "header": "Section 2: Offside from a Real Match - Yes or No",
        "image": "pdf_images/page_24_img_1.jpeg",
        "question": "Is this an offsides play?",
        "correct": "yes",
        "feedback": "This is an offsides play because the player in question is closer to the opponent’s goal line than both the ball and the second-last defender at the moment the ball is played to them!"
    },
    {
        "header": "Section 2: Offside from a Real Match - Yes or No",
        "image": "pdf_images/page_27_img_1.jpeg",
        "question": "Is this an offsides play?",
        "correct": "yes",
        "feedback": "This is a tricky one! This is an offsides play because the last offensive player is just slightly ahead of the second-to-last defender (player #6). Make sure to keep your eye out for the tricky ones!"
    },
]

user_answers = {} 
        
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
    return render_template("learn.html", learn_data=learn_data)

@app.route('/log_event', methods=['POST'])
def log_event():
    data = request.get_json()
    event_type = data.get('event_type')
    slide_number = data.get('slide_number')
    timestamp = data.get('timestamp')
    user_id = session.get('user_id', 'anonymous')  # You can use session or any unique ID

    # Log the event data to the console
    print(f"Event: {event_type}, Slide: {slide_number}, Time: {timestamp}, User: {user_id}")
    
    return '', 204


@app.route("/quiz/<int:num>")
def quiz(num):
    if num >= len(quiz_data):
        return redirect(url_for('game', round_num=1))
    return render_template("quiz.html", question=quiz_data[num], qnum=num)


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.get_json()
    answer = data["answer"]
    qnum = data["question_number"]
    
    correct = quiz_data[qnum]["correct"]
    feedback = quiz_data[qnum]["feedback"]
    is_correct = (answer == correct)

    user_answers[qnum] = answer  # <- stores answer by index

    return jsonify({
        "correct": is_correct,
        "feedback": feedback
    })

@app.route("/drag")
def drag():
    return render_template("drag.html", drag_data=drag_data)

# @app.route("/quiz_result")
# def quiz_result():
#     score = 0
#     for i, answer in enumerate(user_answers):
#         if answer == quiz_data[i]["correct"]:
#             score += 1
#     return render_template("quiz_result.html", score=score, total=len(quiz_data))

# @app.route("/quiz_result")
# def quiz_result():
#     score = 0
#     for i, answer in enumerate(user_answers):
#         if answer == quiz_data[i]["correct"]:
#             score += 1

#     # Get stored attempts
#     game_attempts = session.get("game_attempts", {})

#     session.clear()  # optional: clear session after using it

#     return render_template(
#         "quiz_result.html",
#         score=score,
#         total=len(quiz_data),
#         game_attempts=game_attempts
#     )

@app.route("/quiz_result")
def quiz_result():
    score = 0
    results = []

    for i in range(len(quiz_data)):
        correct_answer = quiz_data[i]["correct"]
        question_text = quiz_data[i]["question"]
        feedback = quiz_data[i]["feedback"]

        user_answer = user_answers.get(i, "No answer")  # fetch safely

        is_correct = (user_answer == correct_answer)
        if is_correct:
            score += 1

        results.append({
            "number": i + 1,
            "question": question_text,
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "feedback": feedback
        })

    game_attempts = session.get("game_attempts", {})
    session.clear()

    return render_template(
        "quiz_result.html",
        score=score,
        total=len(quiz_data),
        game_attempts=game_attempts,
        results=results
    )


@app.route('/field')
def field():
    return render_template('field.html')

@app.route("/restart_quiz")
def restart_quiz():
    global user_answers
    user_answers.clear()  # clears stored quiz answers
    return redirect(url_for('quiz', num=0))


@app.route('/game/<int:round_num>')
def game(round_num):
    if round_num not in [1, 2, 3]:
        return redirect(url_for('game', round_num=1))
    return render_template('field.html', round_num=round_num)


@app.route("/log_attempts", methods=["POST"])
def log_attempts():
    data = request.get_json()
    round_num = data.get("round_num")
    attempts = data.get("attempts")

    # Initialize dict if not already present
    if "game_attempts" not in session:
        session["game_attempts"] = {}

    # Store attempts for this round (as string keys, since session uses JSON)
    session["game_attempts"][str(round_num)] = attempts
    session.modified = True  # mark session as changed

    return jsonify({"status": "logged"})

if __name__ == "__main__":
    app.run(debug=True)
