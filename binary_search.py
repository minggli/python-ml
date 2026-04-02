"""
binary search

toy binary search implementation
"""


def binary_search(arr, target):
    i = 0
    j = len(arr) - 1

    # binary search only operates on sorted array.
    arr = sorted(arr)

    while i < j:
        mid = (i + j) // 2

        if arr[mid] < target:
            i = mid + 1
        elif arr[mid] > target:
            j = mid
        else:
            return mid

    return -1


if __name__ == "__main__":
    arr = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    target = 35
    result = binary_search(arr, target)

    print(result)
