from collections import Counter
from datastructures.example import ExampleList


def get_additional_values(student_list: ExampleList, provided_list: ExampleList):
    student_list_counter = Counter(student_list.get_data())
    provided_list_counter = Counter(provided_list.get_data())

    return sorted(list({value for value in student_list_counter if student_list_counter[value] > provided_list_counter[value]}))


def get_missing_values(student_list: ExampleList, provided_list: ExampleList):
    student_list_counter = Counter(student_list.get_data())
    provided_list_counter = Counter(provided_list.get_data())

    return sorted(list({value for value in provided_list_counter if student_list_counter[value] < provided_list_counter[value]}))
