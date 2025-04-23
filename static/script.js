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
        if (data.next_question !== null) {
            window.location.href = "/quiz/" + data.next_question;
        } else {
            window.location.href = "/quiz_result";
        }
    });
}
