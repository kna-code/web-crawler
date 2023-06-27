# To run all tests: 
# > python3 -m unittest tests.search.test_search_utils 
#
# To run a single test:
# > python3 -m unittest tests.search.test_search_utils.SearchUtilsTests.test_parse_keyword_found 

import unittest
from src.search.search_request import SearchRequest 
from src.search.search_result import SearchResult
from src.search.search_utils import SearchUtils
import httplib2

class SearchUtilsTests(unittest.TestCase):
    def test_parse_keyword_found(self):

        searchRequest = SearchRequest("Test", "", "", ["abortion"])

        url = "https://profiles.bu.edu/Elisabeth.Woodhams"
        resp, contents = httplib2.Http().request(url)
        str_contents = contents.decode('utf-8')

        print(f'TYPE {type(str_contents)}')
        results = SearchUtils.search_keywords(searchRequest, url, str_contents)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].keyword, "abortion")
        self.assertEqual(results[0].url, url)

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


    def test_search_links_with_relative_url(self):

        searchRequest = SearchRequest("Test", ["sph.emory.edu"], "", [])

        url = "https://sph.emory.edu/faculty/?dept=gh"
        resp, contents = httplib2.Http().request(url)
        str_contents = contents.decode('utf-8')

        result = SearchUtils.search_links(searchRequest, url, str_contents)
        self.assertGreater(len(result), 1)

if __name__ == '__main__':
    unittest.main()