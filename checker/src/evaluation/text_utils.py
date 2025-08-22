from evaluation.BstViolationType import BSTViolationType
from binarytrees import BinaryTreeNode, RedBlackTreeNode


def format_value_list(val_set: set[int], is_german: bool) -> str:
    val_list = sorted(val_set)
    if not val_list:
        return ""
    if len(val_list) == 1:
        return str(val_list[0])
    return ", ".join(map(str, val_list[:-1])) + f" {'und' if is_german else 'and'} {val_list[-1]}"


def format_string_list(string_list: list[str], is_german: bool) -> str:
    if not string_list:
        return ""
    if len(string_list) == 1:
        return str(string_list[0])
    return ", ".join(map(str, string_list[:-1])) + f" {'und' if is_german else 'and'} {string_list[-1]}"


def pluralize(singular: str, plural: str, count: int) -> str:
    return singular if count == 1 else plural


def describe_bst_violation(node: BinaryTreeNode | RedBlackTreeNode, violation: BSTViolationType, is_german: bool) -> str:
    """
    Returns a descriptive string about why a given node violates a BST rule, based on allowed value bounds.

    Arguments:
    - node: the BinaryTreeNode or RedBlackTreeNode that is in violation.
    - violation: the type of violation.
    - left_bound: minimum
    - right_bound: maximum
    """
    val = node.get_value()

    if is_german:
        if violation == BSTViolationType.TOO_SMALL_FOR_RIGHT_SUBTREE:
            return f"Wert {val} ist zu klein für die Position. "
        elif violation == BSTViolationType.TOO_LARGE_FOR_LEFT_SUBTREE:
            return f"Wert {val} ist zu groß für die Position. "
    else:
        if violation == BSTViolationType.TOO_SMALL_FOR_RIGHT_SUBTREE:
            return f"Value {val} is too small for its position. "
        elif violation == BSTViolationType.TOO_LARGE_FOR_LEFT_SUBTREE:
            return f"Value {val} is too large for its position. "
