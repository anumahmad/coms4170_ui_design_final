const player = document.getElementById("draggable");
const dropzones = document.querySelectorAll(".dropzone");
const message = document.getElementById("message");

let initialTop, initialLeft;

// Wait until DOM is fully ready to store accurate initial position
window.addEventListener("DOMContentLoaded", () => {
  initialTop = player.style.top;
  initialLeft = player.style.left;
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

    const isCorrect = zone.dataset.correct === "true";

    // Visual feedback on dropzone
    zone.style.backgroundColor = isCorrect
      ? "rgba(0, 255, 0, 0.6)"
      : "rgba(255, 0, 0, 0.6)";

    if (isCorrect) {
      // Reset player to original position
      player.style.top = initialTop;
      player.style.left = initialLeft;

      // Countdown logic
      let countdown = 3;
      message.textContent = `✅ Onside! Moving to next round in ${countdown}...`;

      const interval = setInterval(() => {
        countdown--;
        if (countdown > 0) {
          message.textContent = `✅ Onside! Moving to next round in ${countdown}...`;
        } else {
          clearInterval(interval);
          zone.style.backgroundColor = "transparent";
          const nextRound = currentRound < 3 ? currentRound + 1 : 1;
          window.location.href = `/game/${nextRound}`;
        }
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
