function checkAnswer(isYes) {
    const feedback = document.getElementById("feedback");
    // Placeholder logic
    feedback.textContent = isYes ? "Correct!" : "Wrong!";
}
function submitAnswer(choice, qnum) {
    fetch("/submit_answer", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            answer: choice,
            question_number: qnum
        })
    })
    .then(response => response.json())
    .then(data => {
        // Show feedback
        const feedbackEl = document.getElementById("feedback");
        if (data.correct) {
            feedbackEl.textContent = "Correct! " + data.feedback;
            feedbackEl.style.color = "green";
        } else {
            feedbackEl.textContent = "Wrong! " + data.feedback;
            feedbackEl.style.color = "red";
        }

        // Hide question and answer buttons
        const questionContainer = document.querySelector(".quiz-question-container");
        questionContainer.style.display = "none";

        // Show next button
        document.getElementById("nextBtn").style.display = "inline-block";
    });
}

function goToNext(qnum) {
    window.location.href = `/quiz/${qnum + 1}`;
}

