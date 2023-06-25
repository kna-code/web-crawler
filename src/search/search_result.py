from typing import List

class SearchResultExcerpt:
    location: int
    text: str

    def __init__(self, location, text):
        self.location = location
        self.text = text

class SearchResult:
    name: str
    keyword: str
    url: str
    excerpts: List[SearchResultExcerpt]

    def __init__(self, name, keyword, url, excerpts):
        self.name = name
        self.keyword = url
        self.url = url
        self.excerpts = excerpts