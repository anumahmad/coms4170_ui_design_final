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

    // Create explanation feedback
    const explanationText = document.createElement('div');
    explanationText.classList.add('feedback-explanation');
    explanationText.textContent = data.feedback;

    // Append both to feedback element
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
    window.location.href = `/quiz/${qnum + 1}`;
}

