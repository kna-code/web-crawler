# Example Usage
# > python3 ./src/search_websites.py ./data/test1.json ./output

from search.search_request import SearchRequest
from search.search_request import SearchRequestFile
from search.web_crawler import WebCrawler
from datetime import datetime
import sys
from util import file_util
import argparse

def main():

    parser = argparse.ArgumentParser(prog="search_websites",
                                     description="Searches websites for keywords",
                                     epilog="------------------------------------")

    parser.add_argument('param_file', help="the search parameters JSON file") 
    parser.add_argument('output_dir', help="the output diretory")
    parser.add_argument('-d', '--debug', action='store_true', help="enables debug output") 


    args = parser.parse_args()

    print(f'search_websites')
    print(f' search_params_file: {args.param_file}')
    print(f' output_dir: {args.output_dir}')

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    timestamped_output_dir = f"{args.output_dir}/{timestamp}"
    debug_output_dir = f"{timestamped_output_dir}/debug"

    search_file = SearchRequestFile.from_json(file_util.get_file_contents(args.param_file))
    for request in search_file.search_requests:
        if args.debug:
            request.enable_debug_output(debug_output_dir)

        crawler = WebCrawler(request, timestamped_output_dir)
        crawler.run()

if __name__ == "__main__":
    main()
