from search.search_request import SearchRequest
from search.web_crawler import WebCrawler
from datetime import datetime

def main():


    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = f"./output/{timestamp}"
    debug_dir = f"{output_dir}/debug"

    #searchRequest = SearchRequest("Boston University Faculty", ["www.bu.edu/sph"], "https://www.bu.edu/sph/about/directory/", ["abortion"])
    searchRequest = SearchRequest("Emory University Faculty", ["sph.emory.edu"], "https://sph.emory.edu/faculty/?dept=gh", ["abortion"]) #.enable_debug_output(debug_dir)

    crawler = WebCrawler(searchRequest, output_dir)
    crawler.run()

if __name__ == "__main__":
    main()
