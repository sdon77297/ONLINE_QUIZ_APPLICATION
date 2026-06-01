document.addEventListener("DOMContentLoaded", () => {
  if (window.AOS) AOS.init({duration: 700, once: true, offset: 80});
  document.querySelectorAll(".counter").forEach((counter) => {
    const target = Number(counter.dataset.target || 0);
    let value = 0;
    const step = Math.max(1, Math.ceil(target / 70));
    const tick = () => {
      value = Math.min(target, value + step);
      counter.textContent = value.toLocaleString();
      if (value < target) requestAnimationFrame(tick);
    };
    tick();
  });
  const typed = document.getElementById("typedText");
  if (typed) {
    const words = ["adaptive quizzes", "real analytics", "exam confidence"];
    let i = 0;
    setInterval(() => { i = (i + 1) % words.length; typed.textContent = words[i]; }, 1900);
  }
});
