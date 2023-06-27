from .search_request import SearchRequest 
from .search_result import SearchResult
from .search_result import SearchResultExcerpt
import re

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

        # for relative links we need to pre-pend the source url's path
        root_url = url
        argsIdx = root_url.find("?")
        if argsIdx > 0:
            root_url = root_url[:argsIdx]

        if root_url[1] != "/":
            root_url = root_url + "/"

        links = []
        linkRegExPattern = re.compile('href="(\S*)"')        
        for link_url in re.findall(linkRegExPattern, contents):
            link_url = link_url.lower()

            if link_url.startswith("http"):                
                # Check the domain
                for domain in search_request.domains:                
                    match = re.search(domain, link_url)
                    if match:
                        links.append(link_url)
            else:
                # Handle relative link
                link_url = f'{root_url}{link_url}'
                links.append(link_url)
          
                
        return links
        