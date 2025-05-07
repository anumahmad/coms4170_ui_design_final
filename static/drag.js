const player = document.getElementById("draggable");
const dropzones = document.querySelectorAll(".dropzone");
const message = document.getElementById("message");
const attemptDisplay = document.getElementById("attempt-count");
const navButtons = document.getElementById("navigation-buttons");

let initialTop, initialLeft;
let attemptCount = 0;

window.addEventListener("DOMContentLoaded", () => {
  initialTop = player.style.top;
  initialLeft = player.style.left;

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

      message.textContent = "✅ Onside! You may now click Next to continue.";

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

      // Show Next/Back buttons
    //   if (navButtons) {
    //     navButtons.style.display = "block";
    //   }

      // Optional: remove zone highlight after short delay
      setTimeout(() => {
        zone.style.backgroundColor = "transparent";
      }, 1000);

    } else {
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
