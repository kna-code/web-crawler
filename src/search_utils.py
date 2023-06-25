from .search_request import SearchRequest 
from .search_result import SearchResult
from .search_result import SearchResultExcerpt
import re

class SearchUtils():
    @staticmethod
    def search_keywords(search_request: SearchRequest, url: str, contents: str):      
        excerpts = []

        contents_lower = contents.lower()
        startIdx = 0

        for keyword in search_request.keywords:
                #print(f'looking for keyword {keyword} in {contents_lower}')
                match = re.search(keyword, contents_lower)
                while match:

                    # Exctract the exceprt text
                    excerpt_len = int(search_request.excerpt_length/2)
                    excerptStart = max(0, startIdx + match.start() - excerpt_len)
                    excerptEnd = min(len(contents)-1, startIdx + match.end() + excerpt_len)
                    exceprtText = contents[excerptStart:excerptEnd]

                    excerpts.append(SearchResultExcerpt(match.start(), exceprtText))

                    # Search for more matches..
                    startIdx = startIdx + match.start() + 1
                    match = re.search(keyword, contents_lower[startIdx:])
        
        if len(excerpts) > 0:
            return SearchResult(search_request.name,
                            keyword,
                            url,
                            excerpts)


    @staticmethod
    def search_links(search_request: SearchRequest, url: str, contents: str):        
        links = []
        linkRegExPattern = re.compile('<a href="(\S*)">')        
        for url in re.findall(linkRegExPattern, contents):
            for domain in search_request.domains:                
                match = re.search(domain, url)
                if match:
                    links.append(url)
                

        return links
        