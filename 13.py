from utils import *
from pipe import *
import functools


def comparison(x, y):
    cmp = is_in_order([x, y])
    if cmp is None:
        return 0
    return -1 if cmp else 1


def main(filepath: str):
    packets = list(
        lines(filepath)
        | where(lambda l: l)  # Remove empty lines
        | map(eval)  # Parse lists from string
    )
    packets.append([[2]])
    packets.append([[6]])
    sorted_packets = sorted(packets, key=functools.cmp_to_key(comparison))
    print(
        (sorted_packets.index([[2]]) + 1) *
        (sorted_packets.index([[6]]) + 1)
    )


# Returns None to indicate when the two lists are equal.
# Otherwise returns a bool indicating if the two lists are in order.
def is_in_order(pair_of_lists) -> bool | None:
    left = pair_of_lists[0]
    right = pair_of_lists[1]
    for i in range(max(len(left), len(right))):

        if i >= len(left):
            return True
        if i >= len(right):
            return False

        l = left[i]
        r = right[i]

        if not is_iterable(l) and not is_iterable(r):
            if l == r:
                continue
            return l < r

        l = l if is_iterable(l) else [l]
        r = r if is_iterable(r) else [r]
        comp = is_in_order([l, r])
        if comp is not None:
            return comp

    return None


main(f"{day_number(__file__)}.input")
