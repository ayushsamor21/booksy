# SampleAPIHandler

A simple Python-based REST API using `http.server` running at `http://localhost:8002`. This project demonstrates how to handle HTTP requests (`GET`, `POST`, `PUT`, `DELETE`) with a custom request handler.

---

##  Getting Started

### Installation & Running the Server

1. Clone the repository (or download the script):
   ```bash
   git clone https://github.com/ayushsamor21/booksy.git
   cd booksy/restful_api

2. Run server:
    ```bash
    python3 sampleApiHandler.py

---

##  API Usage with curl

### GET request
1. GET method (Retrieve data from server):
    ```bash
    curl -X GET http://localhost:8002

### POST request
1. POST method (Create new resource):
    ```bash
    curl -X POST http://localhost:8002 \
     -H "Content-Type: application/json" \
     -d '{"name": "John", "age": 30}'

### PUT request
1. PUT method (update new resource):
    ```bash
     curl -X PUT http://localhost:8002 \
     -H "Content-Type: application/json" \
     -d '{"name": "John", "age": 31}'
   
### DELETE request
1. DELETE method (delete new resource):
    ```bash
   curl -X DELETE http://localhost:8002
    
