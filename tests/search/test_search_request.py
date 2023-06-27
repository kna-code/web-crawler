# To run all tests: 
# > python3 -m unittest tests.search.test_search_request
#
# To run a single test:
# python3 -m unittest unittest tests.search.test_search_request.SearchRequestTest.test_load_from_json

import unittest
from src.search.search_request import SearchRequestFile
from src.util import file_util
from util import file_util

class SearchRequestTest(unittest.TestCase):
    def test_load_from_json(self):

        json1 = file_util.get_file_contents("./data/faculty_profiles.json")
        requestFile = SearchRequestFile.from_json(json1)
        self.assertEqual(len(requestFile.search_requests), 2)
'''
to_json is not working

    def test_file_round_trip_serialization(self):

        json1 = file_util.get_file_contents("./data/faculty_profiles.json")
        requestFile = SearchRequestFile.from_json(json1)

        print(f'Type: {type(requestFile)}')
        json2 = requestFile.to_json()

        self.assertEqual(json1, json2)  
'''

if __name__ == '__main__':
    unittest.main()