from binarytrees import RedBlackTreeNode, RedBlackTreeColor
from evaluation.BstViolationType import BSTViolationType
from typing import Tuple, List, Set

from collections import Counter
from typing import Tuple, Set, List, Dict


def get_not_correct_handled_values_based_on_task_type(
    task_type: str,
    existing_tree: RedBlackTreeNode | None,
    student_tree: RedBlackTreeNode | None,
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

    elif task_type == "RED_BLACK_TREE_INSERT":
        for val, count_to_insert in values_counter.items():
            existing_count = existing_counter.get(val, 0)
            student_count = student_counter.get(val, 0)
            expected_minimum = existing_count + count_to_insert

            if student_count >= expected_minimum:
                correctly_handled.add(val)
            else:
                incorrectly_handled.add(val)

        return incorrectly_handled, correctly_handled

    elif task_type == "RED_BLACK_TREE_REPAIR":
        for node, existing_count in existing_counter.items():
            student_count = student_counter.get(node, 0)

            if student_count == existing_count:
                correctly_handled.add(node)
            else:
                incorrectly_handled.add(node)

    else:
        raise ValueError(f"Unsupported task_type: {task_type}")


def get_bst_rule_violating_nodes(student_tree: RedBlackTreeNode | None, values: list[int]) -> Tuple[List[Tuple[RedBlackTreeNode, BSTViolationType]]]:
    """
    Checks whether the student's binary search tree violates BST ordering rules.
    """
    if not values or student_tree is None:
        return []

    violations: List[Tuple[RedBlackTreeNode, BSTViolationType]] = []

    def check_node(node: RedBlackTreeNode | None, min_val: int | None, max_val: int | None):
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
    student_tree: RedBlackTreeNode | None,
    solution_tree: RedBlackTreeNode | None,
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
    student_tree: RedBlackTreeNode | None,
    existing_tree: RedBlackTreeNode | None,
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

        elif task_type == "RED_BLACK_TREE_INSERT":
            if student_count < existing_count:
                missing_unexpectedly.add(val)

        elif task_type == "RED_BLACK_TREE_REPAIR":
            expected_remaining = existing_count
            if student_count < expected_remaining:
                missing_unexpectedly.add(val)

        else:
            raise ValueError(f"Unsupported task_type: {task_type}")

    return missing_unexpectedly


def get_nodes_with_wrong_colors_without_root(
    solution_tree: RedBlackTreeNode | None,
    student_tree: RedBlackTreeNode | None,
) -> Tuple[List[int]]:
    """Returns a list of nodes that are miscolored. Exclude root, since that is graded separately, since that violates a red-black property.
    """
    if solution_tree is None:
        return []

    solution_nodes = solution_tree.preorder_traverse()
    student_nodes = student_tree.preorder_traverse()
    miscolored_nodes = []

    for student_node in student_nodes[1:]:
        miscolorings_for_node = ([solution_node for solution_node in solution_nodes if solution_node.get_value(
        ) == student_node.get_value() and solution_node.get_color() != student_node.get_color()])
        amount_miscolorings_for_node = len(miscolorings_for_node)
        if amount_miscolorings_for_node > 0:
            miscolored_nodes.append(student_node.get_value())
    return sorted(set(miscolored_nodes))


def get_wrongly_colored_roots(student_tree: RedBlackTreeNode | None) -> Tuple[List[int]]:
    if student_tree is not None and student_tree.get_color() != RedBlackTreeColor.BLACK:
        return [student_tree.get_value()]
    else:
        return []


def get_red_red_violating_node_pairs(student_tree: RedBlackTreeNode | None) -> Tuple[List[int]]:
    if student_tree is None:
        return []

    student_nodes = student_tree.preorder_traverse()
    red_red_violation_pairs = []
    for student_node in student_nodes:
        if student_node.get_color() == RedBlackTreeColor.RED:
            if student_node.get_left_child() and student_node.get_left_child().get_color() == RedBlackTreeColor.RED:
                red_red_violation_pairs.append(
                    [student_node.get_value(), student_node.get_left_child().get_value()])
            if student_node.get_right_child() and student_node.get_right_child().get_color() == RedBlackTreeColor.RED:
                red_red_violation_pairs.append(
                    [student_node.get_value(), student_node.get_right_child().get_value()])
    return red_red_violation_pairs


def get_black_height_for_preleaves(student_tree: RedBlackTreeNode | None) -> Tuple[int, List[int]]:
    preleaves_of_given_black_height = {}

    def get_black_height(node: RedBlackTreeNode, black_height=0):
        is_black_node = node.get_color() == RedBlackTreeColor.BLACK
        if is_black_node:
            black_height += 1
        if node.get_left_child():
            get_black_height(node.get_left_child(), black_height)
        else:
            preleaves_of_given_black_height[black_height] = preleaves_of_given_black_height.get(
                black_height, []) + [node.get_value()]
        if node.get_right_child():
            get_black_height(node.get_right_child(), black_height)
        else:
            preleaves_of_given_black_height[black_height] = preleaves_of_given_black_height.get(
                black_height, []) + [node.get_value()]
    if student_tree is None:
        return []
    else:
        get_black_height(student_tree)
        preleaves_of_given_black_height_list = [
            (black_height, preleaves) for black_height, preleaves in preleaves_of_given_black_height.items()]
        preleaves_of_given_black_height_list.sort(key=lambda item: item[0])
        return preleaves_of_given_black_height_list


def get_all_values_at_wrong_position(
    solution_tree: RedBlackTreeNode,
    student_tree: RedBlackTreeNode | None
) -> Tuple[List[int]]:
    """Retrieves a sorted list of distinct values inserted at the incorrect position.
    All nodes in the student_tree are checked. Differing (absolute) paths result in the node being flagged as incorrectly placed.

    This function looks at all the values instead of only a subset, since that is especially relevant for red-black trees,
    since the entire hierarchy can change drastically after performing rebalancing.
    """
    sol_paths = collect_paths(solution_tree)
    stu_paths = collect_paths(student_tree)

    wrongly_positioned = []

    sol_value_to_paths: dict[int, set] = {}
    stu_value_to_paths: dict[int, set] = {}

    for value, path in sol_paths:
        sol_value_to_paths[value] = sol_value_to_paths.get(
            value, set()).union({path})

    for value, path in stu_paths:
        stu_value_to_paths[value] = stu_value_to_paths.get(
            value, set()).union({path})

    for value, paths in stu_value_to_paths.items():
        if sol_value_to_paths.get(value) is not None:
            if sol_value_to_paths.get(value) != paths:
                wrongly_positioned.append(value)

    unique_wrong = sorted(set(wrongly_positioned))
    return unique_wrong


def get_values_inserted_at_a_wrong_position(
    solution_tree: RedBlackTreeNode,
    existing_tree: RedBlackTreeNode | None,
    student_tree: RedBlackTreeNode | None,
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
    solution_tree: RedBlackTreeNode,
    existing_tree: RedBlackTreeNode | None,
    student_tree: RedBlackTreeNode | None
) -> float:
    """
    Returns a similarity score (0.0 to 1.0) for how accurately the student adjusted the tree
    after deletions. Only nodes that were expected to change (by comparing existing_tree and
    solution_tree) are considered.
    """

    def as_path_set(tree: RedBlackTreeNode | None) -> Set[Tuple[int, Tuple[str, ...]]]:
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

    def get_node_by_path(root: RedBlackTreeNode | None, path: tuple[str, ...]) -> RedBlackTreeNode | None:
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


def collect_paths(node: RedBlackTreeNode | None, path: List[str] = None) -> List[Tuple[int, Tuple[str, ...]]]:
    if node is None:
        return []
    if path is None:
        path = []
    val = node.get_value()
    result = [(val, tuple(path))]
    result += collect_paths(node.get_left_child(), path + ['left'])
    result += collect_paths(node.get_right_child(), path + ['right'])
    return result


def get_all_values(tree: RedBlackTreeNode | None) -> List[int]:
    if tree is None:
        return []
    return [node.get_value() for node in tree.inorder_traverse()]


def get_reached_checkpoint(checkpoints: list[RedBlackTreeNode], student_tree: RedBlackTreeNode) -> int:
    """Returns the amount of passed checkpoints by checking whether the submission equals one of the checkpoints.

    It is always assumed that in order to pass checkpoint N, checkpoint N-1 was also passed.
    """
    for offset_from_solution, checkpoint in enumerate(reversed(checkpoints)):
        if checkpoint.is_equal_including_subtrees(student_tree):
            return len(checkpoints) - offset_from_solution
    return 0
