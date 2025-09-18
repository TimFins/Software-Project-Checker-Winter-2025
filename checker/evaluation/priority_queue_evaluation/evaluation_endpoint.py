from datastructures.priorityqueue import PriorityQueueNode


def evaluate_priority_queue_task(request: dict) -> tuple[int, str, dict]:
    """Priority Queue evaluation function. Takes in the full request and delegates it to the respective evaluation pipeline.

    Score is rounded to the nearest integer and clamped [0, 100].
    Leading and trailing whitespaces are stripped from the feedback.
    """
    task_type = request["taskType"]
    def evaluator_function(
        _): return 0, "Evaluation for this task is not implemented", "{}"
    match task_type:
        case "PRIORITY_QUEUE_EXTRACT_HIGHEST_PRIORITY":
            evaluator_function = evaluate_priority_queue_extract_highest_priority_task
        case "PRIORITY_QUEUE_INSERT":
            evaluator_function = evaluate_priority_queue_insert_task
    score, feedback, solution = evaluator_function(
        request)
    score = min(max(round(score), 0), 100)
    feedback = feedback.strip()
    return score, feedback, solution


def evaluate_priority_queue_extract_highest_priority_task(request: dict):
    """ A students task is evaluated where the student was asked to extract the element with the highest priority 
    from a provided priority queue. The student did so and ended up with the student priority queue which now 
    needs to be evaluated.
    """
    try:
        student_priority_queue = PriorityQueueNode.from_dict(
            request["studentPriorityQueue"])
        print("StudentPriorityQueue:")
        if student_priority_queue:
            student_priority_queue.print_tree()
        else:
            print("StudentPriorityQueue is empty.")
    except:
        raise ValueError("StudentPriorityQueue has an incorrect format.")

    try:
        print("ProvidedPriorityQueue:")
        provided_avl_tree = PriorityQueueNode.from_dict(
            request["providedPriorityQueue"])
        if provided_avl_tree:
            provided_avl_tree.print_tree()
        else:
            print("ProvidedPriorityQueue is empty.")
    except:
        raise ValueError("ProvidedPriorityQueue has an incorrect format.")

    print("Is Max Priority Queue:")
    print(is_max_priority_queue(request))

    """ Here, after parsing the JSON into the according class structures, the evaluation should take place.
    Therefore, you should first create a solution which is used to compare it against the student priority queue.
    After creating the solution, in different functions comparisons should take place which determine which
    exact mistakes were made and based on that generate the feedback and calculate a score.
    """

    score, feedback, solution = 100, f"The feedback isn't implemented yet for priority queue (extract highest priority): {'MAX' if is_max_priority_queue(request) else 'MIN'}", "The solution isn't implemented yet."
    return score, feedback, solution


def evaluate_priority_queue_insert_task(request: dict):
    """ A students task is evaluated where the student was asked to insert the values into the provided priority queue.
    The student did so and ended up with the student priority queue which now needs to be evaluated.
    """
    try:
        student_priority_queue = PriorityQueueNode.from_dict(
            request["studentPriorityQueue"])
        print("StudentPriorityQueue:")
        if student_priority_queue:
            student_priority_queue.print_tree()
        else:
            print("StudentPriorityQueue is empty.")
    except:
        raise ValueError("StudentPriorityQueue has an incorrect format.")

    try:
        print("ProvidedPriorityQueue:")
        provided_avl_tree = PriorityQueueNode.from_dict(
            request["providedPriorityQueue"])
        if provided_avl_tree:
            provided_avl_tree.print_tree()
        else:
            print("ProvidedPriorityQueue is empty.")
    except:
        raise ValueError("ProvidedPriorityQueue has an incorrect format.")

    print("Is Max Priority Queue:")
    print(is_max_priority_queue(request))

    values = request.get("values")
    print("Values:")
    print(values)

    """ Here, after parsing the JSON into the according class structures, the evaluation should take place.
    Therefore, you should first create a solution which is used to compare it against the student priority queue.
    After creating the solution, in different functions comparisons should take place which determine which
    exact mistakes were made and based on that generate the feedback and calculate a score.
    """

    score, feedback, solution = 100, f"The feedback isn't implemented yet for priority queue (insert): {'max' if is_max_priority_queue(request) else 'min'}", "The solution isn't implemented yet."
    return score, feedback, solution


def is_max_priority_queue(request: dict) -> bool:
    """Determines whether the request demands the priority queue to be interpreted
    as a min-priority queue or max-priority queue.
    """
    max_priority_queue_type = request.get("priorityQueueType")

    if max_priority_queue_type == "MAX":
        return True
    elif max_priority_queue_type == "MIN":
        return False
    else:
        raise ValueError(
            f"Invalid priorityQueueType: {max_priority_queue_type}")
