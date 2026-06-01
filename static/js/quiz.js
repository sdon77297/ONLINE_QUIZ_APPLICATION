document.addEventListener("DOMContentLoaded", () => {
  const questionText = document.getElementById("questionText");
  const optionList = document.getElementById("optionList");
  const progress = document.getElementById("quizProgress");
  const number = document.getElementById("questionNumber");
  const palette = document.getElementById("questionPalette");
  const autosave = document.getElementById("autosaveStatus");
  const timer = document.getElementById("quizTimer");
  if (!questionText || !optionList || !progress || !number || !palette) return;

  const questions = [
    { q: "Which keyword is used to define a function in Python?", o: ["func", "def", "lambda", "method"] },
    { q: "Which data structure uses FIFO order?", o: ["Stack", "Queue", "Tree", "Graph"] },
    { q: "What does HTML stand for?", o: ["HyperText Markup Language", "HighText Machine Language", "Hyper Tool Markup Link", "Home Text Markup Language"] },
    { q: "Which Java concept supports multiple forms?", o: ["Encapsulation", "Polymorphism", "Compilation", "Serialization"] },
    { q: "Which metric measures classification correctness?", o: ["Accuracy", "Entropy", "Latency", "Variance"] },
  ];
  const answers = new Array(questions.length).fill(null);
  let index = 0;

  const setAutosave = (text) => {
    if (!autosave) return;
    autosave.innerHTML = `<i class="fa-solid fa-cloud-arrow-up me-1"></i>${text}`;
  };

  const renderQuestion = () => {
    const current = questions[index];
    number.textContent = index + 1;
    questionText.classList.add("animate__animated", "animate__fadeIn");
    questionText.textContent = current.q;
    progress.style.width = `${((index + 1) / questions.length) * 100}%`;
    optionList.innerHTML = current.o.map((option, optionIndex) => {
      const checked = answers[index] === optionIndex ? "checked" : "";
      const selected = answers[index] === optionIndex ? "selected" : "";
      return `<label class="${selected}"><input type="radio" name="answer" value="${optionIndex}" ${checked}><span>${option}</span></label>`;
    }).join("");
    [...palette.querySelectorAll("button")].forEach((button, i) => {
      button.classList.toggle("active", i === index);
      button.classList.toggle("answered", answers[i] !== null);
    });
  };

  optionList.addEventListener("change", (event) => {
    if (!event.target.matches("input[name='answer']")) return;
    answers[index] = Number(event.target.value);
    setAutosave("Saving...");
    setTimeout(() => setAutosave("Auto-saved"), 450);
    renderQuestion();
  });

  document.getElementById("nextQuestion")?.addEventListener("click", () => {
    index = Math.min(questions.length - 1, index + 1);
    renderQuestion();
  });
  document.getElementById("prevQuestion")?.addEventListener("click", () => {
    index = Math.max(0, index - 1);
    renderQuestion();
  });
  palette.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    index = [...palette.querySelectorAll("button")].indexOf(button);
    renderQuestion();
  });

  if (timer) {
    let seconds = Number(timer.dataset.minutes || 15) * 60;
    setInterval(() => {
      seconds = Math.max(0, seconds - 1);
      const mm = String(Math.floor(seconds / 60)).padStart(2, "0");
      const ss = String(seconds % 60).padStart(2, "0");
      timer.querySelector("span").textContent = `${mm}:${ss}`;
    }, 1000);
  }

  renderQuestion();
});
