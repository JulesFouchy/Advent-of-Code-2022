from utils import *
from pipe import *


def main(filepath: str):
    output(
        lines(filepath)
        | where(lambda l: l)  # Remove empty lines
        | map(eval)  # Parse lists from string
        | groups_of(2)
        | apply(enumerate)
        | where(lambda x: is_in_order(x[1]))
        | map(lambda x: x[0] + 1)
        | apply(sum)
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
