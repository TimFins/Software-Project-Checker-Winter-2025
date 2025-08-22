from binarytrees import BinaryTreeNode
from .evaluate_binary_search_tree import get_not_correct_handled_values_based_on_task_type, get_bst_rule_violating_nodes, get_additional_values_not_meant_to_be_added, get_missing_values_not_meant_to_be_removed, get_similarity_for_adjusted_values_only
from evaluation.text_utils import *

task_type = "BINARY_SEARCH_TREE_DELETE"


def binary_search_tree_deletion_evaluation(existing_tree: BinaryTreeNode, values: list[int], student_tree: BinaryTreeNode, is_german: bool = True):
    ####################################################################################
    # 1. Solve the task yourself (with existing_tree and or values, depending on task) #
    ####################################################################################
    solution, inorder_predecessor_solution = delete_values_from_tree(
        existing_tree, values)

    ##################################################
    # 2. Compare your solution with the student tree #
    ##################################################
    not_deleted_values, deleted_values = get_not_correct_handled_values_based_on_task_type(
        task_type, existing_tree, student_tree, values)
    similarity = get_similarity_for_adjusted_values_only(
        solution, existing_tree, student_tree)
    violations = get_bst_rule_violating_nodes(student_tree, values)
    extra_vals = get_additional_values_not_meant_to_be_added(
        task_type, student_tree, solution, values)
    missing_values_based_on_existing_tree = get_missing_values_not_meant_to_be_removed(
        task_type, student_tree, existing_tree, values)

    ###############################################
    # 3. Calculate solution and generate feedback #
    ###############################################
    # 100 points is the maximum that can be reached
    # max 100 points if all values have been deleted
    points_for_deleted_values = len(deleted_values) / len(values) * 100
    # deduct 10 points for each additional value
    points_to_subtract_for_additional_values = len(extra_vals) * 10
    # deduct 10 points for each missing value from the existing tree
    # which should not have been touched
    points_to_subtract_for_missing_values = len(
        missing_values_based_on_existing_tree) * 10
    # deduct 10 points for each bst rule violated
    points_to_subtract_for_bst_violation = len(violations) * 10

    score = (
        points_for_deleted_values * 0.4
        + points_for_deleted_values * 0.6 * similarity
        - points_to_subtract_for_bst_violation
        - points_to_subtract_for_additional_values
        - points_to_subtract_for_missing_values
    )

    feedback = ""

    if is_german:
        if student_tree == inorder_predecessor_solution and inorder_predecessor_solution != solution:
            wrong_solution_word = pluralize(
                "Der Wert", "Die Werte", len(not_deleted_values))
            wrong_solution_verb = pluralize(
                "wurde", "wurden", len(not_deleted_values))
            return max(0, score), f"{wrong_solution_word} {wrong_solution_verb} nicht wie erwartet mit dem kleinsten Knoten des rechten Teilbaums (Inorder-Nachfolger), sondern mit dem größten Knoten des linken Teilbaums (Inorder-Vorgänger) ersetzt.", solution

        if not not_deleted_values:
            feedback += "Alle Werte wurden aus dem Baum entfernt"
        else:
            missing_word = pluralize(
                "Der Wert", "Die Werte", len(not_deleted_values))
            missing_verb = pluralize(
                "wurde", "wurden", len(not_deleted_values))
            feedback += f"{missing_word} {format_value_list(not_deleted_values, is_german)} {missing_verb} nicht entfernt"

            if deleted_values:
                feedback += ". "
                added_word = pluralize(
                    "Der Wert", "Die Werte", len(deleted_values))
                added_verb = pluralize("wurde", "wurden", len(deleted_values))
                feedback += f"{added_word} {format_value_list(deleted_values, is_german)} {added_verb} entfernt"

        violation_msg = ""
        if violations and similarity < 1 and not not_deleted_values:
            violation_msg = ", aber es gibt Verstöße gegen die Regeln für binäre Suchbäume und einige Knoten sind an falscher Position"
        elif violations:
            violation_msg = ", aber es gibt Verstöße gegen die Regeln für binäre Suchbäume"
        elif similarity < 1 and not not_deleted_values:
            violation_msg = ", aber einige Knoten sind an falscher Position"

        feedback += violation_msg + ". "

        violating_values_messages = []
        for node, violation_type in violations:
            msg = describe_bst_violation(node, violation_type, is_german)
            violating_values_messages.append(msg)

        if violating_values_messages:
            feedback += "".join(violating_values_messages)

        extra_value_noun = pluralize("der Wert", "die Werte", len(extra_vals))
        extra_verb = pluralize("sollte", "sollten", len(extra_vals))

        feedback_parts = []

        if extra_vals:
            feedback_parts.append(
                f"{extra_verb} {extra_value_noun} {format_value_list(extra_vals, is_german)} "
                f"nicht im Baum auftauchen"
            )

        if missing_values_based_on_existing_tree:
            missing_value_noun = pluralize("der Wert", "die Werte", len(
                missing_values_based_on_existing_tree))
            missing_verb = pluralize("fehlt", "fehlen", len(
                missing_values_based_on_existing_tree))
            missing_pronoun = pluralize("er", "sie", len(
                missing_values_based_on_existing_tree))
            missing_verb_two = pluralize("sollte", "sollten", len(
                missing_values_based_on_existing_tree))

            if extra_vals:
                feedback_parts.append(
                    f"{missing_value_noun} {format_value_list(missing_values_based_on_existing_tree, is_german)} "
                    f"{missing_verb}, obwohl {missing_pronoun} vorhanden sein {missing_verb_two}"
                )
            else:
                feedback_parts.append(
                    f"{missing_verb} {missing_value_noun} {format_value_list(missing_values_based_on_existing_tree, is_german)}"
                    f", obwohl {missing_pronoun} vorhanden sein {missing_verb_two}"
                )

        if feedback_parts:
            feedback += "Zustätzlich " + " und ".join(feedback_parts) + ". "
    else:
        if student_tree == inorder_predecessor_solution and inorder_predecessor_solution != solution:
            wrong_solution_word = pluralize(
                "value", "values", len(not_deleted_values))
            wrong_solution_verb = pluralize(
                "was", "were", len(not_deleted_values))
            return max(0, score), f"The {wrong_solution_word} {wrong_solution_verb} not replaced with the smallest node of the right subtree (inorder successor) as expected, but instead with the largest node of the left subtree (inorder predecessor).", solution

        if not not_deleted_values:
            feedback += "All values were deleted from the tree"
        else:
            missing_word = pluralize(
                "value", "values", len(not_deleted_values))
            missing_verb = pluralize("was", "were", len(not_deleted_values))
            feedback += f"The {missing_word} {format_value_list(not_deleted_values, is_german)} {missing_verb} not deleted"

            if deleted_values:
                feedback += ". "
                added_word = pluralize("value", "values", len(deleted_values))
                added_verb = pluralize("was", "were", len(deleted_values))
                feedback += f"The {added_word} {format_value_list(deleted_values, is_german)} {added_verb} deleted"

        violation_msg = ""
        if violations and similarity < 1 and not not_deleted_values:
            violation_msg = ", but there are binary search tree rule violations and some nodes are at the wrong positions"
        elif violations:
            violation_msg = ", but there are binary search tree rule violations"
        elif similarity < 1 and not not_deleted_values:
            violation_msg = ", but some nodes are at the wrong position"

        feedback += violation_msg + ". "

        violating_values_messages = []
        for node, violation_type in violations:
            msg = describe_bst_violation(node, violation_type, is_german)
            violating_values_messages.append(msg)

        if violating_values_messages:
            feedback += "".join(violating_values_messages)

        extra_value_noun = pluralize("value", "values", len(extra_vals))
        extra_verb = pluralize("was", "were", len(extra_vals))

        missing_value_noun = pluralize("value", "values", len(
            missing_values_based_on_existing_tree))
        missing_verb = pluralize("is", "are", len(
            missing_values_based_on_existing_tree))

        feedback_parts = []

        if extra_vals:
            feedback_parts.append(
                f"the {extra_value_noun} {format_value_list(extra_vals, is_german)} "
                f"{extra_verb} not supposed to appear in the tree"
            )

        if missing_values_based_on_existing_tree:
            feedback_parts.append(
                f"the {missing_value_noun} {format_value_list(missing_values_based_on_existing_tree, is_german)} "
                f"{missing_verb} missing even though it should be present"
            )

        if feedback_parts:
            feedback += "Additionally, " + " and ".join(feedback_parts) + ". "

    ####################
    # 4. Send response #
    ####################
    return score, feedback, solution


def delete_values_from_tree(root: BinaryTreeNode | None, values: list[int]) -> BinaryTreeNode | None:
    """Deletes all values from a BST iteratively. Returns the modified tree (or None if empty)."""
    tree_copy = root.deep_copy() if root else None
    for value in values:
        if tree_copy is None:
            break

        tree_copy = delete(tree_copy, value)

    tree_copy_inorder_predecessor = root.deep_copy() if root else None
    for value in values:
        if tree_copy_inorder_predecessor is None:
            break

        tree_copy_inorder_predecessor = delete_inorder_predecessor(
            tree_copy_inorder_predecessor, value)

    return tree_copy, tree_copy_inorder_predecessor


def delete(root: BinaryTreeNode | None, data: int) -> BinaryTreeNode | None:
    """Deletes a node from the BST. Returns the new root (or None if tree becomes empty)."""
    node = root
    predecessor = None

    while node and data != node.get_value():
        predecessor = node
        if data < node.get_value():
            node = node.get_left_child()
        else:
            node = node.get_right_child()

    if not node:
        return root

    if node.get_left_child() and node.get_right_child():
        pred_min_elem = node
        min_elem = node.get_right_child()
        while min_elem.get_left_child():
            pred_min_elem = min_elem
            min_elem = min_elem.get_left_child()

        node.set_value(min_elem.get_value())
        if pred_min_elem.get_left_child() == min_elem:
            pred_min_elem.set_left_child(min_elem.get_right_child())
        else:
            pred_min_elem.set_right_child(min_elem.get_right_child())

    else:
        successor = node.get_left_child() or node.get_right_child()

        if not predecessor:
            return successor
        else:
            if node.get_value() < predecessor.get_value():
                predecessor.set_left_child(successor)
            else:
                predecessor.set_right_child(successor)

    return root


def delete_inorder_predecessor(root: BinaryTreeNode | None, data: int) -> BinaryTreeNode | None:
    """Deletes a node from the BST. Returns the new root (or None if tree becomes empty)."""
    node = root
    predecessor = None

    while node and data != node.get_value():
        predecessor = node
        if data < node.get_value():
            node = node.get_left_child()
        else:
            node = node.get_right_child()

    if not node:
        return root

    if node.get_left_child() and node.get_right_child():
        pred_max_elem = node
        max_elem = node.get_left_child()
        while max_elem.get_right_child():
            pred_max_elem = max_elem
            max_elem = max_elem.get_right_child()

        node.set_value(max_elem.get_value())
        if pred_max_elem.get_right_child() == max_elem:
            pred_max_elem.set_right_child(max_elem.get_left_child())
        else:
            pred_max_elem.set_left_child(max_elem.get_left_child())

    else:
        successor = node.get_left_child() or node.get_right_child()

        if not predecessor:
            return successor
        else:
            if node.get_value() < predecessor.get_value():
                predecessor.set_left_child(successor)
            else:
                predecessor.set_right_child(successor)

    return root


def tree_size(node: BinaryTreeNode | None) -> int:
    """Returns the number of nodes in the binary tree (size)."""
    if node is None:
        return 0
    return 1 + tree_size(node.get_left_child()) + tree_size(node.get_right_child())
