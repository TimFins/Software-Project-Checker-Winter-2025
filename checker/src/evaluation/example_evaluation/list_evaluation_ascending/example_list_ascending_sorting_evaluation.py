from datastructures.example import ExampleList

def example_list_ascending_sorting_evaluation(student_list: ExampleList, provided_list: ExampleList) -> tuple[int, str, ExampleList]:
    correct_sorted_list = provided_list.sorted(asc=True)
    desc_sorted_list = provided_list.sorted(asc=False)

    if correct_sorted_list == student_list:
        return 100, "Correct!", correct_sorted_list
    elif desc_sorted_list == student_list:
        return 50, "The list was sorted descending not ascending.", correct_sorted_list
    else:
        return 0, "Incorrect! Some values aren't correctly sorted.", correct_sorted_list