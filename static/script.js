// Add smooth scroll to form
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".survey-form");

  form.addEventListener("submit", (e) => {
    let valid = true;

    // Check if all required fields are filled
    form.querySelectorAll("select, input[type='number']").forEach((input) => {
      if (!input.value) {
        input.style.borderColor = "red";
        valid = false;
      } else {
        input.style.borderColor = "#ccc";
      }
    });

    if (!valid) {
      e.preventDefault();
      alert("⚠️ Please answer all questions before submitting!");
      return;
    }

    // Show loading animation
    const button = form.querySelector("button");
    button.innerText = "Predicting...";
    button.disabled = true;
    button.style.opacity = "0.7";
  });
});
