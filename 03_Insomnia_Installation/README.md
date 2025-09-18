# Using Insomnia to Test Your Flask Server

So far, we have tested our Flask server using `cURL` or `Windows PowerShell` in the command line. This helped us learn the basics of how HTTP requests work. However, typing long commands and escaping quotes for JSON bodies can get a little tricky and time-consuming.  
This is where **Insomnia** comes in: it is a graphical REST client that makes sending requests and analyzing responses much easier.

## Insomnia Overview
[Insomnia](https://insomnia.rest/) is a lightweight tool for testing and debugging APIs.  
It provides a simple interface for sending requests to your Flask server and viewing responses in a structured way. You can think of it as a "GUI for cURL".

### Advantages over cURL
- **No complicated command syntax** – Fill out request fields instead of writing long commands.  
- **Automatic JSON formatting** – Request bodies and responses are displayed clearly.  
- **History and collections** – Save your requests in a workspace and reuse them later.  
- **Environment variables** – Store things like your base URL (`http://127.0.0.1:5000`) so you don’t have to type them every time.  
- **Visual debugging** – Responses are formatted and easy to read, with clear status codes and headers.

---

## Installing Insomnia
You can download Insomnia for your operating system from the official website:  
[https://insomnia.rest/download](https://insomnia.rest/download)

Once installed, open it and create a new **Collection** to organize your requests for the Flask exercises.

---

## Sending a Request in Insomnia
If your Flask server is running locally on port 5000, you can test it with the same request we already tried with `cURL` which you will now create in Insomnia. If the following instructions aren't enough, you can look up this guide: [Insomnia Guide](https://docs.insomnia.rest/insomnia/send-your-first-request)

### Step 1 – Create a new request
1. Click **New Request**.  
2. Name it e.g., `Example List Sort`.  
3. Choose **POST** as the request method.  
4. Enter the URL: http://127.0.0.1:5000/example-list-evaluation

### Step 2 – Add the request body
Switch to the **Body** tab, select **JSON**, and paste in the following example body:
```json
{
    "providedList": [1, 3, 2, 7, 9, 0],
    "studentList": [0, 1, 3, 2, 7, 9],
    "taskType": "EXAMPLE_LIST_SORT_ASCENDING"
}
```

### Alternative: Import requests from a `.yaml` file
Instead of creating requests manually, you can also import predefined requests into Insomnia.  
A `requests.yaml` file is provided in the same directory as this README for the Example List Sort Evaluation program.  

To import it:  
1. Open the main menu in Insomnia.  
2. Go to **Import/Export** → **Import Data**.  
3. Select **From File**.  
4. Choose the `requests.yaml` file located in the same directory as this README.  

After importing, all example requests will appear in your workspace, organized into two folders:  
- One folder contains requests for testing the **ascending list sorting** evaluation.  
- The other folder contains requests for testing the **descending list sorting** evaluation.  

Each folder includes five requests. In each set, one request is correct, while the other four contain small mistakes in the `studentList` submission. When you send these requests, the microservice will evaluate them, provide a score, and return detailed feedback based on the errors.


## Final Words

Using **Insomnia** is highly recommended when working with your Flask server. While `cURL` is great for learning the basics of HTTP requests, Insomnia makes the process of testing, debugging, and experimenting much easier and more efficient.  

I personally use Insomnia extensively when developing and testing HTTP servers, especially when implementing other evaluation services. The ability to **store requests, organize them in collections, and quickly create new variations** is invaluable for systematic testing and rapid development.  

Mastering this tool will save you a lot of time and effort, not only for these exercises but for any project involving APIs or HTTP servers.
