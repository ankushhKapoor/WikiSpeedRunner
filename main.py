from core.wiki_client import WikiClient
from core.embeddings import SBERTEncoder

title = "Dog"

wiki = WikiClient()

# print(wiki.get_page(title))
# print(wiki.exists(title))
# print(wiki.get_links(title))
# print(wiki.get_summary(title))

sbert = SBERTEncoder()

print(sbert.encode(title))