# simplesort/mergesort.py

def merge_sort(data: list) -> list:
    """
    Sorts a list in ascending order using the merge sort algorithm.

    :param data: A list of comparable elements.
    :return: A new list containing the sorted elements.
    """
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left_half = data[:mid]
    right_half = data[mid:]

    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    return _merge(left_half, right_half)

def _merge(left: list, right: list) -> list:
    """
    Merges two sorted lists into a single sorted list.
    """
    sorted_list = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            sorted_list.append(left[left_index])
            left_index += 1
        else:
            sorted_list.append(right[right_index])
            right_index += 1

    sorted_list.extend(left[left_index:])
    sorted_list.extend(right[right_index:])
    
    return sorted_list