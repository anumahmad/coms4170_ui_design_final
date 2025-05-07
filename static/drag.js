const player = document.getElementById("draggable");
const dropzones = document.querySelectorAll(".dropzone");
const message = document.getElementById("message");
const attemptDisplay = document.getElementById("attempt-count");

let initialTop, initialLeft;
let attemptCount = 0;

// Wait until DOM is fully ready to store accurate initial position
window.addEventListener("DOMContentLoaded", () => {
  initialTop = player.style.top;
  initialLeft = player.style.left;

  // Display initial attempt count
  if (attemptDisplay) {
    attemptDisplay.textContent = `Attempts: ${attemptCount}`;
  }
});

// Get round number from URL
const currentRound = parseInt(window.location.pathname.split("/").pop());

player.addEventListener("dragstart", (e) => {
  e.dataTransfer.setData("text/plain", player.id);
});

dropzones.forEach(zone => {
  zone.addEventListener("dragover", e => e.preventDefault());

  zone.addEventListener("drop", e => {
    e.preventDefault();

    attemptCount++;

    // Update visible attempt counter
    if (attemptDisplay) {
      attemptDisplay.textContent = `Attempts: ${attemptCount}`;
    }

    const isCorrect = zone.dataset.correct === "true";

    // Visual feedback on dropzone
    zone.style.backgroundColor = isCorrect
      ? "rgba(0, 255, 0, 0.6)"
      : "rgba(255, 0, 0, 0.6)";

    if (isCorrect) {
      // Reset player to original position
      player.style.top = initialTop;
      player.style.left = initialLeft;

      // Show countdown
      let countdown = 3;
      message.textContent = `✅ Onside! Moving to next round in ${countdown}...`;

      // Log attempts to server
      fetch("/log_attempts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          round_num: currentRound,
          attempts: attemptCount
        })
      });

      const interval = setInterval(() => {
        countdown--;
        if (countdown > 0) {
          message.textContent = `✅ Onside! Moving to next round in ${countdown}...`;
        } else {
          clearInterval(interval);
          zone.style.backgroundColor = "transparent";

          if (currentRound < 3) {
            window.location.href = `/game/${currentRound + 1}`;
          } else {
            window.location.href = `/quiz_result`;
          }
        }
      }, 1000);
    } else {
      // Incorrect drop
      message.textContent = "❌ Offside! Try again.";

      setTimeout(() => {
        zone.style.backgroundColor = "transparent";
        player.style.top = initialTop;
        player.style.left = initialLeft;
        message.textContent = "";
      }, 3000);
    }
  });
});
