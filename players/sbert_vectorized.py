from players.player import Player
from core.embeddings import SBERTEncoder

class PlayerSBERTVectorized(Player):
    def __init__(self):
        self.encoder = SBERTEncoder()

    def choose_next_link(self, current_page, target_page, links, wiki_client):
        target_emb = self.encoder.encode(wiki_client.get_summary(target_page))
        candidate_texts = [l.replace("_", " ") for l in links]
        idx = self.encoder.rank_list(target_emb, candidate_texts)
        return links[idx]