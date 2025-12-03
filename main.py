import json
import time
from pathlib import Path
from datetime import datetime

from core.wiki_client import WikiClient
from players.sbert_vectorized import PlayerSBERTVectorized
from players.llm import PlayerLLM

START_PAGE = "Dog"
TARGET_PAGE = "Linux"
TARGET_DESC = "Linux is a family of open-source, Unix-like operating systems that manage computer hardware and software."
HISTORY_FILE = "history.json"

# Choose: "vector" or "llm"
PLAYER_TYPE = "vector"

# UI ON(True)/OFF(False)
USE_BROWSER = False

if USE_BROWSER:
    from visualisation.browser_runner import BrowserRunner
else:
    BrowserRunner = None

def get_player(player_type: str):
    pt = player_type.lower()

    if pt == "vector":
        print("SpeedRun Using PlayerSBERTVectorized")
        return PlayerSBERTVectorized()

    if pt == "llm":
        print("SpeedRun Using PlayerLLM (Gemini)")
        return PlayerLLM()

    raise ValueError(f"Unknown PLAYER_TYPE: {player_type}")

def append_run_to_history(data: dict):
    path = Path(HISTORY_FILE)
    try:
        runs = json.loads(path.read_text()) if path.exists() else []
        if not isinstance(runs, list):
            runs = []
    except Exception: # File ends like [{...}  (invalid JSON)
        runs = []

    runs.append(data)
    path.write_text(json.dumps(runs, indent=4))


def run_speedrun():
    print("\nWikipedia Speed Runner\n")
    print(f"Start page : {START_PAGE}")
    print(f"Target page: {TARGET_PAGE}")
    print(f"Player type: {PLAYER_TYPE}")
    print(f"Browser    : {'ON' if USE_BROWSER else 'OFF'}\n")

    wiki = WikiClient()
    player = get_player(PLAYER_TYPE)

    if not wiki.exists(START_PAGE):
        print(f"[ERROR] Start page not found: {START_PAGE}")
        return

    if not wiki.exists(TARGET_PAGE):
        print(f"[ERROR] Target page not found: {TARGET_PAGE}")
        return

    browser = BrowserRunner() if (USE_BROWSER and BrowserRunner) else None

    visited = []
    current = START_PAGE
    success = False
    start_time = time.perf_counter()

    if browser:
        browser.open_page(current)

    while True:
        print(f"Current page: https://en.wikipedia.org/wiki/{current}")

        if current == TARGET_PAGE:
            success = True
            print("\n[SUCCESS] Reached target page!")
            break

        links = wiki.get_links(current)
        links = [l for l in links if l not in visited]

        if not links:
            print("\n[FAIL] No outgoing unvisited links.")
            break

        if isinstance(player, PlayerSBERTVectorized):
            next_page = player.choose_next_link(current, TARGET_PAGE, links, wiki)
        else:
            next_page = player.choose_next_link(current, TARGET_PAGE, links, TARGET_DESC)
        current = next_page.replace(" ", "_")
        visited.append(current)

        if browser:
            browser.click_link_to(current)

    end_time = time.perf_counter()
    total_time = round(end_time - start_time, 4)

    if browser:
        browser.close()

    print(f"\nSuccess     : {success}")
    print(f"Total steps : {len(visited)}")
    print(f"Total time  : {total_time} seconds")

    run_record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "start": START_PAGE,
        "target": TARGET_PAGE,
        "player_type": PLAYER_TYPE,
        "success": success,
        "path": visited,
        "steps": len(visited),
        "time_sec": total_time,
        "use_browser": USE_BROWSER,
    }

    append_run_to_history(run_record)
    print(f"\n[LOG] Appended run to {HISTORY_FILE}")

if __name__ == "__main__":
    run_speedrun()