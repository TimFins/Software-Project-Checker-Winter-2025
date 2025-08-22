from binarytrees import BinaryTreeNode, RedBlackTreeNode
import json
from .binarysearchtree.evaluate_binary_search_tree_insertion import binary_search_tree_insertion_evaluation
from .binarysearchtree.evaluate_binary_search_tree_deletion import binary_search_tree_deletion_evaluation
from .redblacktree.evaluate_red_black_tree_insertion import red_black_tree_insertion_evaluation
from .redblacktree.evaluate_red_black_tree_repair import red_black_tree_repair_evaluation
import logging

logger = logging.getLogger(__name__)


def evaluate_binary_tree_task(request: dict) -> tuple[int, str, dict]:
    """Generic binary tree evaluation function. Takes in the full request and delegates it to the respective evaluation pipeline.

    Score is rounded to the nearest integer and clamped [0, 100].
    Leading and trailing whitespaces are stripped from the feedback.
    """
    task_type = request["taskType"]
    language = request["jobMetaInfo"]["locale"]
    def evaluator_function(
        _): return 0, "Evaluation for this task is not implemented", "{}"
    match task_type:
        case "BINARY_SEARCH_TREE_INSERT":
            evaluator_function = evaluate_binary_search_tree_insertion
        case "BINARY_SEARCH_TREE_DELETE":
            evaluator_function = evaluate_binary_search_tree_deletion
        case "RED_BLACK_TREE_INSERT":
            evaluator_function = evaluate_red_black_tree_insertion
        case "RED_BLACK_TREE_REPAIR":
            evaluator_function = evaluate_red_black_tree_repair
    score, feedback, solution = evaluator_function(
        request, (False if language == "en" else True))
    score = min(max(round(score), 0), 100)
    feedback = feedback.strip()
    return score, feedback, solution


def evaluate_binary_search_tree_insertion(request, is_german: bool = True):
    existing_tree_json_data = request.get("existingTree")
    student_tree_json_data = request.get("studentTree")
    values = request.get("values")

    try:
        if existing_tree_json_data != '{}':
            existing_tree = BinaryTreeNode.from_dict(
                json.loads(existing_tree_json_data))
        else:
            existing_tree = None
    except Exception as e:
        logger.error(f"Existing tree could not be parsed from JSON: {e}")
        raise Exception(f"Existing tree could not be parsed from JSON: {e}")

    try:
        if student_tree_json_data != '{}':
            student_tree = BinaryTreeNode.from_dict(
                json.loads(student_tree_json_data))
        else:
            student_tree = None
    except Exception as e:
        logger.error(f"Student tree could not be parsed from JSON: {e}")
        raise Exception(f"Student tree could not be parsed from JSON: {e}")

    score, feedback, solution = binary_search_tree_insertion_evaluation(
        existing_tree, values, student_tree, is_german)
    return score, feedback, solution.to_dict() if solution else '{}'


def evaluate_binary_search_tree_deletion(request, is_german: bool = True):
    existing_tree_json_data = request.get("existingTree")
    student_tree_json_data = request.get("studentTree")
    values = request.get("values")

    try:
        if existing_tree_json_data != '{}':
            existing_tree = BinaryTreeNode.from_dict(
                json.loads(existing_tree_json_data))
        else:
            existing_tree = None
    except Exception as e:
        logger.error(f"Existing tree could not be parsed from JSON: {e}")
        raise Exception(f"Existing tree could not be parsed from JSON: {e}")

    try:
        if student_tree_json_data != '{}':
            student_tree = BinaryTreeNode.from_dict(
                json.loads(student_tree_json_data))
        else:
            student_tree = None
    except Exception as e:
        logger.error(f"Student tree could not be parsed from JSON: {e}")
        raise Exception(f"Student tree could not be parsed from JSON: {e}")

    score, feedback, solution = binary_search_tree_deletion_evaluation(
        existing_tree, values, student_tree, is_german)

    return score, feedback, solution.to_dict() if solution else '{}'


def evaluate_red_black_tree_insertion(request, is_german: bool = True):
    existing_tree_json_data = request.get("existingTree")
    student_tree_json_data = request.get("studentTree")
    values = request.get("values")

    try:
        if existing_tree_json_data != '{}':
            existing_tree = RedBlackTreeNode.from_dict(
                json.loads(existing_tree_json_data))
        else:
            existing_tree = None
    except Exception as e:
        logger.error(f"Existing tree could not be parsed from JSON: {e}")
        raise Exception(f"Existing tree could not be parsed from JSON: {e}")

    try:
        if student_tree_json_data != '{}':
            student_tree = RedBlackTreeNode.from_dict(
                json.loads(student_tree_json_data))
        else:
            student_tree = None
    except Exception as e:
        logger.error(f"Student tree could not be parsed from JSON: {e}")
        raise Exception(f"Student tree could not be parsed from JSON: {e}")

    score, feedback, solution = red_black_tree_insertion_evaluation(
        existing_tree, values, student_tree, is_german)
    return score, feedback, solution.to_dict() if solution else '{}'


def evaluate_red_black_tree_repair(request, is_german: bool = True):
    existing_tree_json_data = request.get("existingTree")
    student_tree_json_data = request.get("studentTree")

    try:
        if existing_tree_json_data != '{}':
            existing_tree = RedBlackTreeNode.from_dict(
                json.loads(existing_tree_json_data))
        else:
            existing_tree = None
    except Exception as e:
        logger.error(f"Existing tree could not be parsed from JSON: {e}")
        raise Exception(f"Existing tree could not be parsed from JSON: {e}")

    try:
        if student_tree_json_data != '{}':
            student_tree = RedBlackTreeNode.from_dict(
                json.loads(student_tree_json_data))
        else:
            student_tree = None
    except Exception as e:
        logger.error(f"Student tree could not be parsed from JSON: {e}")
        raise Exception(f"Student tree could not be parsed from JSON: {e}")

    score, feedback, solution = red_black_tree_repair_evaluation(
        existing_tree, student_tree, is_german)
    return score, feedback, solution.to_dict() if solution else '{}'
