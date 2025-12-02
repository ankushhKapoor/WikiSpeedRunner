from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def choose_next_link(self, current_page, target_page, links, *extra):
        pass

    def play(self, start_page, target_page, wiki_client):
        current = start_page
        visited = []

        while current!=target_page:
            visited.append(current)
            links = wiki_client.get_link(current)
            links = [l for l in links if l not in visited]

            if not links:
                return visited, False
            
            current = self.choose_next_link(current, target_page, links, wiki_client)

        visited.append(target_page)
        return visited, True