
from typing import List

class SearchRequest:
    name: str
    domains: List[str]
    start_url: str
    keywords: List[str]
    excerpt_length = 100
    
    debug_output_enabled = False
    debug_output_dir: str

    def __init__(self, name, domains, start_url, keywords):
        self.name = name
        self.domains = domains
        self.start_url = start_url
        self.keywords = keywords


    def enable_debug_output(self, dir):
        self.debug_output_enabled = True
        self.debug_output_dir = dir
        return self
