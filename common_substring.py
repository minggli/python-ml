"""
find largest common substring
"""


def common_substring(left: str, right: str) -> str:
    """find common substring"""

    largest_common_string = ""

    left_len, right_len = len(left), len(right)
    max_len = max(left_len, right_len)

    for pos_a in range(left_len):
        for pos_b in range(right_len):
            cursor = 1
            while 1:
                left_substring = left[pos_a : pos_a + cursor]
                right_substring = right[pos_b : pos_b + cursor]

                if left_substring == right_substring and cursor <= max_len:
                    if len(left_substring) > len(largest_common_string):
                        largest_common_string = left_substring
                    cursor += 1
                else:
                    break

    return largest_common_string


if __name__ == "__main__":
    print(common_substring("ilikeapplejuidce", "idontlikeapplepie"))
