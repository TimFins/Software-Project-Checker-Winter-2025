from datastructures.example import ExampleList
from ..example_evaluation_utilities.example_evaluation_sorting_utilities import get_descending_violations
from ..example_evaluation_utilities.example_evaluation_values_utilities import *


def example_list_descending_sorting_evaluation(student_list: ExampleList, provided_list: ExampleList) -> tuple[int, str, ExampleList]:
    solution = provided_list.sorted(sort_ascending=False)

    if len(provided_list.get_data()) < 2:
        return 100, "Trivial solution.", solution

    if not student_list.get_data():
        return 0, "Empty submission.", solution

    if student_list.get_data() == solution.get_data():
        return 100, "Correct.", solution

    if student_list.get_data() == provided_list.sorted(sort_ascending=True).get_data():
        return 45, "You were supposed to sort in descending order but sorted in ascending order."

    sorting_violations = get_descending_violations(student_list)
    missing_values = get_missing_values(student_list, provided_list)
    additional_values = get_additional_values(student_list, provided_list)

    feedback = ""
    score = 100

    if sorting_violations:
        feedback += "The list is not correctly sorted in descending order. " + \
            "".join(sorting_violations)
        score -= len(sorting_violations) * 40

    if missing_values:
        feedback += f"The following values are present less often than expected: {missing_values}. "
        score -= len(missing_values) * 20

    if additional_values:
        feedback += f"The following values are present more often than expected: {additional_values}. "
        score -= len(additional_values) * 20

    return score, feedback, solution
