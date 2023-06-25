
from typing import List

class SearchRequest:
    name: str
    domains: List[str]
    start_url: str
    keywords: List[str]
    excerpt_length = 20

    def __init__(self, name, domains, start_url, keywords):
        self.name = name
        self.domains = domains
        self.start_url = start_url
        self.keywords = keywords


