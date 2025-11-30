import wikipediaapi

class WikiClient:

    def __init__(self, language="en", user_agent="WikiSpeedRunner"):
        self.wiki = wikipediaapi.Wikipedia(language=language, user_agent=user_agent)

    def get_page(self, title: str):
        return self.wiki.page(title)

    def exists(self, title: str) -> bool:
        return self.get_page(title).exists()

    def get_links(self, title: str) -> list:
        return list(self.get_page(title).links.keys())

    def get_summary(self, title: str):
        summary = self.get_page(title).summary.strip()
        return summary if summary else title