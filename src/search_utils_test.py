# To run all tests: 
# > python3 -m unittest search_utils_test.py 
#
# To run a single test:
# python3 -m unittest src/search_utils_test.py SearchUtilsTests.test_search_links

import unittest
from .search_request import SearchRequest 
from .search_result import SearchResult
from .search_utils import SearchUtils
import httplib2

class SearchUtilsTests(unittest.TestCase):
    def test_parse_keyword_found(self):

        searchRequest = SearchRequest("Test", "", "", ["abortion"])

        url = "https://profiles.bu.edu/Elisabeth.Woodhams"
        resp, contents = httplib2.Http().request(url)
        str_contents = contents.decode('utf-8')

        print(f'TYPE {type(str_contents)}')
        result = SearchUtils.search_keywords(searchRequest, url, str_contents)
        self.assertTrue(result)

    def test_parse_keyword_not_found(self):

        searchRequest = SearchRequest("Test", "", "", ["monkey brains"])

        url = "https://profiles.bu.edu/Elisabeth.Woodhams"
        resp, contents = httplib2.Http().request(url)
        str_contents = contents.decode('utf-8')

        result = SearchUtils.search_keywords(searchRequest, url, str_contents)
        self.assertFalse(result)

    def test_search_links(self):

        searchRequest = SearchRequest("Test", ["https://profiles.bu.edu"], "", [])

        url = "https://profiles.bu.edu/Elisabeth.Woodhams"
        resp, contents = httplib2.Http().request(url)
        str_contents = contents.decode('utf-8')

        result = SearchUtils.search_links(searchRequest, url, str_contents)
        self.assertGreater(len(result), 1)

if __name__ == '__main__':
    unittest.main()