from search.search_request import SearchRequest
from search.web_crawler import WebCrawler

def main():

    searchRequest = SearchRequest("Boston University Faculty", 
                                   ["bu.edu"], 
                                   "https://www.bu.edu/sph/about/directory/", 
                                   ["abortion"])

    output_dir = "./output"

    crawler = WebCrawler(searchRequest, output_dir)
    crawler.run()

if __name__ == "__main__":
    main()
