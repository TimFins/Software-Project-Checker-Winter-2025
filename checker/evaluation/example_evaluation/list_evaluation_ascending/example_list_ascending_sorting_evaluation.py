from datastructures.example import ExampleList
from ..example_evaluation_utilities.example_evaluation_sorting_utilities import get_ascending_violations
from ..example_evaluation_utilities.example_evaluation_values_utilities import *


def example_list_ascending_sorting_evaluation(student_list: ExampleList, provided_list: ExampleList) -> tuple[int, str, ExampleList]:
    """Evaluate a sort in ascending order exercise, returning score, feedback and solution.
    """
    solution = provided_list.sorted(sort_ascending=True)

    # 1. Just one element to be sorted so the solution is trivial.
    if len(provided_list.get_data()) < 2:
        return 100, "Trivial solution.", solution

    # 2. No submission exists.
    if not student_list.get_data():
        return 0, "Empty submission.", solution

    # 3. The programatically created solution exactly equals the submission.
    if student_list.get_data() == solution.get_data():
        return 100, "Correct.", solution

    # 4. The submission is sorted descending and not ascending as expected.
    if student_list.get_data() == provided_list.sorted(sort_ascending=False).get_data():
        return 45, "You were supposed to sort in ascending order but sorted in descending order.", solution

    # Determine additional mistakes by using functions.
    sorting_violations = get_ascending_violations(student_list)
    missing_values = get_missing_values(student_list, provided_list)
    additional_values = get_additional_values(student_list, provided_list)

    feedback = ""
    score = 100

    # 5. Check if sorting violations exist and print them if there are any. Sorting violations mean
    # a value is not sorted into the correct place.
    if sorting_violations:
        feedback += "The list is not correctly sorted in ascending order. " + \
            "".join(sorting_violations)
        score -= len(sorting_violations) * 40

    # 6. Check if there are values missing which should be present and print them if there are any.
    if missing_values:
        feedback += f"The following values are present less often than expected: {missing_values}. "
        score -= len(missing_values) * 20

    # 7. Check if there are additional values which should not be present and print them if there are any.
    if additional_values:
        feedback += f"The following values are present more often than expected: {additional_values}. "
        score -= len(additional_values) * 20

    return score, feedback, solution
