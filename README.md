# Flashcard Maker

Paste notes → AI generates Q&A pairs as JSON → renders as flip cards.

## Setup (in VS Code)

1. Open this folder in VS Code (`File > Open Folder`).
2. Open a terminal in VS Code (`` Ctrl+` ``).
3. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

4. Get a free API key from https://bazaarlink.ai/free (no credit card
   needed), then set it as an environment variable. Note: your notes get
   sent to this third-party service to generate the flashcards — avoid
   pasting anything sensitive.

   ```bash
   # Windows (PowerShell):
   $env:BAZAARLINK_API_KEY="your-key-here"
   # Mac/Linux:
   export BAZAARLINK_API_KEY="your-key-here"
   ```

   (Tip: for a permanent setup, look into using a `.env` file with
   `python-dotenv` instead of typing this every time.)

5. Run the app:

   ```bash
   python app.py
   ```

6. Open your browser to **http://127.0.0.1:5000**

## How it works

- `app.py` — Flask server. The `/generate` route sends your notes to Claude
  with a system prompt that forces strict JSON output, then validates and
  returns it.
- `templates/index.html` — the page structure.
- `static/style.css` — styling, including the 3D flip-card animation.
- `static/script.js` — sends notes to the backend, renders the returned
  cards, and handles the click-to-flip interaction.

## Next feature idea: "Explain this answer"

When you're ready to add it:
1. Add a small "Explain" button inside `.flip-card-back` in `script.js`'s
   `renderCards()`.
2. Add a new Flask route, e.g. `/explain`, that takes the question + answer
   and asks Claude for a deeper explanation.
3. On click, fetch that route and inject the explanation into the card
   (e.g. append a `<div>` under the answer, or open a small modal).

The current structure (one card = one JS object with `question`/`answer`)
makes this easy to extend — you'd just add an `explanation` field once it's
been fetched.
