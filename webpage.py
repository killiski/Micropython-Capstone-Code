import socket
import json
import os
import time
import _thread
import asyncio


# Global set to track function calls
active_functions = set()



def track_function(func):
    def wrapper(*args, **kwargs):
        # Add the function name to the active set
        active_functions.add(func.__name__)
        print(f"Entering {func.__name__}")

        try:
            return func(*args, **kwargs)
        finally:
            # Remove the function name from the active set
            active_functions.remove(func.__name__)
            print(f"Exiting {func.__name__}")

    return wrapper

    
"""
def track_function(func):
    def wrapper(*args, **kwargs):
        # Add the function name to the active set
        active_functions.add(func.__name__)
        print(f"Entering {func.__name__}")

        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")  # Log any exceptions that occur
            raise  # Re-raise the exception after logging
        finally:
            # Remove the function name from the active set
            active_functions.remove(func.__name__)
            print(f"Exiting {func.__name__}")

    return wrapper
"""

def is_function_in_stack(func_name):
    func_name = "web_server"
    return func_name in active_functions


# Load data from JSON file
def load_data():
    if 'data.json' in os.listdir():
        with open('data.json', 'r') as f:
            return json.load(f)
    else:
        return {"value1": 0, "value2": 0}

# Save data to JSON file
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)


# Handle HTTP requests => we need to put this into a thread
@track_function
def web_server():
    data = load_data()

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][4]
    s = socket.socket()
    
    
    s.bind(addr)
    s.listen(3)
    # s.settimeout(5)
    print("Listening on", addr)
    

    while True:
        cl, addr = s.accept()
        try:
            print('Client connected from', addr)
            
            
            requestRaw = cl.recv(1024)
            #print(requestRaw)
            request = requestRaw.decode()

            
            if '/update' in request:
                # Parse the incoming data
                #print(request)
                data_str = request.split('\r\n\r\n')[1].split('\r\n')[0]
                #print(data_str)
                value1 = int(data_str.split('&')[0].split('=')[1])
                value2 = int(data_str.split('&')[1].split('=')[1])
                data['value1'] = value1
                data['value2'] = value2
                save_data(data)
                response = json.dumps(data)
            elif '/values' in request:
                response = json.dumps(data)
                #print(f"\n\n---------\n\n{response}\n\n---------\n\n")
            else:
                response = html()

            #print(f"\n\n---------\n\n{response}\n\n---------\n\n")
            cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
        except Exception as e:
            print("Error:", e)
            cl.close()  # Ensure the client socket is closed in case of an error






def html():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 Web Server</title>
    <style>
        table {
            position: relative;
            width:100%;
            border-spacing: 0px;
        }
        tr {
            border: 1px solid white;
            font-family: "Verdana", "Arial", sans-serif;
            font-size: 20px;
        }
        th {
            height: 20px;
            padding: 3px 15px;
            background-color: #343a40;
            color: #FFFFFF !important;
        }
        td {
            height: 20px;
            padding: 3px 15px;
        }
        .tabledata {
            font-size: 24px;
            position: relative;
            padding-left: 5px;
            padding-top: 5px;
            height:   25px;
            border-radius: 5px;
            color: #FFFFFF;
            line-height: 20px;
            transition: all 200ms ease-in-out;
            background-color: #00AA00;
        }
        .fanrpmslider {
            width: 30%;
            height: 55px;
            outline: none;
            height: 25px;
        }
        .bodytext {
            font-family: "Verdana", "Arial", sans-serif;
            font-size: 24px;
            text-align: left;
            font-weight: light;
            border-radius: 5px;
            display:inline;
        }
        .navbar {
            width: 100%;
            height: 50px;
            margin: 0;
            padding: 10px 0px;
            background-color: #FFF;
            color: #000000;
            border-bottom: 5px solid #293578;
        }
        .fixed-top {
            position: fixed;
            top: 0;
            right: 0;
            left: 0;
            z-index: 1030;
        }
        .navtitle {
            float: left;
            height: 50px;
            font-family: "Verdana", "Arial", sans-serif;
            font-size: 50px;
            font-weight: bold;
            line-height: 50px;
            padding-left: 20px;
            }
        .navheading {
            position: fixed;
            left: 60%;
            height: 50px;
            font-family: "Verdana", "Arial", sans-serif;
            font-size: 20px;
            font-weight: bold;
            line-height: 20px;
            padding-right: 20px;
        }
        .navdata {
            justify-content: flex-end;
            position: fixed;
            left: 70%;
            height: 50px;
            font-family: "Verdana", "Arial", sans-serif;
            font-size: 20px;
            font-weight: bold;
            line-height: 20px;
            padding-right: 20px;
        }
        .category {
            font-family: "Verdana", "Arial", sans-serif;
            font-weight: bold;
            font-size: 32px;
            line-height: 50px;
            padding: 20px 10px 0px 10px;
            color: #000000;
        }
        .heading {
            font-family: "Verdana", "Arial", sans-serif;
            font-weight: normal;
            font-size: 28px;
            text-align: left;
        }
        
        .btn {
            background-color: #444444;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        .foot {
            font-family: "Verdana", "Arial", sans-serif;
            font-size: 20px;
            position: relative;
            height:   30px;
            text-align: center;   
            color: #AAAAAA;
            line-height: 20px;
        }
        .container {
            max-width: 1800px;
            margin: 0 auto;
        }
        table tr:first-child th:first-child {
            border-top-left-radius: 5px;
        }
        table tr:first-child th:last-child {
            border-top-right-radius: 5px;
        }
        table tr:last-child td:first-child {
            border-bottom-left-radius: 5px;
        }
        table tr:last-child td:last-child {
            border-bottom-right-radius: 5px;
        }
    </style>
    <script>
        function updateValues() {
            const value1 = document.getElementById("value1").value;
            const value2 = document.getElementById("value2").value;
            console.log(value1) //debugging line
            console.log(value2) //debugging line
            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/update", true);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    document.getElementById("displayValue1").innerText = response.value1;
                    document.getElementById("displayValue2").innerText = response.value2;
                }
            };
            xhr.send(`value1=${value1}&value2=${value2}`);
        }

        function fetchValues() {
            const xhr = new XMLHttpRequest();
            xhr.open("GET", "/values", true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    document.getElementById("displayValue1").innerText = response.value1;
                    document.getElementById("displayValue2").innerText = response.value2;
                }
            };
            xhr.send();
        }

        setInterval(fetchValues, 5000);
    </script>
</head>
<body>
    <h1>Store Integer Values</h1>
    <label for="value1">Value 1:</label>
    <input type="range" id="value1" min="0" max="100" step="1" oninput="this.nextElementSibling.value = this.value">
    <output>50</output><br>
    
    <label for="value2">Value 2:</label>
    <input type="range" id="value2" min="0" max="100" step="1" oninput="this.nextElementSibling.value = this.value">
    <output>50</output><br>
    
    <button onclick="updateValues()">Submit</button>
    <h2>Stored Values:</h2>
    <p>Value 1: <span id="displayValue1">0</span></p>
    <p>Value 2: <span id="displayValue2">0</span></p>
</body>
</html>'''




def monitor_webserver():
    # func_name = web_server
    time.sleep(10)
    print(f"{active_functions} so {"web_server" in active_functions}")

    #  print(web_server in active_functions)
    # time.sleep(10)
    

    

def webpage_deploy():
    #web_server()
    
    #_thread.start_new_thread(web_server, ())
    time.sleep(10)
    
    while True:
        print("deploying server")
        web_server()
    
    
    """
    while True:
        print(active_functions)
        print("web_server" not in active_functions)
        if "web_server" not in active_functions:
            print("deploying server")
            web_server()
        
        time.sleep(5) # while the code is small and not reading IO add in this delay
    """


#webpage_deploy() # comment out if you get stuck