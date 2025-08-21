"""
merge sort

toy implementation of merge sort algorithm
"""
import random


def merge_sort(arr):
    """sorting an array in-place in ascending order."""
    if len(arr) < 2:
        return

    # create two copies
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    merge_sort(left)
    merge_sort(right)

    # merge divided arrays into one
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1        
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

if __name__ == "__main__":
    array = [random.choice(range(100)) for _ in range(10)]
    print(array)
    merge_sort(array)
    print(array)

