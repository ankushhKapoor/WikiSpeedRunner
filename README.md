# WikiSpeedRunner

This project plays the **Wikipedia Speedrun game** automatically.  
The goal: reach a target Wikipedia page from a starting page using **only in-page links** - no search, no URL edits, no going back, no cheating.

<br/>

<div align="center">
<img src="https://github.com/ankushhKapoor/WikiSpeedRunner/blob/main/assets/WikiSpeedRunner-UI.gif" align="center" style="width: 90%" />
</div>

<br/>

Two play modes:

- **WikiSpeedRunner** → SBERT Vector mode
- **AI WikiSpeedRunner** → Gemini LLM mode

---

## Game Modes

### Vector Mode - *WikiSpeedRunner* (SBERT)

Uses the **SBERT model** to compute **word embeddings between:**

> every possible next-page title and the target page’s summary

It picks whichever title is semantically closest to the target.

**Pros**
- Very fast (no external API calls)
- Works offline after model download

**Cons**
- Sometimes takes **more steps** (longer path), even though computation is fast

 *Fast execution, longer routes*

---

### LLM Mode - *AI WikiSpeedRunner* (Gemini)

Uses **Google Gemini** to logically determine which link will lead closer to the goal using a **one-line target description**.

**Pros**
- Often picks **shortest or smartest paths**
- Understands concepts contextually

**Cons**
- Slower (each decision triggers an API call)

 *Short path, slower execution*

---

## Browser Mode (Visual Game UI)

You can enable or disable the visual browser from `main.py`:

```python
USE_BROWSER = True   # show the game visually in chromium
# or
USE_BROWSER = False  # run silently (no UI)
````

When enabled, the bot:

* scrolls to the chosen link
* highlights it in **red**
* clicks it like a real player

This transforms the script into a **playable AI game**.

---

## Installation

### 1️. Clone the Repo

```bash
git clone https://github.com/ankushhKapoor/WikiSpeedRunner.git
cd WikiSpeedRunner
```

---

### 2️. Install Dependencies

#### Using `uv` (recommended)

```bash
uv sync
playwright install chromium
```

#### Using `pip` (without uv)

```bash
pip install wikipedia-api sentence-transformers numpy python-dotenv google-genai playwright
playwright install chromium
```

---

### 3️. Environment Variables (LLM mode only)

Create `.env`:

```env
API_KEY=your_gemini_api_key_here
```

- See `/.env.example` in the repository for reference
- Not required for SBERT Vector mode

---

## Running the Game

Edit settings in `main.py`:

```python
START_PAGE = "Dog"
TARGET_PAGE = "Linux"
PLAYER_TYPE = "vector"  # or "llm"
USE_BROWSER = True
```

#### Target Description Requirement

* If using **LLM mode** → set:

```python
TARGET_DESC = "Linux is an open-source operating system..."
```

* If using **Vector/SBERT mode** → leave `TARGET_DESC` empty or ignore it

Then run:

```bash
python main.py
```

* `PLAYER_TYPE = "vector"` → **WikiSpeedRunner**
* `PLAYER_TYPE = "llm"` → **AI WikiSpeedRunner**

---

## History

Each run is saved to `history.json`, including:

* path taken
* steps
* time taken
* player type used

Compare runs to see whether **speed (SBERT)** or **efficiency (LLM)** wins.

---

## Inspiration

This project is inspired by a **Green Code** YouTube video [I Forced AI to Speedrun Wikipedia](https://youtu.be/JvoUHe1OR68?si=Yeo5_a97neHvDOgh) demonstrating an AI solving Wikipedia speedruns.
