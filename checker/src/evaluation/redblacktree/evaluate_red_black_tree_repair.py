from binarytrees import RedBlackTreeNode
from .red_black_tree_algorithms import get_red_black_tree_repair_checkpoints, find_node_causing_violation
from .evaluate_red_black_tree import *
from evaluation.text_utils import *

task_type = "RED_BLACK_TREE_REPAIR"


def red_black_tree_repair_evaluation(existing_tree: RedBlackTreeNode, student_tree: RedBlackTreeNode, is_german: bool = True):
    ####################################################################################
    # 1. Solve the task yourself (with existing_tree and or values, depending on task) #
    ####################################################################################
    try:
        checkpoints = get_red_black_tree_repair_checkpoints(
            existing_tree.deep_copy())
    except ValueError:
        if is_german:
            feedback = "Die Aufgabe ist ungültig, da der bereitgestellte Baum bereits valide ist und nicht repariert werden kann. "
        else:
            feedback = "The task is invalid, since the provided tree is already valid and therefore does not need to be repaired. "
        return 100, feedback, existing_tree
    solution = checkpoints[-1]

    ##################################################
    # 2. Compare your solution with the student tree #
    ##################################################
    # Edge case: Empty Submission
    if student_tree is None:
        if is_german:
            return 0, "Leere Abgabe.", solution
        else:
            return 0, "Empty Submission.", solution

    violations = get_bst_rule_violating_nodes(student_tree, list(
        map(lambda node: node.get_value(), student_tree.inorder_traverse())))
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
    # First check whether a checkpoint was hit. In that case the task is solved correctly or steps were omitted. But in that case, the feedback should be really concise.
    reached_checkpoint = get_reached_checkpoint(checkpoints, student_tree)

    if reached_checkpoint == len(checkpoints):
        if is_german:
            feedback = "Der Rot-Schwarz-Baum wurde erfolgreich repariert. "
        else:
            feedback = "The red-black tree was repaired successfully. "
        return 100, feedback, solution
    elif reached_checkpoint > 0:
        score = 50 + (reached_checkpoint / len(checkpoints)) * 50
        violating_node, violation_type = find_node_causing_violation(
            checkpoints[reached_checkpoint-1])
        feedback = ""
        if is_german:
            zahl_verbalisierung = {1: "einer", 2: "zwei", 3: "drei", 4: "vier", 5: "fünf",
                                   6: "sechs", 7: "sieben", 8: "acht", 9: "neun", 10: "zehn", 11: "elf", 12: "zwölf"}
            reached_checkpoint_verbalisierung = zahl_verbalisierung.get(
                reached_checkpoint, str(reached_checkpoint))
            total_checkpoints_verbalisierung = zahl_verbalisierung.get(
                len(checkpoints), str(len(checkpoints)))
            wurde_wurden = pluralize("wurde", "wurden", reached_checkpoint)
            feedback += f"Von den {total_checkpoints_verbalisierung} benötigten Reparaturschritten {wurde_wurden} nur {reached_checkpoint_verbalisierung} ausgeführt. "
            if violation_type == "RED_ROOT":
                feedback += f"Knoten {violating_node.get_value()} verletzt immer noch die Rot-Schwarz-Eigenschaft, nach der die Wurzel immer schwarz sein muss. "
            elif violation_type == "RED_RED":
                violating_parent = violating_node.get_parent()
                feedback += (
                    f"Knoten {violating_node.get_value()} verletzt immer noch die Rot-Schwarz-Eigenschaft, nach der rote Knoten keine roten Kinder haben dürfen, "
                    f"da sowohl Knoten {violating_node.get_value()} als auch sein Elternknoten {violating_parent.get_value()} rot sind. "
                )
        else:
            number_verbalization = {1: "one", 2: "two", 3: "three", 4: "four",
                                    5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}
            reached_checkpoint_verbalization = number_verbalization.get(
                reached_checkpoint, str(reached_checkpoint))
            total_checkpoints_verbalization = number_verbalization.get(
                len(checkpoints), str(len(checkpoints)))
            was_were = pluralize("was", "were", reached_checkpoint)
            feedback += f"Out of the {total_checkpoints_verbalization} required repair steps, only {reached_checkpoint_verbalization} {was_were} performed. "
            if violation_type == "RED_ROOT":
                feedback += f"Node {violating_node.get_value()} still violates the red-black property according to which the root must be black. "
            elif violation_type == "RED_RED":
                violating_parent = violating_node.get_parent()
                feedback += (
                    f"Node {violating_node.get_value()} still violates the red-black property according to which red nodes are not allowed to have red children, "
                    f"since node {violating_node.get_value()} is red and its parent {violating_parent.get_value()} is also red. "
                )
        return score, feedback, solution

    # From here on, it is clear, that the student did not solve the task correctly and did not prematurely stop at one of the checkpoints towards the solution.
    # That implies, that the problem is improper rebalancing or other issues, not unique to the type of task at hand.
    # Therefore the submission is now just compared with the solution.
    # -- 100 points is the maximum that can be reached --

    # -- Giving points --
    # give 100 base points
    points_to_add_for_baseline = 100

    # -- Deducting points --
    # deduct 5 points for each value having the wrong position
    points_to_deduct_for_wrongly_inserted_vals = len(
        wrongly_inserted_vals) * 10
    # deduct 5 points for each value (except root) having the wrong color
    points_to_deduct_for_wrongly_colored_vals = len(
        wrongly_colored_vals_without_root) * 10
    # deduct 15 points for each additional value, which was not asked for
    points_to_deduct_for_additional_values = sum(extra_vals.values()) * 15
    # deduct 15 points for each missing value from the existing tree, which should not have been removed
    points_to_deduct_for_missing_values = len(
        missing_values_based_on_existing_tree) * 15
    # deduct 10 points for each bst rule violated
    points_to_deduct_for_bst_violations = len(violations) * 10
    # deduct 15 points if the root is red (violation of a red-black tree property)
    points_to_deduct_for_root_color_violation = (
        0 if len(wrongly_colored_roots) == 0 else 1) * 15
    # deduct 10 points for each violation of red nodes having red children (violation(s) of a red-black tree property)
    points_to_deduct_for_red_red_violations = len(
        red_red_violating_node_pairs) * 5
    # deduct 15 points if there is no uniform black height (violation of a red-black tree property)
    points_to_deduct_for_black_height_violation = (
        0 if len(black_height_preleaf_nodes) == 1 else 1) * 15

    score = (0
             + points_to_add_for_baseline
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

        violation_msg = ""
        if violations and wrongly_inserted_vals:
            violation_msg = "Es gibt Verstöße gegen die Regeln für binäre Suchbäume und einige eingefügte Knoten sind an falscher Position. "
        elif violations:
            violation_msg = "Es gibt Verstöße gegen die Regeln für binäre Suchbäume. "
        elif wrongly_inserted_vals:
            violation_msg = "Einige eingefügte Knoten sind an falscher Position. "
        feedback += violation_msg

        if wrongly_inserted_vals:
            wert_werte = pluralize("Wert", "Werte", len(wrongly_inserted_vals))
            inkorrekter_position_inkorrekten_positionen = pluralize(
                "inkorrekter Position", "inkorrekten Positionen", len(wrongly_inserted_vals))
            wurde_wurden = pluralize(
                "wurde", "wurden", len(wrongly_inserted_vals))
            befindet_befinden = pluralize(
                "befindet", "befinden", len(wrongly_inserted_vals))
            er_sie = pluralize("er", "sie", len(wrongly_inserted_vals))
            der_die = pluralize("Der", "Die", len(wrongly_inserted_vals))
            sollte_sollten = pluralize(
                "sollte", "sollten", len(wrongly_inserted_vals))

            feedback += (
                f"{der_die} {wert_werte} {format_value_list(wrongly_inserted_vals, is_german)} "
                f"{befindet_befinden} sich an {inkorrekter_position_inkorrekten_positionen} im Baum, "
                f"basierend auf der Position, an der {er_sie} bei korrekter Rebalancingreihenfolge erscheinen {sollte_sollten}. "
            )

        violating_values_messages = []
        for node, violation_type in violations:
            msg = describe_bst_violation(node, violation_type, is_german)
            violating_values_messages.append(msg)

        if violating_values_messages:
            feedback += "".join(violating_values_messages)

        if wrongly_colored_roots:
            feedback += (
                f"Die Wurzel mit dem Wert {format_value_list(wrongly_colored_roots, is_german)} verletzt die Rot-Schwarz-Eigenschaft, nach der die Wurzel immer schwarz sein muss. "
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
                "Der Wert", "Die Werte", len(extra_vals))
            ist_sind = pluralize("ist", "sind", len(extra_vals))

            feedback_parts.append(
                f"{der_wert_die_werte} {format_value_list(extra_vals.keys(), is_german)} {ist_sind} häufiger im Baum vorhanden als erwartet"
            )

        if missing_values_based_on_existing_tree:
            der_wert_die_werte = pluralize("Der Wert", "Die Werte", len(
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
                    f"{der_wert_die_werte} {format_value_list(missing_values_based_on_existing_tree, is_german)} "
                    f"{fehlt_fehlen}, obwohl {er_sie} vorhanden sein {sollte_sollten}"
                )

        # Zusätzlich {sollte/sollten} {der Wert/die Werte} XYZ nicht im Baum auftauchen und {der Wert/die Werte} {fehlt/fehlen}

        if feedback_parts:
            feedback += " und ".join(feedback_parts) + ". "

    ### English ###
    else:
        violation_msg = ""
        if violations and wrongly_inserted_vals:
            violation_msg = "There are binary search tree rule violations and some inserted nodes are at the wrong position. "
        elif violations:
            violation_msg = "There are binary search tree rule violations. "
        elif wrongly_inserted_vals:
            violation_msg = "Some inserted nodes are at the wrong position. "

        feedback += violation_msg

        if wrongly_inserted_vals:
            value_values = pluralize(
                "value", "values", len(wrongly_inserted_vals))
            position_positions = pluralize(
                "position", "positions", len(wrongly_inserted_vals))
            is_are = pluralize("is", "are", len(wrongly_inserted_vals))
            it_they = pluralize("it", "they", len(wrongly_inserted_vals))

            feedback += (
                f"The {value_values} {format_value_list(wrongly_inserted_vals, is_german)} "
                f"{is_are} located at the incorrect {position_positions} in the tree, "
                f"based on where {it_they} should appear if having applied correct rebalancing. "
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
