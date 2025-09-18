from collections import Counter
from datastructures.example import ExampleList


def get_additional_values(student_list: ExampleList, provided_list: ExampleList) -> list[str]:
    """Returns a sorted list of values, which are present in the submission, but should not be there.
    """
    student_list_counter = Counter(student_list.get_data())
    provided_list_counter = Counter(provided_list.get_data())

    return sorted(list({value for value in student_list_counter if student_list_counter[value] > provided_list_counter[value]}))


def get_missing_values(student_list: ExampleList, provided_list: ExampleList) -> list[str]:
    """Returns a sorted list of values, which should be present in the submission, but are not.
    """
    student_list_counter = Counter(student_list.get_data())
    provided_list_counter = Counter(provided_list.get_data())

    return sorted(list({value for value in provided_list_counter if student_list_counter[value] < provided_list_counter[value]}))
