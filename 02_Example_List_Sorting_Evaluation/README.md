# Evaluator Microservice For List Sorting

The goal of this example is to show you a Python microservice, which provides detailed feedback to students solving list sorting exercises. In this example the student gets a list of numbers and the way they should be sorted, so in ascending order or descending order. After the student submits the exercise, a request is sent to the evaluator microservice checking whether the student solved the exercise correctly.
All the HTTP POST requests for the list sorting topic are sent to the endpoint `/example-list-evaluation`. This endpoint checks which task type should be evaluated based on the `taskType` string contained in the request and forwards the task to the according function. Each of the two tasks which can be evaluated in this microservice, sorting in ascending order and sorting in descending order, has a task type.
The HTTP POST request's body contains all the information about the task as well as the student's submission needed to evaluate the task. So, the route receives the provided list and the student's submission and responds back with a grade from 0 to 100, detailed feedback as text and the solution.

## Flask Server
For evaluating each task, a HTTP POST request will be sent to the microservice, a web server hosted via flask.

### HTTP Routing

The `checker/app.py` file serves as the main entry point for handling requests in the Flask application. It defines the available endpoints, processes incoming data, and returns a response. There, the evaluation logic is started by calling a function.

### Request

The route requires the following JSON input:
- The **studentList** (the student's submission, **mandatory**).
- The **providedList** (initial list, **mandatory**).
- The **taskType** (the task type ("**EXAMPLE_LIST_SORT_ASCENDING**" or "**EXAMPLE_LIST_SORT_DESCENDING**"), **mandatory**).

Inside the route's function, the task is programmatically solved using the **ExampleList** class. The student's submission is then compared to the expected solution, and feedback with an appropriate score is returned.

The request has the following JSON format:
```json
{
    "providedList": ...,
    "studentList": ...,
    "taskType": ...
}
```

### Start server

You can use Flask to start the HTTP server. We recommend running in debug mode, because this way the server automatically restarts when the code changes, so that you do not have to restart the server manually.
To start the HTTP server run the following command in the command line. Your working directory needs to be the directory containing `app.py`:
> flask run --debug

If the `flask` command cannot be located correctly, then you can also try:
> python -m flask run --debug

Upon success, an HTTP server starts on localhost. You can terminate it using CTRL+C in the terminal.

Since Flask usually takes localhost port 5000, you will probably find your HTTP server there. Alternatively, look for the address in the terminal output. Usually it will look like this:
> * Running on http://127.0.0.1:5000

### Send request to server
If the server runs you can send a request to the given server by e.g., using command line tools like cURL or other API tools like Postman/Insomnia. We will be talking later about Postman/Insomnia.
You will have to send a POST request to the endpoint and pass the contents as a JSON body.

#### Example body:
You can just use this JSON body as an example.

A task where the student is asked to sort a provided list in ascending order:
```json
{
    "providedList": [1, 3, 2, 7, 9, 0],
    "studentList": [0, 1, 3, 2, 7, 9],
    "taskType": "EXAMPLE_LIST_SORT_ASCENDING"
}
```

A task where the student is asked to sort a provided list in descending order:
```json
{
    "providedList": [1, 3, 2, 7, 9, 0],
    "studentList": [9, 7, 2, 3, 1, 0],
    "taskType": "EXAMPLE_LIST_SORT_DESCENDING"
}
```

#### Example request using cURL
Flask uses port 5000 by default. In that case, you can use this cURL command to test the HTTP server.
```sh
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"providedList":[1,3,2,7,9,0],"studentList":[0,1,3,2,7,9],"taskType":"EXAMPLE_LIST_SORT_ASCENDING"}' http://127.0.0.1:5000/example-list-evaluation
```

#### Example request using PowerShell on Windows
Flask uses port 5000 by default. In that case, you can use this command in Windows PowerShell to test the HTTP server.
```sh
Invoke-WebRequest -Uri "http://127.0.0.1:5000/example-list-evaluation" -ContentType "application/json" -Method POST -Body '{"providedList":[1,3,2,7,9,0],"studentList":[0,1,3,2,7,9],"taskType":"EXAMPLE_LIST_SORT_ASCENDING"}'
```

### Evaluation functions
The evaluation functions for evaluating the list sorting exercises are stored in the `evaluation/example_evaluation` directory. The `evaluation/example_evaluation/evaluation_endpoint.py` decides based on the task type contained in the HTTP POST request which evaluation function, i.e. the one for ascending or descending list sorting exercise, should be used. The real evaluation then takes placed based on the task type in `evaluation/example_evaluation/list_evaluation_ascending/example_list_ascending_sorting_evaluation.py` or `evaluation/example_evaluation/list_evaluation_descending/example_list_descending_sorting_evaluation.py`.

Since both task types make use of similar or even the same functions (i.e., handling missing values), there is also a directory `evaluation/example_evaluation/example_evaluation_utilities` which contains functions, which both task evaluations can make use of.

That practice would be good for keeping it structured, but you do not have to strictly follow that approach.

### Response

The response has an HTTP status code of 200 (OK). The response includes:
- **score** (from 0 to 100)
- **feedback** as text
- **solution** the correct solution list

The response has the following JSON format:
```json
{
    "score": ...,
    "feedback": ...,
    "solution": ...
}
```

## Example JSON requests/responses
### Example request for sorting a list correctly in ascending order
This could be an example list where the task is to sort the list in ascending order.
In this example the student has correctly sorted the list in ascending order.
*In this example, the student submission is correct.*
#### Request
```json
{
    "providedList": [1, 3, 2, 7, 9, 0],
    "studentList": [0, 1, 2, 3, 7, 9],
    "taskType": "EXAMPLE_LIST_SORT_ASCENDING"
}
```

#### Response
```json
{
	"feedback": "Correct.",
	"score": 100,
	"solution": [0, 1, 2, 3, 7, 9]
}
```

### Example request for sorting a list in descending order instead of ascending order
This could be an example where the task is to sort the list in ascending order.
In this example the student has accidentally sorted the list in descending order instead of ascending order.
*In this example, the student submission is incorrect.*
#### Request
```json
{
    "providedList": [1, 3, 2, 7, 9, 0],
    "studentList": [9, 7, 3, 2, 1, 0],
    "taskType": "EXAMPLE_LIST_SORT_ASCENDING"
}
```

#### Response
```json
{
	"feedback": "You were supposed to sort in ascending order but sorted in descending order instead.",
	"score": 45,
	"solution": [0, 1, 2, 3, 7, 9]
}
```

### Example request for not correctly sorting a list in descending order, leaving out values and having extra values
This could be an example where the student makes mistakes when sorting, forgot certain values and added additional values, which were not asked for.
*In this example, the student submission is incorrect.*
#### Request
```json
{
    "providedList": [1, 3, 2, 7, 9, 0],
    "studentList": [3, 1, 8, 7, 0, 2],
    "taskType": "EXAMPLE_LIST_SORT_DESCENDING"
}
```

#### Response
```json
{
	"feedback": "The list is not correctly sorted in ascending order. The value 3 is not allowed to be before 1. The value 7 is not allowed to be before 0. The following values are present less often than expected: [9].",
	"score": 0,
	"solution": [0, 1, 2, 3, 7, 9]
}
```
