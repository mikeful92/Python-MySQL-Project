# Card Project -Phase 1

After following the introduction we are ready to start looking at some of the code. We will start with the <code>database.py</code> file. This is part of the final step of setup.

## Set-up

### SQL Tables/Data

We have automated the process of creating the SQL Tables and inserting sample data for them. This will allow us to DROP tables and revert to a clean slate as needed.

Once in the /Phase 1 directory we can run the python scrip with:

```
python3 database.py
```

The command interface will provide information on the success of the execution.

### Breakdown the code

```python
import pymysql
```

We begin by just importing the module needed for the connection to MySQL. It includes everything we will be referencing through out the code.

```python
try:
    cnn = pymysql.connect(
        host="localhost",
        user="root",  # your username
        password='root',
        database="bb_cards")  # name of the data base
    print("It Works!!")
```

Here we are creating an object that will be used as the connection to the database by using the connect() function. The connection function takes a few parameters. The database is local, so the host is "localhost". We will be using the root user, but that could change in the future. The password is based on what you set up at instalation of the MySQL-Server. Last we want it to go directly into using the "bb_cards" database.

```python
cursor = cnn.cursor()
```

While we have created a connection, we need a cursor to actual perform the actions that we desire to the database. As the name implies the cursor acts like the cursor when inputing commands through the command line interface. The cursor will execute queries that are provided as strings.

```python
createStatement = """CREATE TABLE buy_list(
        sport varchar(2) NOT NULL,
        item_desc varchar(50) NOT NULL,
        buy_price int(10) NOT NULL
    ) ENGINE=MyISAM;"""
```

Here we are creating a variable that will hold the query for creation of the first table as a string. This allows us to make changes directly to the variable and re-use the query if necesarry.


```python
cursor.execute(createStatement)
    print("Table created")
```

The cursor has an execute() function that will run our desired query from a string. We do not receive confirmation of the completion so we print directly to the command line.

```python
insertStatement = """INSERT INTO `buy_list` (`sport`, `item_desc`, `buy_price`) VALUES
    ('BB', '1960 Topps Mantle #350 PSA 4', 199),
    ('FB', '1961 Topps Unitas #1 PSA 3', 299),
    ('BK', '1986-1987 Jordan #26 PSA 8', 400),
    ('HK', '1954 Parkhurst Howe #24 PSA 4', 500),
    ('BB', '1983 Topps Wax Case', 2300),
    ('BK', '1989-90 Fleer Wax Case', 300);
    """
```

This is similar to the creation variable, but now we are inserting data into the table. By having this variable we can easily add or delete more items that we would like to have on our starting table.

```python
cursor.execute(insertStatement)
print("Data inserted")
cnn.commit()
print("Changes commited")
```

Here we have another execute function. After we have completed our changes to the database we commit those changes. This is done using the commit() function from the connection object(Not the cursor object).

```python
except pymysql.MySQLError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))

finally:
    if cursor:
        cursor.close()
    if cnn:
        cnn.close()
```

We include some exception handling to catch any errors and finally close the cursor and the connection.

### Check data

We can check on the data we inputed with the following commands:

```
$ mysql -u root -p
mysql>USE bb_cards;
mysql>SELECT * FROM buy_list;
```

This will display the results of the data we have inputed.

## Card Server

### Run server

Now that we have everything set up and ready we can run the server by executing the python script.

```
$ python3 CardServer.py
DB connection established
Starting server...
Running server on localhost:8080...
```

As long as the security group on AWS has been properly set now you can open a browser one your computer and go to [instance ip]:8080 to see the results.

### Breakdown the code

```python
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import pymysql
```

This are the modules that we will need to run the server. 

ThreadinMixIn is a part of the socketserver module that allows for each request that comes to the server to be separated thread. This allows multiple connections to be handled at the same time by the server. Threading is a subject that can be discussed later.

HTTPServer is the module that creates a socket using TCP/HTTP and enables our python script to listen for request.
BaseHTTPRequestHandler is the module that we will use as baseclass for our request handler. It knows how to manage the incoming request, process it and responsd to it.

pymysql was used in the database.py

```python
conn = pymysql.connect(
    host="localhost",
    user="root",  # your username
    password='root',
    database="bb_cards")  # name of the data base
print("DB connection established")
```

We have seen the use of the connect() function to create a connection object. We include this code at the top of the file so that the rest of the code can use this connection as needed.

(We will skip the two classes and jump to the main function)

```python
def main():
    server_address = ''
    port = 8080
    try:
        print("Starting server...")
        server = ThreadedHTTPServer((server_address,port), webServerHandler)
        print("Running server on localhost:{}...".format(port))
        server.serve_forever()
```

Here we are starting the HTTP server. In a non-threaded server we would run the line ```server = HTTPServer((server_address,port), webServerHandler)```. HTTPServer function accepts a tuple of the address we want the server on and the port. It also takes a second parameter which is the custom handler that we design. This custom handler is a class which has the BaseHTTPRequestHandler as its parent. 

In our current version we use ```server = ThreadedHTTPServer((server_address, port), webServerHandler)``` so that each request can be managed as a separate thread. In order to do this we create a shell class that combines the ThreadedMixIn module and the HTTPServer:

```python
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass
```

Finally the ```server.serve_forever()``` just ensures that the connection will be open indefinitely.

```python
except KeyboardInterrupt:
    print("^C received, shutting down server")
    server.socket.close()
```

If we need to shutdown the server we have this exception handler that catches the "ctrl+c" keyboard input and closes the server.

Hyper-text Transfer Protocol(HTTP) can handle various "verbs" or methods of request. The most common methods are GET and POST. Our webServerHandler class will have functions to handle each method that we would like to accept. For this example we only use GET method.

```python
class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            print(self.path)
            if self.path.endswith("/"):  
```

self is the instance of the class and the actual request. The path of that request is the file/directory trying to be reach as part of the URL and after the domain. Since we creating a response for request going to the home directory we use the if statement to check for a path that ends with "/".

```python
    cursor = conn.cursor()
    query = "SELECT item_desc, buy_price FROM buy_list WHERE item_desc LIKE '1988 Fleer Michael Jordan #17 PSA 8%';"
    cursor.execute(query)
    results = cursor.fetchall()
```

This four lines are use to query the desired data from the database. We create a cursor object like we did before. Instead of having an insert query string, we have a SELECT query string. We execute the query and use the cursor's fetchall() function to store the data in the results variable.

```python
    self.send_response(200)
    
    self.send_header('Content-type','text/html')
    self.end_headers()
```

HTTP uses codes to let the browser know that its request has been received and to expect a response. There are various codes, in this example we use the send_response() functiont to send a 200 code with means OK. HTTP also uses headers to inform the browser about what to expect in the response. ```self.send_header('Content-type', 'text/html')``` lets the browser know that we are sending an HTML response. end_headers() lets it know there are no more headers and to expect the response body.

```python
    output = ""
    output += """<!DOCTYPE html>...
```

We will be composing the body of the HTML response as a string. We use the output variable to hold the static portion of the response, which is the head and most of the body. 

```python
    if results:
        output += "<ul>"
        for row in results:
            output += "<li>" + row + "</li>"
            output += "</ul>"
    else:
        output += "<h5>No Matching Inventory...</h5>"
```

We check to see if the results variable from the SQL query has any results. If it does, we preceed to iterate thru the rows in the results and append them as HTML list to the output variable.
If there is no results, we attach a "No Matching Inventory" message to the output string.

```python
    output += "</body></html>"
    self.wfile.write(bytes(output, "utf8"))
    return
```

Finish the HTML string by appending the body and html tag. Then we write to contents of the string to the output stream. Return the function to let the handler know we are done.

```python
except IOError:
    self.send_error(404, 'File Not Found: {}'.format(self.path))
```

Exception handler catches if the path leads to an error. 

## Up next

This script will run a server that can handle HTTP request to the specific port. As we can see when we pull up the page on a browser, it does not server static files such as styles.css or favicon. This will be steps for the next part.


## Resources

http.server module: https://docs.python.org/3/library/http.server.html

BaseHTTPServer: https://pymotw.com/2/BaseHTTPServer/index.html#module-BaseHTTPServer

MultithreadedSimpleHTTPServer: https://github.com/Nakiami/MultithreadedSimpleHTTPServer