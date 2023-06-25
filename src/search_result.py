from typing import List

class SearchResultExcerpt:
    location: int
    exceprt: str

    def __init__(self, location, excerpt):
        self.location = location
        self.excerpt = excerpt

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