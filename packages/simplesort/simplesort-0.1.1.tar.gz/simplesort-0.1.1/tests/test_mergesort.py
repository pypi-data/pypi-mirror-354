# tests/test_mergesort.py

import unittest
from simplesort import merge_sort

class TestMergeSort(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_sorted_list(self):
        self.assertEqual(merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted_list(self):
        self.assertEqual(merge_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_unsorted_list(self):
        self.assertEqual(merge_sort([3, 1, 4, 1, 5, 9, 2, 6]), [1, 1, 2, 3, 4, 5, 6, 9])

    def test_list_with_duplicates(self):
        self.assertEqual(merge_sort([5, 8, 2, 5, 2, 8]), [2, 2, 5, 5, 8, 8])

    def test_list_with_negative_numbers(self):
        self.assertEqual(merge_sort([-3, 1, -4, 0, 5, -9, 2, 6]), [-9, -4, -3, 0, 1, 2, 5, 6])

if __name__ == '__main__':
    unittest.main()