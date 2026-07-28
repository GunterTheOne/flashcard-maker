const generateBtn = document.getElementById("generate-btn");
const notesInput = document.getElementById("notes-input");
const statusEl = document.getElementById("status");
const cardsContainer = document.getElementById("cards-container");
const cardCountEl = document.getElementById("card-count");

generateBtn.addEventListener("click", async () => {
  const notes = notesInput.value.trim();

  if (!notes) {
    statusEl.textContent = "Paste some notes first.";
    return;
  }

  statusEl.style.color = "#666";
  statusEl.textContent = "Generating flashcards...";
  generateBtn.disabled = true;
  cardsContainer.innerHTML = "";
  cardCountEl.textContent = "";

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ notes }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Something went wrong.");
    }

    renderCards(data.cards);
    statusEl.textContent = "";
    cardCountEl.textContent = `${data.cards.length} flashcards — click a card to flip it`;
  } catch (err) {
    statusEl.style.color = "#b3261e";
    statusEl.textContent = err.message;
  } finally {
    generateBtn.disabled = false;
  }
});

function renderCards(cards) {
  cardsContainer.innerHTML = "";

  cards.forEach((card) => {
    const cardEl = document.createElement("div");
    cardEl.className = "flip-card";
    cardEl.innerHTML = `
      <div class="flip-card-inner">
        <div class="flip-card-front">
          <span class="card-label">Question</span>
          <span>${escapeHtml(card.question)}</span>
        </div>
        <div class="flip-card-back">
          <span class="card-label">Answer</span>
          <span>${escapeHtml(card.answer)}</span>
        </div>
      </div>
    `;
    cardEl.addEventListener("click", () => cardEl.classList.toggle("flipped"));
    cardsContainer.appendChild(cardEl);
  });
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
