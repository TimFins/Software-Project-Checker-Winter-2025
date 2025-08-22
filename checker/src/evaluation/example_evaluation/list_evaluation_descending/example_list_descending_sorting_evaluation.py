from datastructures.example import ExampleList

def example_list_descending_sorting_evaluation(student_list: ExampleList, provided_list: ExampleList) -> tuple[int, str, ExampleList]:
    correct_sorted_list = provided_list.sorted(asc=False)
    asc_sorted_list = provided_list.sorted(asc=True)

    if correct_sorted_list == student_list:
        return 100, "Correct!", correct_sorted_list
    elif asc_sorted_list == student_list:
        return 50, "The list was sorted ascending not descending.", correct_sorted_list
    else:
        return 0, "Incorrect! Some values aren't correctly sorted.", correct_sorted_list