* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: linear-gradient(135deg, #07131f, #0a1d2e 45%, #122b40);
  color: #edf5ff;
}

.app-shell {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.topbar {
  margin-bottom: 24px;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  opacity: 0.7;
  font-size: 0.8rem;
}

h1, h2, h3 {
  margin-top: 0;
}

.layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.panel {
  background: rgba(9, 17, 29, 0.9);
  border: 1px solid rgba(160, 196, 255, 0.2);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.22);
}

.field-group {
  margin-bottom: 16px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid rgba(155, 188, 255, 0.3);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
  color: #edf5ff;
  font-size: 1rem;
}

input::placeholder {
  color: #b7c7d9;
}

.button-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 12px;
  margin-bottom: 18px;
}

button {
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #4ea3ff, #2a7ae1);
  color: white;
  padding: 12px 18px;
  font-weight: 700;
  cursor: pointer;
}

button.secondary {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(158, 191, 255, 0.2);
}

.result-box,
.feedback-box {
  background: rgba(19, 41, 60, 0.9);
  border: 1px solid rgba(87, 160, 255, 0.25);
  border-radius: 12px;
  padding: 16px;
}

.hidden {
  display: none;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(170px, 1fr));
  gap: 14px;
}

.result-grid div {
  border: 1px solid rgba(159, 191, 255, 0.18);
  border-radius: 8px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.02);
}

.result-grid span {
  display: block;
  font-size: 0.8rem;
  opacity: 0.75;
  margin-bottom: 4px;
}

.exercise-box {
  min-height: 120px;
  padding: 14px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(164, 195, 255, 0.16);
  margin-bottom: 16px;
}

.answer-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px 18px;
}

.feedback-box {
  margin-top: 18px;
  white-space: pre-line;
  line-height: 1.6;
}

@media (max-width: 800px) {
  .layout,
  .answer-form,
  .result-grid {
    grid-template-columns: 1fr;
  }
}
