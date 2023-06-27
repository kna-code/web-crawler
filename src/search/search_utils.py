from .search_request import SearchRequest 
from .search_result import SearchResult
from .search_result import SearchResultExcerpt
import re
from urllib.parse import urljoin

class SearchUtils():
    @staticmethod
    def search_keywords(search_request: SearchRequest, url: str, contents: str):      
       
        results = []

        contents_lower = contents.lower()
        startIdx = 0

        for keyword in search_request.keywords:
                excerpts = []

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
                    result = SearchResult(search_request.name,
                                keyword,
                                url,
                                excerpts)
                    results.append(result)

        return results


    @staticmethod
    def search_links(search_request: SearchRequest, url: str, contents: str):     

        links = []
        linkRegExPattern = re.compile('href="(\S*)"')        
        for link_url in re.findall(linkRegExPattern, contents):
            link_url = link_url.lower()

            # Handle special caseses
            if link_url.startswith("mailto"):
                break 
            elif link_url.startswith("file"):
                break 
            elif not link_url.startswith("http"):
                link_url = urljoin(url, link_url)
            
            links.append(link_url)
                
        return links
        