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

// Add to your existing JavaScript
document.addEventListener('DOMContentLoaded', function() {
  // Initialize half-circle meter
  const meter = document.querySelector('.half-circle');
  const meterValue = document.querySelector('.meter-center');
  const questions = document.querySelectorAll('select');
  
  function updateMeter() {
    const answered = Array.from(questions).filter(q => q.value).length;
    const total = questions.length;
    const progress = (answered / total) * 100;
    
    meter.style.setProperty('--progress', `${progress}%`);
    meterValue.textContent = `${Math.round(progress)}%`;
    
    // Add glow effect when complete
    if (progress === 100) {
      meter.classList.add('meter-complete');
    }
  }

  questions.forEach(q => {
    q.addEventListener('change', updateMeter);
    // Add floating label animation
    q.addEventListener('focus', (e) => {
      e.target.parentElement.classList.add('focused');
    });
    q.addEventListener('blur', (e) => {
      if (!e.target.value) {
        e.target.parentElement.classList.remove('focused');
      }
    });
  });

  // Initialize
  updateMeter();
});
