# Evaluator Microservice For AVL Trees

The goal of this example is to create a Python microservice, which provides detailed feedback to students solving AVL tree exercises. The rough outline follows the example in `02_Example_List_Sorting_Evaluation`, but instead the endpoint `/avl-tree-evaluation` is used for evaluating AVL tree exercises.

## Request

The route requires the following JSON input:

- The **studentAVLTree** (the students submission, **mandatory**).
- The **providedAVLTree** (initial AVL tree. May be empty, **optional**).
- The **values** (which are to be inserted into the AVL tree, **mandatory**).
- The **taskType** (the task type ("**AVL_TREE_INSERT**"), **mandatory**).

Inside the route's function, the task is programmatically solved using the **AVLTreeNode** class. The student's submission is then compared against the expected solution, and feedback with an appropriate score is returned.

The request has the following JSON format:

```json
{
    "studentAVLTree": ...,
    "providedAVLTree": ...,
    "values": ...,
    "taskType": ...
}
```

### Example request using cURL

Flask uses port 5000 by default. In that case, you can use this cURL command to test the HTTP server.

```sh
TODO: Insert example cURL request
```

### Example request using PowerShell on Windows

Flask uses port 5000 by default. In that case, you can use this command in Windows PowerShell to test the HTTP server.

```sh
TODO: Insert example PowerShell request
```

### More requests when using Insomnia

We recommend using Insomnia for easier testing. We have provided a `requests.yml` in this directory with more examples. We would highly advise you trying it out. Please consult `03_Insomnia_Installation` with a guide on how to get started with Insomnia.

## Evaluation functions

The evaluation functions for evaluating AVL tree exercises are stored in the `evaluation/avl_tree_evaluation` directory. We highly recommend to structure your evaluation directory similar to how we have done so in `02_Example_List_Sorting_Evaluation`.

## Response

The response has an HTTP status code of 200 (OK). The response includes:

- **score** (from 0 to 100)
- **feedback** as text
- **solution** the correct solution as JSON

The response has the following JSON format:

```json
{
    "score": ...,
    "feedback": ...,
    "solution": ...
}
```

## The AVLTreeNode Class

The class can be imported using:

```python
from datastructures.avltree import AVLTreeNode
```

You can find a Python file showcasing the most important functionalities of this class in `checker/example_usage_avl_tree.py`.

Below is an explanation of the most relevant attributes and methods of the `AVLTreeNode` class. The source code for this class can be found in `checker/datastructures/avltree/_classes/AVLTreeNode.py` but ideally you should not have to concern yourself with that.

Method/Attribute                       | Datatype(s)                                       | Notes
-------------------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
**value** _(setter, getter)_           | `int`                                             | Value of the node.
**balance** _(setter, getter)_         | `int`                                             | Balance value of the node. `0` → left and right subtrees are balanced. `>0` → left subtree is taller than right subtree. `<0` → right subtree is taller than left subtree. This class does not automatically update the balance value. It has to be updated manually by calling `set_balance()` or directly altering the `_balance` attribute behind it.
**left_child** _(setter, getter)_      | `AVLTreeNode` or `None`                           | Left child of the node.
**right_child** _(setter, getter)_     | `AVLTreeNode` or `None`                           | Right child of the node.
**parent** _(setter, getter)_          | `AVLTreeNode` or `None`                           | Parent of the node.
**==**                                 | accepts `AVLTreeNode`                             | Compares whether two nodes have the same value. Subtrees are not checked.
**is_equal_including_subtrees(other)** | accepts `AVLTreeNode`                             | Compares whether two nodes have the same value and balance value. Additionally makes sure, that the entire left and right subtrees are also equal.
**preorder_traverse()**                | returns `list[AVLTreeNode]`                       | Returns the node and its descendants as a list in the order after preorder traversal.
**inorder_traverse()**                 | returns `list[AVLTreeNode]`                       | Returns the node and its descendants as a list in the order after inorder traversal.
**postorder_traverse()**               | returns `list[AVLTreeNode]`                       | Returns the node and its descendants as a list in the order after postorder traversal.
**to_dict()**                          | returns `dict[str, any]`                          | Converts node and subtrees to a dictionary, just like the one in the input.
**print_tree()**                       |                                                   | Prints formatted structure of node and subtrees to STDOUT.
**generate_tree_image(title)**         | optionally accepts `str` or `None`, returns `str` | Generate a base 64 encoded string containing the AVL tree as PNG, which can e.g., be written to a file. Optionally one can provide a string title, which will be included at the top of the image. If it cannot be generated, an exception is raised containing the original error message. The idea behind this method is, that it can be used for debugging.
**display_tree_image(title, img)**     | optionally accepts (`str` or `None`) and `str`    | Generates an image of the AVL tree and displays it in an image viewer. One can optionally provide a title to be shown at the top of the image. One can also provide a base64-encoded string containing the image as input. If none is provided, then one is automatically generated. If an image string is provided, the title is ignored, since the generated image will already have a title. If it cannot be generated or displayed, the user is informed. The idea is, that it can be used for debugging.
**deep_copy()**                        | returns `AVLTreeNode`                             | Creates a deep copy of the node and subtrees. The copy can be modified without affecting the original.
AVLTreeNode.**from_dict(dict)**        | accepts `dict[str, any]`, returns `AVLTreeNode`   | Class method, which takes a dictionary as input and converts it to a `AVLTreeNode` with all its subtrees.
