// API helper function
async function apiCall(endpoint, data) {
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    return { error: error.message };
  }
}

// State
let currentExercise = null;
let hintStep = 1;

// DOM Elements
const ipInput = document.getElementById("ipInput");
const cidrInput = document.getElementById("cidrInput");
const maskInput = document.getElementById("maskInput");
const calculateBtn = document.getElementById("calculateBtn");
const generateExerciseBtn = document.getElementById("generateExerciseBtn");
const resultBox = document.getElementById("resultBox");
const exerciseBox = document.getElementById("exerciseBox");
const checkAnswerBtn = document.getElementById("checkAnswerBtn");
const hintBtn = document.getElementById("hintBtn");
const explainBtn = document.getElementById("explainBtn");
const feedbackBox = document.getElementById("feedbackBox");

// Calculate subnet
calculateBtn.addEventListener("click", async () => {
  const ip = ipInput.value.trim();
  const cidr = cidrInput.value;
  const mask = maskInput.value.trim();

  if (!ip) {
    alert("Please enter an IP address");
    return;
  }

  const result = await apiCall("/api/calculate", {
    ip,
    cidr: cidr ? parseInt(cidr) : null,
    mask: mask || null,
  });

  if (result.error) {
    alert("Error: " + result.error);
    return;
  }

  // Display results
  document.getElementById("networkOutput").textContent = result.network_address;
  document.getElementById("broadcastOutput").textContent =
    result.broadcast_address;
  document.getElementById("maskOutput").textContent = result.subnet_mask;
  document.getElementById("firstHostOutput").textContent = result.first_host;
  document.getElementById("lastHostOutput").textContent = result.last_host;
  document.getElementById("usableHostsOutput").textContent =
    result.usable_hosts;

  resultBox.classList.remove("hidden");
});

// Generate exercise
generateExerciseBtn.addEventListener("click", async () => {
  const result = await apiCall("/api/generate-exercise", {
    exercise_type: "basic",
  });

  currentExercise = result;
  hintStep = 1;

  // Display exercise
  exerciseBox.innerHTML = `
    <h3>Exercise</h3>
    <p><strong>${result.prompt}</strong></p>
  `;

  // Clear answer fields
  document.getElementById("networkAnswer").value = "";
  document.getElementById("broadcastAnswer").value = "";
  document.getElementById("maskAnswer").value = "";
  document.getElementById("firstHostAnswer").value = "";
  document.getElementById("lastHostAnswer").value = "";
  document.getElementById("usableHostsAnswer").value = "";

  feedbackBox.classList.add("hidden");
});

// Check answer
checkAnswerBtn.addEventListener("click", async () => {
  if (!currentExercise) {
    alert("Generate an exercise first");
    return;
  }

  const answer = {
    network_address: document.getElementById("networkAnswer").value,
    broadcast_address: document.getElementById("broadcastAnswer").value,
    subnet_mask: document.getElementById("maskAnswer").value,
    first_host: document.getElementById("firstHostAnswer").value,
    last_host: document.getElementById("lastHostAnswer").value,
    usable_hosts: document.getElementById("usableHostsAnswer").value,
  };

  const result = await apiCall("/api/check-answer", {
    exercise: currentExercise,
    answer,
  });

  // Display feedback
  const feedbackText = `
Score: ${result.score}/100
${result.passed ? "✅ PASSED" : "❌ NEEDS WORK"}

Feedback:
${result.feedback}
  `.trim();

  feedbackBox.textContent = feedbackText;
  feedbackBox.classList.remove("hidden");
  hintStep = 1;
});

// Get hint
hintBtn.addEventListener("click", async () => {
  if (!currentExercise) {
    alert("Generate an exercise first");
    return;
  }

  const result = await apiCall("/api/hint", {
    exercise: currentExercise,
    step: hintStep,
  });

  feedbackBox.textContent = `Hint (Step ${hintStep}):\n\n${result.hint}`;
  feedbackBox.classList.remove("hidden");

  hintStep += 1;
});

// Explain concept
explainBtn.addEventListener("click", async () => {
  const result = await apiCall("/api/explain", {
    concept: "IPv4 subnetting",
  });

  feedbackBox.textContent = result.explanation;
  feedbackBox.classList.remove("hidden");
});
