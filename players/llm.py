import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

from players.player import Player

class PlayerLLM(Player):
    def __init__(self, llm_model="gemini-2.5-flash", temperature=0.5):
        load_dotenv()

        api_key = os.getenv("API_KEY")
        if not api_key:
            raise RuntimeError("API_KEY not set in .env")

        self.client = genai.Client(api_key=api_key)
        self.llm_model = llm_model
        self.temperature = temperature

    def choose_next_link(self, cur, tar, links, target_desc):
        if not links:
            raise ValueError("No outgoing links provided to PlayerLLM.")

        prompt = f"""
You are a Wikipedia speedrun expert.

A Wikipedia speedrun is a challenge where players race to navigate from
one Wikipedia article to another using ONLY article links.

Your job: pick ONE link from the list below that will bring us closer
to the target Wikipedia page "{tar}" whose description is:

\"\"\"{target_desc}\"\"\"

Current page: "{cur}"

Valid outgoing link TITLES from the current page:
{json.dumps(links, indent=2)}

INSTRUCTIONS:
- Return EXACTLY ONE title from the list above.
- The answer must be character-for-character identical to one of those titles.
- Do NOT add any explanation, punctuation, quotes, or extra text.
- Only output the chosen title.
"""

        response = self.client.models.generate_content(
            model=self.llm_model,
            config=types.GenerateContentConfig(
                temperature=self.temperature
            ),
            contents=prompt,
        )

        output = (response.text or "").strip()

        if output in links:
            return output

        cleaned = output.strip('"').strip("'")
        if cleaned in links:
            return cleaned

        lowered = cleaned.lower()
        for title in links:
            if title.lower() == lowered:
                return title

        return links[0]
