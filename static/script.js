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
        
        // Clear existing feedback
    feedbackEl.innerHTML = '';

    // Create main feedback (Correct! or Wrong!)
    const resultText = document.createElement('div');
    resultText.classList.add('feedback-result');
    resultText.textContent = data.correct ? "Correct!" : "Wrong!";

    // Add correct or wrong class
    if (data.correct) {
        resultText.classList.add("correct");
    } else {
        resultText.classList.add("wrong");
    }

    // Create explanation text
    const explanationText = document.createElement("div");
    explanationText.textContent = data.feedback;
    explanationText.classList.add("feedback-explanation");

    // Append
    feedbackEl.appendChild(resultText);
    feedbackEl.appendChild(explanationText);

        
        // Hide question and answer buttons
        const questionContainer = document.querySelector(".quiz-question-container");
        questionContainer.style.display = "none";

        // Show next button
        document.getElementById("nextBtn").style.display = "inline-block";
    });
}

function goToNext(qnum) {
    window.location.href = `/quiz/${qnum}`;
}

