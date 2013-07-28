"""
Tests console app functionality
"""

import unittest
import json
import plus.console_app as app


class TestConsoleApp(unittest.TestCase):

    def test_search_people(self):
        response_data = app.search_people('gabe newell')
        result = json.loads(response_data)
        self.assertTrue(result)
        self.assertTrue(result.has_key('kind'))
        self.assertEqual(result['kind'], 'plus#peopleFeed')


if __name__ == '__main__':
    unittest.main()