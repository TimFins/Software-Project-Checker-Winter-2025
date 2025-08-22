from binarytrees import BinaryTreeNode
from .evaluate_binary_search_tree import get_not_correct_handled_values_based_on_task_type, get_bst_rule_violating_nodes, get_additional_values_not_meant_to_be_added, get_missing_values_not_meant_to_be_removed, get_values_inserted_at_a_wrong_position
from evaluation.text_utils import *

task_type = "BINARY_SEARCH_TREE_INSERT"


def binary_search_tree_insertion_evaluation(existing_tree: BinaryTreeNode, values: list[int], student_tree: BinaryTreeNode, is_german: bool = True):
    ####################################################################################
    # 1. Solve the task yourself (with existing_tree and or values, depending on task) #
    ####################################################################################
    solution = insert_values_to_tree(existing_tree, values)

    ##################################################
    # 2. Compare your solution with the student tree #
    ##################################################

    missing_values, added_values = get_not_correct_handled_values_based_on_task_type(
        task_type, existing_tree, student_tree, values)
    violations = get_bst_rule_violating_nodes(student_tree, values)
    extra_vals = get_additional_values_not_meant_to_be_added(
        task_type, student_tree, solution)
    missing_values_based_on_existing_tree = get_missing_values_not_meant_to_be_removed(
        task_type, student_tree, existing_tree)
    wrongly_inserted_vals = get_values_inserted_at_a_wrong_position(
        solution,
        existing_tree,
        student_tree,
        values
    )

    ###############################################
    # 3. Calculate solution and generate feedback #
    ###############################################
    # 100 points is the maximum that can be reached
    # max 40 points if all values have been added
    points_for_added_values = len(added_values) / len(values) * 40
    # max 60 points if all values were added at the right position
    # we sum the values which are wrongly placed with the ones which
    # aren't present because they are "wrongly" positioned
    points_for_correct_positioned_added_values = (
        1 - (len(wrongly_inserted_vals) + len(missing_values)) / len(values)) * 60
    # deduct 10 points for each additional value
    points_to_subtract_for_additional_values = sum(extra_vals.values()) * 10
    # deduct 10 points for each missing value from the existing tree
    # which should not have been touched
    points_to_subtract_for_missing_values = len(
        missing_values_based_on_existing_tree) * 10
    # deduct 5 points for each bst rule violated
    points_to_subtract_for_bst_violation = len(violations) * 5

    score = (points_for_added_values
             + points_for_correct_positioned_added_values
             - points_to_subtract_for_additional_values
             - points_to_subtract_for_missing_values
             - points_to_subtract_for_bst_violation)

    feedback = ""

    if is_german:
        if not missing_values:
            feedback += "Alle Werte wurden eingefügt"
        else:
            missing_word = pluralize(
                "Der Wert", "Die Werte", len(missing_values))
            missing_verb = pluralize("wurde", "wurden", len(missing_values))
            feedback += f"{missing_word} {format_value_list(missing_values, is_german)} {missing_verb} nicht eingefügt"

            if added_values:
                feedback += ". "
                added_word = pluralize(
                    "Der Wert", "Die Werte", len(added_values))
                added_verb = pluralize("wurde", "wurden", len(added_values))
                feedback += f"{added_word} {format_value_list(added_values, is_german)} {added_verb} eingefügt"

        violation_msg = ""
        if violations and wrongly_inserted_vals:
            violation_msg = ", aber es gibt Verstöße gegen die Regeln für binäre Suchbäume und einige eingefügte Knoten sind an falscher Position"
        elif violations:
            violation_msg = ", aber es gibt Verstöße gegen die Regeln für binäre Suchbäume"
        elif wrongly_inserted_vals:
            violation_msg = ", aber einige eingefügte Knoten sind an falscher Position"

        feedback += violation_msg + ". "

        if wrongly_inserted_vals:
            wrongly_value_noun = pluralize(
                "Wert", "Werte", len(wrongly_inserted_vals))
            wrongly_position_noun = pluralize(
                "Position", "Positionen", len(wrongly_inserted_vals))
            wrongly_verb = pluralize(
                "wurde", "wurden", len(wrongly_inserted_vals))
            wrongly_pronoun = pluralize(
                "er", "sie", len(wrongly_inserted_vals))
            wrongly_article = pluralize(
                "Der", "Die", len(wrongly_inserted_vals))

            feedback += (
                f"{wrongly_article} {wrongly_value_noun} {format_value_list(wrongly_inserted_vals, is_german)} "
                f"{wrongly_verb} an inkorrekten {wrongly_position_noun} im Baum eingefügt, "
                f"basierend auf der Position, an der {wrongly_pronoun} bei korrekter Einfügereihenfolge erscheinen sollten. "
            )

        violating_values_messages = []
        for node, violation_type in violations:
            msg = describe_bst_violation(node, violation_type, is_german)
            violating_values_messages.append(msg)

        if violating_values_messages:
            feedback += "".join(violating_values_messages)

        extra_value_noun = pluralize("der Wert", "die Werte", len(extra_vals))
        extra_verb = pluralize("war", "waren", len(extra_vals))

        feedback_parts = []

        if extra_vals:
            extra_value_noun = pluralize(
                "der Wert", "die Werte", len(extra_vals))
            extra_verb = pluralize("ist", "sind", len(extra_vals))

            value_list_text = format_value_list(extra_vals.keys(), is_german)

            feedback_parts.append(
                f"{extra_verb} {extra_value_noun} {value_list_text} häufiger im Baum vorhanden als erwartet"
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

        # Zusätzlich sollten/sollte der Wert/die Werte XYZ nicht im Baum auftauchen und der Werte/die Werte fehlt/fehlen

        if feedback_parts:
            feedback += "Zusätzlich " + " und ".join(feedback_parts) + ". "
    else:
        if not missing_values:
            feedback += "All values were inserted into the tree"
        else:
            missing_word = pluralize("value", "values", len(missing_values))
            missing_verb = pluralize("was", "were", len(missing_values))
            feedback += f"The {missing_word} {format_value_list(missing_values, is_german)} {missing_verb} not inserted"

            if added_values:
                feedback += ". "
                added_word = pluralize("value", "values", len(added_values))
                added_verb = pluralize("was", "were", len(added_values))
                feedback += f"The {added_word} {format_value_list(added_values, is_german)} {added_verb} inserted"

        violation_msg = ""
        if violations and wrongly_inserted_vals:
            violation_msg = ", but there are binary search tree rule violations and some inserted nodes are at the wrong position"
        elif violations:
            violation_msg = ", but there are binary search tree rule violations"
        elif wrongly_inserted_vals:
            violation_msg = ", but some inserted nodes are at the wrong position"

        feedback += violation_msg + ". "

        if wrongly_inserted_vals:
            wrongly_value_noun = pluralize(
                "value", "values", len(wrongly_inserted_vals))
            wrongly_position_noun = pluralize(
                "position", "positions", len(wrongly_inserted_vals))
            wrongly_verb = pluralize("was", "were", len(wrongly_inserted_vals))
            wrongly_pronoun = pluralize(
                "it", "they", len(wrongly_inserted_vals))

            feedback += (
                f"The {wrongly_value_noun} {format_value_list(wrongly_inserted_vals, is_german)} "
                f"{wrongly_verb} inserted at the incorrect {wrongly_position_noun} in the tree, "
                f"based on where {wrongly_pronoun} should appear if inserted in the correct order. "
            )

        violating_values_messages = []
        for node, violation_type in violations:
            msg = describe_bst_violation(node, violation_type, is_german)
            violating_values_messages.append(msg)

        if violating_values_messages:
            feedback += "".join(violating_values_messages)

        feedback_parts = []

        if extra_vals:
            extra_value_noun = pluralize("value", "values", len(extra_vals))
            extra_verb = pluralize("appears", "appear", len(extra_vals))

            value_list_text = format_value_list(extra_vals.keys(), is_german)

            feedback_parts.append(
                f"the {extra_value_noun} {value_list_text} {extra_verb} more often than expected"
            )

        if missing_values_based_on_existing_tree:
            missing_value_noun = pluralize("value", "values", len(
                missing_values_based_on_existing_tree))
            missing_verb = pluralize("was", "were", len(
                missing_values_based_on_existing_tree))
            wrongly_pronoun = pluralize("it", "they", len(
                missing_values_based_on_existing_tree))
            feedback_parts.append(
                f"the {missing_value_noun} {format_value_list(missing_values_based_on_existing_tree, is_german)} "
                f"{missing_verb} missing even though {wrongly_pronoun} should be present"
            )

        if feedback_parts:
            feedback += "Additionally, " + " and ".join(feedback_parts) + ". "

    ####################
    # 4. Send response #
    ####################
    return score, feedback, solution

# unmodified recursive bst insertion algorithm


def insert(node: BinaryTreeNode | None, value: int) -> BinaryTreeNode:
    if node is None:
        return BinaryTreeNode(value)
    if value < node.get_value():
        node.set_left_child(insert(node.get_left_child(), value))
    else:
        node._set_right_child(insert(node.get_right_child(), value))
    return node


def insert_values_to_tree(existing_tree: BinaryTreeNode | None, values: list[int]) -> BinaryTreeNode:
    tree_copy = existing_tree.deep_copy() if existing_tree is not None else None

    for value in values:
        tree_copy = insert(tree_copy, value)
    return tree_copy
