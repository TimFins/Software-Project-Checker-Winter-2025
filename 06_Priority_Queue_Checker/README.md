# Evaluator Microservice For Priority Queues

The goal of this example is to create a Python microservice, which provides detailed feedback to students solving priority queue exercises. The rough outline follows the example in `02_Example_List_Sorting_Evaluation`, but instead the endpoint `/priority-queue-evaluation` is used for evaluating priority queue exercises.

## Request

Inside each route's function, the task is programmatically solved using the **PriorityQueueNode** class. The student's submission is then compared against the expected solution, and feedback with an appropriate score is returned. The route features two different exercises, which require different JSON input:

### Insertion

Inserting values into a priority queue. This task receives the following inputs:

- The **studentPriorityQueue** (the students submission, **mandatory**).
- The **providedPriorityQueue** (initial priority queue. May be empty, **optional**).
- The **values** (which are to be inserted into the priority queue, **mandatory**).
- The **priorityQueueType** (`"MIN"` for min-priority queue or `"MAX"` for max-priority queue, **mandatory**).
- The **taskType** (the task type ("**PRIORITY_QUEUE_INSERT**"), **mandatory**).

The request has the following JSON format:

```json
{
    "studentPriorityQueue": ...,
    "providedPriorityQueue": ...,
    "values": ...,
    "priorityQueueType": ...,
    "taskType": ...
}
```

### Extraction

Extracting the highest priority value a given number of times. So calling `extract_min()` or `extract_max()` a given number of times sequentially. This task gets the following inputs:

- The **studentPriorityQueue** (the students submission, **mandatory**).
- The **providedPriorityQueue** (initial priority queue, **mandatory**).
- The **extractCount** (the amount of times the highest priority item should be extracted, **mandatory**).
- The **priorityQueueType** (`"MIN"` for min-priority queue or `"MAX"` for max-priority queue, **mandatory**).
- The **taskType** (the task type ("**PRIORITY_QUEUE_EXTRACT_HIGHEST_PRIORITY**"), **mandatory**).

The request has the following JSON format:

```json
{
    "studentPriorityQueue": ...,
    "providedPriorityQueue": ...,
    "extractCount": ...,
    "priorityQueueType": ...,
    "taskType": ...
}
```

### Example request using cURL

Flask uses port 5000 by default. In that case, you can use this cURL command to test the HTTP server.

```sh
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"studentPriorityQueue":{"value":3,"left":{"value":4,"left":null,"right":null},"right":{"value":5,"left":null,"right":null}},"providedPriorityQueue":{"value":1,"left":{"value":2,"left":{"value":4,"left":null,"right":null},"right":{"value":5,"left":null,"right":null}},"right":{"value":3,"left":null,"right":null}},"priorityQueueType":"MIN","extractCount":3,"taskType":"PRIORITY_QUEUE_EXTRACT_HIGHEST_PRIORITY"}' http://127.0.0.1:5000/priority-queue-evaluation
```

### Example request using PowerShell on Windows

Flask uses port 5000 by default. In that case, you can use this command in Windows PowerShell to test the HTTP server.

```sh
Invoke-WebRequest -Uri "http://127.0.0.1:5000/priority-queue-evaluation" -ContentType "application/json" -Method POST -Body '{"studentPriorityQueue":{"value":3,"left":{"value":4,"left":null,"right":null},"right":{"value":5,"left":null,"right":null}},"providedPriorityQueue":{"value":1,"left":{"value":2,"left":{"value":4,"left":null,"right":null},"right":{"value":5,"left":null,"right":null}},"right":{"value":3,"left":null,"right":null}},"priorityQueueType":"MIN","extractCount":3,"taskType":"PRIORITY_QUEUE_EXTRACT_HIGHEST_PRIORITY"}' 
```

### More requests when using Insomnia

We recommend using Insomnia for easier testing. We have provided requests as a `.yaml` file  in the `checker` directory with more examples. We would highly advise you trying it out. Please consult `03_Insomnia_Installation` with a guide on how to get started with Insomnia.

## Evaluation functions

The evaluation functions for evaluating priority queue exercises are stored in the `evaluation/priority_queue_evaluation` directory. We highly recommend to structure your evaluation directory similar to how we have done so in `02_Example_List_Sorting_Evaluation`.

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

## The PriorityQueueNode Class

The class can be imported using:

```python
from datastructures.priorityqueue import PriorityQueueNode
```

You can find a Python file showcasing the most important functionalities of this class in `checker/example_usage_priority_queue.py`.

Below is an explanation of the most relevant attributes and methods of the `PriorityQueueNode` class. The source code for this class can be found in `checker/datastructures/priorityqueue/_classes/PriorityQueueNode.py` but ideally you should not have to concern yourself with that.

Method/Attribute                       | Datatype(s)                                           | Notes
-------------------------------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
**value** _(setter, getter)_           | `int`                                                 | Value of the node.
**left_child** _(setter, getter)_      | `PriorityQueueNode` or `None`                         | Left child of the node.
**right_child** _(setter, getter)_     | `PriorityQueueNode` or `None`                         | Right child of the node.
**parent** _(setter, getter)_          | `PriorityQueueNode` or `None`                         | Parent of the node.
**==**                                 | accepts `PriorityQueueNode`                           | Compares whether two nodes have the same value. Subtrees are not checked.
**is_equal_including_subtrees(other)** | accepts `PriorityQueueNode`                           | Compares whether two nodes have the same value and balance value. Additionally makes sure, that the entire left and right subtrees are also equal.
**preorder_traverse()**                | returns `list[PriorityQueueNode]`                     | Returns the node and its descendants as a list in the order after preorder traversal.
**inorder_traverse()**                 | returns `list[PriorityQueueNode]`                     | Returns the node and its descendants as a list in the order after inorder traversal.
**postorder_traverse()**               | returns `list[PriorityQueueNode]`                     | Returns the node and its descendants as a list in the order after postorder traversal.
**to_dict()**                          | returns `dict[str, any]`                              | Converts node and subtrees to a dictionary, just like the one in the input.
**print_tree()**                       |                                                       | Prints formatted structure of node and subtrees to STDOUT.
**generate_tree_image(title)**         | optionally accepts `str` or `None`, returns `str`     | Generate a base 64 encoded string containing the priority queue as PNG, which can e.g., be written to a file. Optionally one can provide a string title, which will be included at the top of the image. If it cannot be generated, an exception is raised containing the original error message. The idea behind this method is, that it can be used for debugging.
**display_tree_image(title, img)**     | optionally accepts (`str` or `None`) and `str`        | Generates an image of the priority queue and displays it in an image viewer. One can optionally provide a title to be shown at the top of the image. One can also provide a base64-encoded string containing the image as input. If none is provided, then one is automatically generated. If an image string is provided, the title is ignored, since the generated image will already have a title. If it cannot be generated or displayed, the user is informed. The idea is, that it can be used for debugging.
**deep_copy()**                        | returns `PriorityQueueNode`                           | Creates a deep copy of the node and subtrees. The copy can be modified without affecting the original.
PriorityQueueNode.**from_dict(dict)**  | accepts `dict[str, any]`, returns `PriorityQueueNode` | Class method, which takes a dictionary as input and converts it to a `PriorityQueueNode` with all its subtrees.
