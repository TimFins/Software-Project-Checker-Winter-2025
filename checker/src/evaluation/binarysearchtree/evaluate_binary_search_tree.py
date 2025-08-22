from binarytrees import BinaryTreeNode
from evaluation.BstViolationType import BSTViolationType
from typing import Tuple, List, Set

from collections import Counter
from typing import Tuple, Set, List, Dict


def get_not_correct_handled_values_based_on_task_type(
    task_type: str,
    existing_tree: BinaryTreeNode | None,
    student_tree: BinaryTreeNode | None,
    values: List[int]
) -> Tuple[Set[int], Set[int]]:
    """
    Identifies which values were missing (not inserted or deleted) and which were correctly handled,
    accounting for duplicates by comparing counts before and after operation.
    """

    if not values:
        return set(), set()

    existing_values = get_all_values(existing_tree)
    student_values = get_all_values(student_tree)

    existing_counter = Counter(existing_values)
    student_counter = Counter(student_values)
    values_counter = Counter(values)

    incorrectly_handled = set()
    correctly_handled = set()

    if task_type == "BINARY_SEARCH_TREE_INSERT":
        for val, count_to_insert in values_counter.items():
            existing_count = existing_counter.get(val, 0)
            student_count = student_counter.get(val, 0)
            expected_minimum = existing_count + count_to_insert

            if student_count >= expected_minimum:
                correctly_handled.add(val)
            else:
                incorrectly_handled.add(val)

        return incorrectly_handled, correctly_handled

    elif task_type == "BINARY_SEARCH_TREE_DELETE":
        for val, count_to_delete in values_counter.items():
            existing_count = existing_counter.get(val, 0)
            student_count = student_counter.get(val, 0)
            expected_maximum = max(existing_count - count_to_delete, 0)

            if student_count <= expected_maximum:
                correctly_handled.add(val)
            else:
                incorrectly_handled.add(val)

        return incorrectly_handled, correctly_handled

    else:
        raise ValueError(f"Unsupported task_type: {task_type}")


def get_bst_rule_violating_nodes(student_tree: BinaryTreeNode | None, values: list[int]) -> Tuple[List[Tuple[BinaryTreeNode, BSTViolationType]]]:
    """
    Checks whether the student's binary search tree violates BST ordering rules.
    """
    if not values or student_tree is None:
        return []

    violations: List[Tuple[BinaryTreeNode, BSTViolationType]] = []

    def check_node(node: BinaryTreeNode | None, min_val: int | None, max_val: int | None):
        if node is None:
            return

        val = node.get_value()

        if max_val is not None and val >= max_val:
            violations.append(
                (node, BSTViolationType.TOO_LARGE_FOR_LEFT_SUBTREE))
            check_node(node.get_left_child(), None, val)
            check_node(node.get_right_child(), val, None)
            return

        if min_val is not None and val < min_val:
            violations.append(
                (node, BSTViolationType.TOO_SMALL_FOR_RIGHT_SUBTREE))
            check_node(node.get_left_child(), None, max_val)
            check_node(node.get_right_child(), val, None)
            return

        check_node(node.get_left_child(), min_val, val)
        check_node(node.get_right_child(), val, max_val)

    check_node(student_tree, None, None)

    return violations


def get_additional_values_not_meant_to_be_added(
    task_type: str,
    student_tree: BinaryTreeNode | None,
    solution_tree: BinaryTreeNode | None,
    values: List[int] = []
) -> Dict[int, int]:
    """
    Identifies values that are present more times in the student tree than in the solution tree.
    Returns a dictionary mapping each extra value to the number of excess occurrences.

    For deletion tasks, values that were supposed to be deleted are ignored.
    """
    student_counter = Counter(get_all_values(student_tree))
    solution_counter = Counter(get_all_values(solution_tree))
    values_to_ignore = Counter(
        values) if task_type == "BINARY_SEARCH_TREE_DELETE" else Counter()

    extras = {}

    for val, student_count in student_counter.items():
        expected_count = solution_counter.get(val, 0)

        if student_count > expected_count:
            # In deletion task, ignore if value is in the to-be-deleted list
            if task_type == "BINARY_SEARCH_TREE_DELETE" and val in values_to_ignore:
                continue

            extras[val] = student_count - expected_count

    return extras


def get_missing_values_not_meant_to_be_removed(
    task_type: str,
    student_tree: BinaryTreeNode | None,
    existing_tree: BinaryTreeNode | None,
    values: List[int] = []
) -> Set[int]:
    """
    Identifies values from existing_tree that are missing in student_tree and were not meant to be removed.

    In a deletion task: filters out values that were supposed to be deleted.
    In an insertion task: no values should be removed, so all missing values are unexpected.
    """

    if existing_tree is None:
        return set()

    existing_counter = Counter(get_all_values(existing_tree))
    student_counter = Counter(get_all_values(student_tree))
    values_counter = Counter(values)

    missing_unexpectedly = set()

    for val, existing_count in existing_counter.items():
        student_count = student_counter.get(val, 0)

        if task_type == "BINARY_SEARCH_TREE_DELETE":
            removed_intentionally = values_counter.get(val, 0)
            expected_remaining = max(existing_count - removed_intentionally, 0)
            if student_count < expected_remaining:
                missing_unexpectedly.add(val)

        elif task_type == "BINARY_SEARCH_TREE_INSERT":
            if student_count < existing_count:
                missing_unexpectedly.add(val)

        else:
            raise ValueError(f"Unsupported task_type: {task_type}")

    return missing_unexpectedly


def get_values_inserted_at_a_wrong_position(
    solution_tree: BinaryTreeNode,
    existing_tree: BinaryTreeNode | None,
    student_tree: BinaryTreeNode | None,
    values: List[int]
) -> Tuple[List[int]]:
    """
    Returns a list of values that were inserted by the student but are not at the correct position
    """

    def filter_values(paths: List[Tuple[int, Tuple[str, ...]]], valid_values: List[int]) -> List[Tuple[int, Tuple[str, ...]]]:
        return [p for p in paths if p[0] in valid_values]

    sol_paths = filter_values(collect_paths(solution_tree), values)
    ex_paths = filter_values(collect_paths(existing_tree), values)
    stu_paths = filter_values(collect_paths(student_tree), values)

    sol_counter = Counter(sol_paths)
    ex_counter = Counter(ex_paths)
    stu_counter = Counter(stu_paths)

    expected_insertions = sol_counter - ex_counter
    wrongly_positioned = []

    for val_path, expected_count in expected_insertions.items():
        val = val_path[0]
        correct_path_count = stu_counter.get(val_path, 0)

        if correct_path_count >= expected_count:
            continue

        total_val_count = sum(
            v for (v_, _), v in stu_counter.items() if v_ == val)
        existing_val_count = sum(
            v for (v_, _), v in ex_counter.items() if v_ == val)
        student_inserted_val_count = total_val_count - existing_val_count

        if student_inserted_val_count >= expected_count:
            wrongly_positioned.append(val)

    unique_wrong = sorted(set(wrongly_positioned))

    return unique_wrong


def get_similarity_for_adjusted_values_only(
    solution_tree: BinaryTreeNode,
    existing_tree: BinaryTreeNode | None,
    student_tree: BinaryTreeNode | None
) -> float:
    """
    Returns a similarity score (0.0 to 1.0) for how accurately the student adjusted the tree
    after deletions. Only nodes that were expected to change (by comparing existing_tree and
    solution_tree) are considered.
    """

    def as_path_set(tree: BinaryTreeNode | None) -> Set[Tuple[int, Tuple[str, ...]]]:
        if tree is None:
            return set()
        return set(collect_paths(tree))
    sol_paths = as_path_set(solution_tree)
    ex_paths = as_path_set(existing_tree)

    affected_paths = sol_paths.symmetric_difference(ex_paths)

    if not affected_paths:
        if as_path_set(student_tree) == sol_paths:
            return 1.0
        else:
            return 0.0

    def get_node_by_path(root: BinaryTreeNode | None, path: tuple[str, ...]) -> BinaryTreeNode | None:
        current = root
        for direction in path:
            if current is None:
                return None
            if direction == "left":
                current = current.get_left_child()
            elif direction == "right":
                current = current.get_right_child()
            else:
                return None
        return current

    total = 0
    correct = 0

    for val, path in sol_paths:
        if (val, path) in affected_paths:
            total += 1
            node = get_node_by_path(student_tree, path)
            if node is not None and node.get_value() == val:
                correct += 1

    if total == 0:
        return 1.0

    return correct / total


def collect_paths(node: BinaryTreeNode | None, path: List[str] = None) -> List[Tuple[int, Tuple[str, ...]]]:
    if node is None:
        return []
    if path is None:
        path = []
    val = node.get_value()
    result = [(val, tuple(path))]
    result += collect_paths(node.get_left_child(), path + ['left'])
    result += collect_paths(node.get_right_child(), path + ['right'])
    return result


def get_all_values(tree: BinaryTreeNode | None) -> List[int]:
    if tree is None:
        return []
    return [node.get_value() for node in tree.inorder_traverse()]
