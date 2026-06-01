document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".needs-validation").forEach((form) => {
    form.addEventListener("submit", (event) => {
      const password = document.getElementById("password");
      const confirm = document.getElementById("confirmPassword");
      if (password && confirm && password.value !== confirm.value) confirm.setCustomValidity("Passwords do not match");
      else confirm?.setCustomValidity("");
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add("was-validated");
    });
  });

  document.querySelectorAll(".toggle-password").forEach((button) => {
    button.addEventListener("click", () => {
      const input = document.getElementById(button.dataset.target);
      if (!input) return;
      input.type = input.type === "password" ? "text" : "password";
      button.querySelector("i").className = input.type === "password" ? "fa-regular fa-eye" : "fa-regular fa-eye-slash";
    });
  });

  const password = document.getElementById("password");
  password?.addEventListener("input", () => {
    const value = password.value;
    let score = 0;
    if (value.length >= 8) score += 25;
    if (/[A-Z]/.test(value)) score += 25;
    if (/[0-9]/.test(value)) score += 25;
    if (/[^A-Za-z0-9]/.test(value)) score += 25;
    const bar = document.querySelector(".strength span");
    if (bar) {
      bar.style.width = `${score}%`;
      bar.style.background = score > 75 ? "#10b981" : score > 45 ? "#f59e0b" : "#ef4444";
    }
    const text = document.getElementById("strengthText");
    if (text) text.textContent = score > 75 ? "Strong password" : score > 45 ? "Medium password" : "Weak password";
  });
});
