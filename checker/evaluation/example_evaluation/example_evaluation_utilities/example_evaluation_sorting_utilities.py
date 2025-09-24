from datastructures.example import ExampleList


def get_ascending_violations(student_list: ExampleList) -> list[str]:
    """Get a list of violation messages, 
    indicating that some elements are not in sorted order when they should be sorted in ascending order.
    """
    sorting_violations = []
    for predecessor, value in zip(student_list.get_data()[:-1], student_list.get_data()[1:]):
        if predecessor > value:
            sorting_violations.append(
                f"The value {predecessor} is not allowed to be before {value}. ")
    return sorting_violations


def get_descending_violations(student_list: ExampleList) -> list[str]:
    """Get a list of violation messages, 
    indicating that some elements are not in sorted order when they should be sorted in descending order.
    """
    sorting_violations = []
    for predecessor, value in zip(student_list.get_data()[:-1], student_list.get_data()[1:]):
        if predecessor < value:
            sorting_violations.append(
                f"The value {predecessor} is not allowed to be before {value}. ")
    return sorting_violations
