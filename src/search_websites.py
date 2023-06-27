# Example Usage
# > python3 ./src/search_websites.py ./data/test1.json ./output

from search.search_request import SearchRequest
from search.search_request import SearchRequestFile
from search.web_crawler import WebCrawler
from datetime import datetime
import sys
from util import file_util

def main():

    if( len(sys.argv[0]) < 3):
        print("Expected Usage:\nseach_websites.py [SearchParamaterFile] [OutputDir]")
        return

    search_params_file = sys.argv[1]
    output_dir = sys.argv[2]

    print(f'search_websites')
    print(f' search_params_file: {search_params_file}')
    print(f' output_dir: {output_dir}')

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    timestamped_output_dir = f"{output_dir}/{timestamp}"
    #debug_dir = f"{output_dir}/debug"

    search_file = SearchRequestFile.from_json(file_util.get_file_contents(search_params_file))
    print(f'requests = {search_file.search_requests}, len={len(search_file.search_requests)}')
    for request in search_file.search_requests:
        crawler = WebCrawler(request, timestamped_output_dir)
        crawler.run()

if __name__ == "__main__":
    main()
