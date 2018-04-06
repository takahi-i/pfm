import unittest

from pf_manager.util.util import create_ordered_2d_array_from_dict
from pf_manager.util.util import convert_dictionary_to_2d_array
from pf_manager.util.util import sort_body_order
from pf_manager.util.util import add_headers

import sys
py_version = sys.version_info[0]

HEADERS = ['name', 'local_port', 'login_user']
JSON_DATA = {
        'b_test': {'local_port': '8889',
                   'login_user': None,
                   'name': 'b_test'},
        'a_test': {'local_port': '8888',
                   'login_user': None,
                   'name': 'a_test'}}


class TestUtil(unittest.TestCase):
    def test_create_oredered_2d_array_from_dict(self):
        expected = [['name', 'local_port', 'login_user'], ['a_test', '8888', None], ['b_test', '8889', None]]
        actual = create_ordered_2d_array_from_dict(JSON_DATA, HEADERS)
        self.assertEqual(expected, actual)

    def test_convert_dictionary_to_2d_array(self):
        expected = [['b_test', '8889', None], ['a_test', '8888', None]]
        actual = convert_dictionary_to_2d_array(JSON_DATA, HEADERS)
        if py_version < 3:
            self.assertItemsEqual(expected, actual)
        else:
            self.assertCountEqual(expected, actual)

    def test_sort_body_order(self):
        body = [['b_test', '8889', None], ['a_test', '8888', None]]
        expected = [['a_test', '8888', None], ['b_test', '8889', None]]
        actual = sort_body_order(body)
        self.assertEqual(expected, actual)

    def test_add_headers(self):
        body = ['a_test', '8888', None]
        expected = [HEADERS, 'a_test', '8888', None]
        actual = add_headers(body, HEADERS)
        self.assertEqual(expected, actual)
