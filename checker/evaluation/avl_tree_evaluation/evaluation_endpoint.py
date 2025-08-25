from datastructures.avltree import AVLTree

def evaluate_avl_tree_task(request: dict) -> tuple[int, str, dict]:
    """AVL tree evaluation function. Takes in the full request and delegates it to the respective evaluation pipeline.

    Score is rounded to the nearest integer and clamped [0, 100].
    Leading and trailing whitespaces are stripped from the feedback.
    """
    task_type = request["taskType"]
    def evaluator_function(
        _): return 0, "Evaluation for this task is not implemented", "{}"
    match task_type:
        case "AVL_TREE_INSERT":
            evaluator_function = evaluate_avl_tree_insert_task
        case "AVL_TREE_DELETE":
            evaluator_function = evaluate_avl_tree_delete_task
    score, feedback, solution = evaluator_function(
        request)
    score = min(max(round(score), 0), 100)
    feedback = feedback.strip()
    return score, feedback, solution

def evaluate_avl_tree_insert_task(request: dict):
    """ A students task is evaluated where the student was asked to insert the values into the provided avl tree.
    The student did so and ended up with the student avl tree which now needs to be evaluated.
    """
    try:
        student_avl_tree = AVLTree.from_dict( request["studentAVLTree"])
        print("StudenAVLTree:")
        if student_avl_tree: 
            student_avl_tree.print_tree()
        else:
            print("StudentAVLTree is empty.")
    except:
        raise ValueError("StudentAVLTree has an incorrect format.")
    
    try:
        print("ProvidedAVLTree:")
        provided_avl_tree = AVLTree.from_dict(request["providedAVLTree"])
        if provided_avl_tree: 
            provided_avl_tree.print_tree()
        else:
            print("ProvidedAVLTree is empty.")
    except:
        raise ValueError("ProvidedAVLTree has an incorrect format.")

    values = request.get("values")
    print("Values:")
    print(values)

    """ Here, after parsing the JSON into the according class structures, the evaluation should take place.
    Therefore, you should first create a solution which is used to compare it against the student avl tree.
    After creating the solution, in different functions comparisons should take place which determine which
    exact mistakes were made and based on that generate the feedback and calculate a score.
    """
   
    score, feedback, solution = 100, "The feedback isn't implemented yet.", "The solution isn't implemented yet."
    return score, feedback, solution

def evaluate_avl_tree_delete_task(request: dict):
    """ A students task is evaluated where the student was asked to delete the values from the provided avl tree.
    The student did so and ended up with the student avl tree which now needs to be evaluated.
    """
    try:
        student_avl_tree = AVLTree.from_dict( request["studentAVLTree"])
        print("StudenAVLTree:")
        if student_avl_tree: 
            student_avl_tree.print_tree()
        else:
            print("StudentAVLTree is empty.")
    except:
        raise ValueError("StudentAVLTree has an incorrect format.")
    
    try:
        print("ProvidedAVLTree:")
        provided_avl_tree = AVLTree.from_dict(request["providedAVLTree"])
        if provided_avl_tree: 
            provided_avl_tree.print_tree()
        else:
            print("ProvidedAVLTree is empty.")
    except:
        raise ValueError("ProvidedAVLTree has an incorrect format.")

    values = request.get("values")
    print("Values:")
    print(values)

    """ Here, after parsing the JSON into the according class structures, the evaluation should take place.
    Therefore, you should first create a solution which is used to compare it against the student avl tree.
    After creating the solution, in different functions comparisons should take place which determine which
    exact mistakes were made and based on that generate the feedback and calculate a score.
    """
   
    score, feedback, solution = 100, "The feedback isn't implemented yet.", "The solution isn't implemented yet."
    return score, feedback, solution