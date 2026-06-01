document.addEventListener("DOMContentLoaded", () => {
  const loader = document.getElementById("pageLoader");
  setTimeout(() => loader?.classList.add("hide"), 250);

  const nav = document.querySelector(".app-navbar");
  window.addEventListener("scroll", () => nav?.classList.toggle("scrolled", window.scrollY > 8));

  const savedTheme = localStorage.getItem("quizcraft-theme");
  if (savedTheme) document.documentElement.dataset.theme = savedTheme;
  document.getElementById("themeToggle")?.addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("quizcraft-theme", next);
  });

  document.querySelectorAll(".ripple").forEach((button) => {
    button.addEventListener("click", (event) => {
      const ink = document.createElement("span");
      const size = Math.max(button.offsetWidth, button.offsetHeight);
      ink.className = "ink";
      ink.style.width = ink.style.height = `${size}px`;
      ink.style.left = `${event.offsetX - size / 2}px`;
      ink.style.top = `${event.offsetY - size / 2}px`;
      button.appendChild(ink);
      setTimeout(() => ink.remove(), 560);
    });
  });

  document.getElementById("sidebarOpen")?.addEventListener("click", () => document.getElementById("sidebar")?.classList.add("open"));
  document.getElementById("sidebarClose")?.addEventListener("click", () => document.getElementById("sidebar")?.classList.remove("open"));

  const search = document.getElementById("courseSearch");
  const filter = document.getElementById("courseFilter");
  const cards = [...document.querySelectorAll(".course-card")];
  const applyCourseFilters = () => {
    const term = (search?.value || "").toLowerCase();
    const category = filter?.value || "all";
    cards.forEach((card) => {
      const matchesText = card.dataset.title.toLowerCase().includes(term);
      const matchesCategory = category === "all" || card.dataset.category === category;
      card.style.display = matchesText && matchesCategory ? "" : "none";
    });
  };
  search?.addEventListener("input", applyCourseFilters);
  filter?.addEventListener("change", applyCourseFilters);
  document.querySelectorAll("[data-view]").forEach((btn) => btn.addEventListener("click", () => {
    document.querySelectorAll("[data-view]").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById("courseGrid")?.classList.toggle("list-view", btn.dataset.view === "list");
  }));

  if (document.getElementById("performanceChart")) {
    new Chart(document.getElementById("performanceChart"), {type:"line",data:{labels:["Apt","Py","Java","Web","DSA","AI"],datasets:[{label:"Score",data:[72,84,79,88,82,91],borderColor:"#2563eb",backgroundColor:"rgba(37,99,235,.12)",fill:true,tension:.4}]},options:{plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,max:100}}}});
  }
  if (document.getElementById("resultChart")) {
    new Chart(document.getElementById("resultChart"), {type:"doughnut",data:{labels:["Score","Remaining"],datasets:[{data:[86,14],backgroundColor:["#10b981","#e5e7eb"],borderWidth:0}]},options:{cutout:"72%",plugins:{legend:{display:false}}}});
  }
});
