# Evaluator Microservice for List sorting

The goal of this example is to show you a Python microservice, which provides detailed feedback to students solving list sorting exercises. In this example the student gets a list of numbers and the way they should be sorted, so ascending or descending. After the student solved the exercise, a request is send to the evaluator microservice checking whether the student solve the exercise correctly.
All the HTTP POST requests for the list sorting topic are send to one endpoint. This endpoint checks which task type should be evaluated based on the string contained in the request and forwards the task to the according function. Each of the two tasks which can be evaluated in this microservice, sorting ascending and sorting descending, has a task type.
The HTTP POST requests body contains all the information about the task as well as the student's submission needed to evaluate the task. Based on the task, so the provided tree which should be sorted and the students submission, a solution, a grade and detailed feedback is created and send back as a JSON response.

### Send request to server
If the server runs you can send a request to the given server by e.g., using command line tools like CURL or other API tools like Postman/Insomnia. We will be talking later on about Postman/Insomnia.
You will have to perform a post request on the endpoint and pass the contents as a JSON body.

#### Example body:
You can just use this JSON bodys as an example.

A task where the student is asked to sort a proviedList ascending:
```json
{
    "providedList": [1,3,2,7,9,0],
    "studentList": [0,1,3,2,7,9],
    "taskType": "EXAMPLE_LIST_SORT_ASCENDING"
}
```

A task where the student is asked to sort a proviedList descending:
```json
{
    "providedList": [1,3,2,7,9,0],
    "studentList": [9,7,2,3,1,0],
    "taskType": "EXAMPLE_LIST_SORT_DESCENDING"
}
```

#### Example request using cURL
Assuming Flask uses the default port 5000, you can use this cURL command to test the HTTP server.
```sh
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"providedList":[1,3,2,7,9,0],"studentList":[0,1,3,2,7,9],"taskType":"EXAMPLE_LIST_SORT_ASCENDING"}' http://127.0.0.1:5000/example-list-evaluation
```

#### Example request using PowerShell on Windows
Assuming Flask uses the default port 5000, you can use this command in Windows PowerShell to test the HTTP server.
```sh
Invoke-WebRequest -Uri "http://127.0.0.1:5000/example-list-evaluation" -ContentType "application/json" -Method POST -Body '{"providedList":[1,3,2,7,9,0],"studentList":[0,1,3,2,7,9],"taskType":"EXAMPLE_LIST_SORT_ASCENDING"}'
```

## HTTP Routing

The `app.py` file serves as the main entry point for handling requests in the Flask application. It defines the available endpoints, processes incoming data, and returns a response. There, the evaluation logic is started by calling a function.

### Request

Each route requires the following JSON input:
- The **studentList** (the submitted solution, **mandatory**).
- The **providedList** (initial list, **mandatory**).

Inside the route's function, the task is programmatically solved using the **ExampleList** class. The student's submission is then evaluated against the expected solution, and feedback with an appropriate score is returned.

The request has the following JSON format:
```json
{
    "providedList": ...,
    "studentList": ...,
    "taskType": ...
}
```

As an example, the endpoint `/example-list-evaluation` in `app.py` was defined. This route does the following:
- Accepts input
- Converts the **lists** from JSON to objects using `ExampleList`.
- Does grading, creates feedback and a solution.
- Returns the score, feedback and solution.

### Evaluation functions
The evaluation functions for evaluating the list sorting exercises are stored in the `evaluation/example_evaluation` directory. The `evaluation/example_evaluation/evaluation_endpoint.py` decides based on the task type contained in the HTTP POST request which evaluation function, so for ascending or descending list sorting exercise, should be used. The real evaluation then takes placed based on the task type in `evaluation\example_evaluation\list_evaluation_ascending\example_list_ascending_sorting_evaluation.py` or `evaluation\example_evaluation\list_evaluation_descending\example_list_descending_sorting_evaluation.py`.


### Response

The response has an HTTP status code of 200 (OK). The response includes:
- **score** (from 0 to 100)
- **feedback** as text
- **solution** the correct solution list as JSON

The response has the following JSON format:
```json
{
    "score": ...,
    "feedback": ...,
    "solution": ...
}
```

## Example JSON requests/responses
### Example request for sorting a list ascending
This could be an example list where the task is to sort the list ascending.
In this example the student has correctly sorted the list ascending.
*In this example, the student submission is correct.*
#### Request
```json
{
    "providedList": [1, 3, 2,7,9,0],
    "studentList": [0,1,2,3,7,9],
    "taskType": "EXAMPLE_LIST_SORT_ASCENDING"
}
```

#### Response
```json
{
	"feedback": "Correct!",
	"score": 100,
	"solution": [0,1,2,3,7,9]
}
```

### Example request for sorting a list ascending
This could be an example list where the task is to sort the list ascending.
In this example the student has accidentally sorted the list descending instead of ascending.
*In this example, the student submission is incorrect.*
#### Request
```json
{
    "providedList": [1, 3, 2,7,9,0],
    "studentList": [0,1,2,3,7,9],
    "taskType": "EXAMPLE_LIST_SORT_ASCENDING"
}
```

#### Response
```json
{
	"feedback": "The list was sorted descending not ascending.",
	"score": 50,
	"solution": [0,1,2,3,7,9]
}
```