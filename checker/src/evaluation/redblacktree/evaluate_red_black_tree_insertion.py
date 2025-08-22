from binarytrees import RedBlackTreeNode
from .evaluate_red_black_tree import *
from .red_black_tree_algorithms import insert_values_into_red_black_tree
from evaluation.text_utils import *

task_type = "RED_BLACK_TREE_INSERT"


def red_black_tree_insertion_evaluation(existing_tree: RedBlackTreeNode, values: list[int], student_tree: RedBlackTreeNode, is_german: bool = True):
    ####################################################################################
    # 1. Solve the task yourself (with existing_tree and or values, depending on task) #
    ####################################################################################
    solution = insert_values_into_red_black_tree(
        existing_tree.deep_copy() if existing_tree is not None else None, values)

    ##################################################
    # 2. Compare your solution with the student tree #
    ##################################################
    # Edge case: Empty Submission
    if student_tree is None:
        if is_german:
            return 0, "Leere Abgabe.", solution
        else:
            return 0, "Empty Submission.", solution

    missing_values, added_values = get_not_correct_handled_values_based_on_task_type(
        task_type, existing_tree, student_tree, values)
    violations = get_bst_rule_violating_nodes(student_tree, values)
    extra_vals = get_additional_values_not_meant_to_be_added(
        task_type, student_tree, solution)
    missing_values_based_on_existing_tree = get_missing_values_not_meant_to_be_removed(
        task_type, student_tree, existing_tree)
    wrongly_inserted_vals = get_all_values_at_wrong_position(
        solution, student_tree)
    wrongly_colored_vals_without_root = get_nodes_with_wrong_colors_without_root(
        solution, student_tree)
    wrongly_colored_roots = get_wrongly_colored_roots(student_tree)
    red_red_violating_node_pairs = get_red_red_violating_node_pairs(
        student_tree)
    black_height_preleaf_nodes = get_black_height_for_preleaves(student_tree)

    ############################################
    # 3. Calculate score and generate feedback #
    ############################################
    # -- 100 points is the maximum that can be reached --

    # -- Giving points --
    # max 100 points if all values have been added
    points_to_give_for_added_values = len(added_values) / len(values) * 100

    # -- Deducting points --
    # deduct 5 points for each value having the wrong position
    points_to_deduct_for_wrongly_inserted_vals = len(
        wrongly_inserted_vals) * 10
    # deduct 5 points for each value (except root) having the wrong color
    points_to_deduct_for_wrongly_colored_vals = len(
        wrongly_colored_vals_without_root) * 5
    # deduct 10 points for each additional value, which was not asked for
    points_to_deduct_for_additional_values = sum(extra_vals.values()) * 10
    # deduct 10 points for each missing value from the existing tree, which should not have been removed
    points_to_deduct_for_missing_values = len(
        missing_values_based_on_existing_tree) * 10
    # deduct 5 points for each bst rule violated
    points_to_deduct_for_bst_violations = len(violations) * 10
    # deduct 10 points if the root is red (violation of a red-black tree property)
    points_to_deduct_for_root_color_violation = (
        0 if len(wrongly_colored_roots) == 0 else 1) * 10
    # deduct 5 points for each violation of red nodes having red children (violation(s) of a red-black tree property)
    points_to_deduct_for_red_red_violations = len(
        red_red_violating_node_pairs) * 10
    # deduct 10 points if there is no uniform black height (violation of a red-black tree property)
    points_to_deduct_for_black_height_violation = (
        0 if len(black_height_preleaf_nodes) == 1 else 1) * 10

    score = (0
             + points_to_give_for_added_values
             - points_to_deduct_for_wrongly_inserted_vals
             - points_to_deduct_for_wrongly_colored_vals
             - points_to_deduct_for_additional_values
             - points_to_deduct_for_missing_values
             - points_to_deduct_for_bst_violations
             - points_to_deduct_for_root_color_violation
             - points_to_deduct_for_red_red_violations
             - points_to_deduct_for_black_height_violation
             )

    ########################
    # 4. Generate feedback #
    ########################
    feedback = ""

    ### German ###
    if is_german:
        if not missing_values:
            feedback += "Alle Werte wurden eingefügt"
        else:
            der_wert_die_werte = pluralize(
                "Der Wert", "Die Werte", len(missing_values))
            wurde_wurden = pluralize("wurde", "wurden", len(missing_values))
            feedback += f"{der_wert_die_werte} {format_value_list(missing_values, is_german)} {wurde_wurden} nicht eingefügt"

            if added_values:
                feedback += ". "
                der_wert_die_werte = pluralize(
                    "Der Wert", "Die Werte", len(added_values))
                wurde_wurden = pluralize("wurde", "wurden", len(added_values))
                feedback += f"{der_wert_die_werte} {format_value_list(added_values, is_german)} {wurde_wurden} eingefügt"

        violation_msg = ""
        if violations and wrongly_inserted_vals:
            violation_msg = ", aber es gibt Verstöße gegen die Regeln für binäre Suchbäume und einige eingefügte Knoten sind an falscher Position"
        elif violations:
            violation_msg = ", aber es gibt Verstöße gegen die Regeln für binäre Suchbäume"
        elif wrongly_inserted_vals:
            violation_msg = ", aber einige eingefügte Knoten sind an falscher Position"

        feedback += violation_msg + ". "

        if wrongly_inserted_vals:
            wert_werte = pluralize("Wert", "Werte", len(wrongly_inserted_vals))
            befindet_befinden = pluralize(
                "wurde", "wurden", len(wrongly_inserted_vals))
            inkorrekter_position_inkorrekten_positionen = pluralize(
                "inkorrekter Position", "inkorrekten Positionen", len(wrongly_inserted_vals))
            er_sie = pluralize("er", "sie", len(wrongly_inserted_vals))
            der_die = pluralize("Der", "Die", len(wrongly_inserted_vals))
            sollte_sollten = pluralize(
                "sollte", "sollten", len(wrongly_inserted_vals))

            feedback += (
                f"{der_die} {wert_werte} {format_value_list(wrongly_inserted_vals, is_german)} "
                f"{befindet_befinden} sich an {inkorrekter_position_inkorrekten_positionen} im Baum, "
                f"basierend auf der Position, an der {er_sie} bei korrekter Einfüge- und Rebalancingreihenfolge erscheinen {sollte_sollten}. "
            )

        violating_values_messages = []
        for node, violation_type in violations:
            msg = describe_bst_violation(node, violation_type, is_german)
            violating_values_messages.append(msg)

        if violating_values_messages:
            feedback += "".join(violating_values_messages)

        if wrongly_colored_roots:
            feedback += (
                f"Die Wurzel mit dem Wert {format_value_list(wrongly_colored_roots, is_german)} verletzt die Rot-Schwarz-Eigenschaft, nach der die Wurzel immer schwarz sein muss."
            )

        if wrongly_colored_vals_without_root:
            der_die = pluralize("Der", "Die", len(
                wrongly_colored_vals_without_root))
            die_falsche_falsche = pluralize(
                "die falsche", "falsche", len(wrongly_colored_vals_without_root))
            wert_werte = pluralize("Wert", "Werte", len(
                wrongly_colored_vals_without_root))
            farbe_farben = pluralize("Farbe", "Farben", len(
                wrongly_colored_vals_without_root))
            hat_haben = pluralize("hat", "haben", len(
                wrongly_colored_vals_without_root))

            feedback += (
                f"{der_die} {wert_werte} {format_value_list(wrongly_colored_vals_without_root, is_german)} "
                f"{hat_haben} {die_falsche_falsche} {farbe_farben} im Baum. "
            )

        if red_red_violating_node_pairs:
            das_die = pluralize("Das", "Die", len(
                red_red_violating_node_pairs))
            eltern_kind_paar_eltern_kind_paare = pluralize(
                "Eltern-Kind-Paar", "Eltern-Kind-Paare", len(red_red_violating_node_pairs))
            red_red_violating_node_pair_text_components = [
                f"Elternteil {parent} mit Kind {child}" for parent, child in red_red_violating_node_pairs]

            feedback += (
                "In dem Baum ist die Eigenschaft verletzt, nach der rote Knoten keine roten Kinder haben dürfen. "
                f"Diese Eigenschaft wird verletzt durch {das_die} {eltern_kind_paar_eltern_kind_paare} {format_string_list(red_red_violating_node_pair_text_components, is_german)}. "
            )

        if len(black_height_preleaf_nodes) > 1:
            violating_black_height_text_components = ""
            for black_height, preleaves in black_height_preleaf_nodes:
                das_die = pluralize("Das", "Die", len(preleaves))
                blatt_blaetter = pluralize("Blatt", "Blätter", len(preleaves))
                dem_den = pluralize("dem", "den", len(set(preleaves)))
                hat_haben = pluralize("hat", "haben", len(preleaves))
                violating_black_height_text_components += f"{das_die} {blatt_blaetter} an {dem_den} Knoten {format_value_list(set(preleaves), is_german)} {hat_haben} eine Schwarzhöhe von {black_height}. "

            feedback += (
                "In dem Baum ist die Eigenschaft verletzt, nach der der Pfad von jedem Knoten zu den Blättern gleich viele schwarze Knoten auf dem Pfad haben muss, "
                "da die Schwarzhöhe (von der Wurzel aus) in diesem Baum inkonsistent ist. "
                f"{violating_black_height_text_components}"
            )

        feedback_parts = []

        if extra_vals:
            der_wert_die_werte = pluralize(
                "der Wert", "die Werte", len(extra_vals))
            ist_sind = pluralize("ist", "sind", len(extra_vals))

            feedback_parts.append(
                f"{ist_sind} {der_wert_die_werte} {format_value_list(extra_vals.keys(), is_german)} häufiger im Baum vorhanden als erwartet"
            )

        if missing_values_based_on_existing_tree:
            der_wert_die_werte = pluralize("der Wert", "die Werte", len(
                missing_values_based_on_existing_tree))
            fehlt_fehlen = pluralize("fehlt", "fehlen", len(
                missing_values_based_on_existing_tree))
            er_sie = pluralize("er", "sie", len(
                missing_values_based_on_existing_tree))
            sollte_sollten = pluralize("sollte", "sollten", len(
                missing_values_based_on_existing_tree))

            if extra_vals:
                feedback_parts.append(
                    f"{der_wert_die_werte} {format_value_list(missing_values_based_on_existing_tree, is_german)} "
                    f"{fehlt_fehlen}, obwohl {er_sie} vorhanden sein {sollte_sollten}"
                )
            else:
                feedback_parts.append(
                    f"{fehlt_fehlen} {der_wert_die_werte} {format_value_list(missing_values_based_on_existing_tree, is_german)}"
                    f", obwohl {er_sie} vorhanden sein {sollte_sollten}"
                )

        # Zusätzlich {sollte/sollten} {der Wert/die Werte} XYZ nicht im Baum auftauchen und {der Wert/die Werte} {fehlt/fehlen}

        if feedback_parts:
            feedback += "Zusätzlich " + " und ".join(feedback_parts) + ". "

    ### English ###
    else:
        if not missing_values:
            feedback += "All values were inserted into the tree"
        else:
            value_values = pluralize("value", "values", len(missing_values))
            was_were = pluralize("was", "were", len(missing_values))
            feedback += f"The {value_values} {format_value_list(missing_values, is_german)} {was_were} not inserted"

            if added_values:
                feedback += ". "
                value_values = pluralize("value", "values", len(added_values))
                was_were = pluralize("was", "were", len(added_values))
                feedback += f"The {value_values} {format_value_list(added_values, is_german)} {was_were} inserted"

        violation_msg = ""
        if violations and wrongly_inserted_vals:
            violation_msg = ", but there are binary search tree rule violations and some inserted nodes are at the wrong position"
        elif violations:
            violation_msg = ", but there are binary search tree rule violations"
        elif wrongly_inserted_vals:
            violation_msg = ", but some inserted nodes are at the wrong position"

        feedback += violation_msg + ". "

        if wrongly_inserted_vals:
            value_values = pluralize(
                "value", "values", len(wrongly_inserted_vals))
            position_positions = pluralize(
                "position", "positions", len(wrongly_inserted_vals))
            it_they = pluralize("it", "they", len(wrongly_inserted_vals))
            is_are = pluralize("is", "are", len(wrongly_inserted_vals))

            feedback += (
                f"The {value_values} {format_value_list(wrongly_inserted_vals, is_german)} "
                f"{is_are} at the incorrect {position_positions} in the tree, "
                f"based on where {it_they} should appear if inserted in the correct order and having applied correct rebalancing. "
            )

        violating_values_messages = []
        for node, violation_type in violations:
            msg = describe_bst_violation(node, violation_type, is_german)
            violating_values_messages.append(msg)

        if violating_values_messages:
            feedback += "".join(violating_values_messages)

        if wrongly_colored_roots:
            feedback += (
                f"The root with the value {format_value_list(wrongly_colored_roots, is_german)} violates the red-black property according to which the root must always be black. "
            )

        if wrongly_colored_vals_without_root:
            value_values = pluralize("value", "values", len(
                wrongly_colored_vals_without_root))
            was_were = pluralize("was", "were", len(
                wrongly_colored_vals_without_root))

            feedback += (
                f"The {value_values} {format_value_list(wrongly_colored_vals_without_root, is_german)} "
                f"{was_were} incorrectly colored in the tree. "
            )

        if red_red_violating_node_pairs:
            parent_child_pair_parent_child_pairs = pluralize(
                "parent-child pair", "parent-child pairs", len(red_red_violating_node_pairs))
            red_red_violating_node_pair_text_components = [
                f"parent {parent} with child {child}" for parent, child in red_red_violating_node_pairs]

            feedback += (
                "This tree violates the red-black property according to which red nodes are not allowed to have red children. "
                f"This property is violated through the {parent_child_pair_parent_child_pairs} {format_string_list(red_red_violating_node_pair_text_components, is_german)}. "
            )

        if len(black_height_preleaf_nodes) > 1:
            violating_black_height_text_components = ""
            for black_height, preleaves in black_height_preleaf_nodes:
                leaf_leaves = pluralize("leaf", "leaves", len(preleaves))
                node_nodes = pluralize("node", "nodes", len(set(preleaves)))
                has_have = pluralize("has", "have", len(preleaves))
                violating_black_height_text_components += f"The {leaf_leaves} of the {node_nodes} {format_value_list(set(preleaves), is_german)} {has_have} a black height of {black_height}. "

            feedback += (
                "This tree violates the red-black property which requires each path from a given node to its descendant leaves to contain the same number of black nodes, "
                "since the black height (relative to the root) is inconsistent in this tree. "
                f"{violating_black_height_text_components}"
            )

        feedback_parts = []

        if extra_vals:
            value_values = pluralize("value", "values", len(extra_vals))
            appears_appear = pluralize("appears", "appear", len(extra_vals))

            value_list_text = format_value_list(extra_vals.keys(), is_german)

            feedback_parts.append(
                f"the {value_values} {value_list_text} {appears_appear} more often than expected"
            )

        if missing_values_based_on_existing_tree:
            value_values = pluralize("value", "values", len(
                missing_values_based_on_existing_tree))
            was_were = pluralize("was", "were", len(
                missing_values_based_on_existing_tree))
            it_they = pluralize("it", "they", len(
                missing_values_based_on_existing_tree))
            feedback_parts.append(
                f"the {value_values} {format_value_list(missing_values_based_on_existing_tree, is_german)} "
                f"{was_were} missing even though {it_they} should be present"
            )

        if feedback_parts:
            feedback += "Additionally, " + " and ".join(feedback_parts) + ". "

    ####################
    # 5. Send response #
    ####################
    return score, feedback, solution
