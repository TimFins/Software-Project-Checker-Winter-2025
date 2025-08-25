from datastructures.example import ExampleList
from .list_evaluation_ascending.example_list_ascending_sorting_evaluation import example_list_ascending_sorting_evaluation
from .list_evaluation_descending.example_list_descending_sorting_evaluation import example_list_descending_sorting_evaluation


def evaluate_list_sorting_task(request: dict) -> tuple[int, str, dict]:
    """Generic example list evaluation function. Takes in the full request and delegates it to the respective evaluation pipeline.

    Score is rounded to the nearest integer and clamped [0, 100].
    Leading and trailing whitespaces are stripped from the feedback.
    """
    task_type = request["taskType"]
    def evaluator_function(
        _): return 0, "Evaluation for this task is not implemented", "{}"
    match task_type:
        case "EXAMPLE_LIST_SORT_ASCENDING":
            evaluator_function = evaluate_ascending_sorting_task
        case "EXAMPLE_LIST_SORT_DESCENDING":
            evaluator_function = evaluate_descending_sorting_task
    score, feedback, solution = evaluator_function(
        request)
    score = min(max(round(score), 0), 100)
    feedback = feedback.strip()
    return score, feedback, solution


def evaluate_ascending_sorting_task(request: dict):
    try:
        student_list = ExampleList(request["studentList"])
    except:
        raise ValueError("StudentList has an incorrect format.")

    try:
        provided_list = ExampleList(request["providedList"])
    except:
        raise ValueError("ProvidedList has an incorrect format.")

    score, feedback, solution = example_list_ascending_sorting_evaluation(
        student_list, provided_list)
    return score, feedback, solution.get_data() if solution else '{}'


def evaluate_descending_sorting_task(request: dict):
    try:
        student_list = ExampleList(request["studentList"])
    except:
        raise ValueError("StudentList has an incorrect format.")

    try:
        provided_list = ExampleList(request["providedList"])
    except:
        raise ValueError("ProvidedList has an incorrect format.")

    score, feedback, solution = example_list_descending_sorting_evaluation(
        student_list, provided_list)
    return score, feedback, solution.get_data() if solution else '{}'
