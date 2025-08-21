"""
binary search

toy binary search implementation
"""


def binary_search(arr, target):
    """binary search implementation on a sorted array."""
    i = 0
    j = len(arr) - 1

    while i < j:        
        mid = (i + j) // 2
        
        if arr[mid] == target:
            return mid

        if arr[mid] < target:
            i += 1
        else:
            j -= 1

    return -1

if __name__ == "__main__":
    arr = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    target = 34
    result = binary_search(arr, target)

    print(result)
