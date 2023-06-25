# To run: 
# > python3 -m unittest search_utils_test.py 

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

        print(f'TYPE {type(str_contents)}')
        result = SearchUtils.search_keywords(searchRequest, url, str_contents)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()