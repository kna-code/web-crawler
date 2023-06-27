
from typing import List
import json
from collections import namedtuple
import json
from types import SimpleNamespace as Namespace

class SearchRequest:
    name: str
    domains: List[str]
    start_url: str
    keywords: List[str]
    excerpt_length = 100
    
    debug_output_enabled = False

    def __init__(self, name: str, domains: List[str], start_url: str, keywords: List[str]):
        self.name = name
        self.domains = domains
        self.start_url = start_url
        self.keywords = keywords


    def enable_debug_output(self, dir):
        self.debug_output_enabled = True
        self.debug_output_dir = dir
        return self


class SearchRequestFile:
    search_requests : List[SearchRequest]

    def __init__(self, search_requests: List[SearchRequest]):
        self.search_requests = search_requests

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(jsonData):           
           requests = []
           obj = json.loads(jsonData)
           for requestObj in obj["search_requests"]:
                request = SearchRequest(requestObj['name'], requestObj['domains'], requestObj['start_url'], requestObj['keywords'])
                requests.append(request)
                
           return SearchRequestFile(requests)
    
