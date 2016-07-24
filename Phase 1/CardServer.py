from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import pymysql

#Create connection object to connect to MySQL DB
conn = pymysql.connect(
    host="localhost",
    user="root",  # your username
    password='root',
    database="bb_cards")  # name of the data base
print("DB connection established")

#HTTPRequestHandler class
class webServerHandler(BaseHTTPRequestHandler):
    #Handle GET Method request
    def do_GET(self):
        try:
            print(self.path)
            # Match the request path to "/" or home page
            if self.path.endswith("/"):

                cursor = conn.cursor()
                # Select all Fleer Michael Jordan cards
                query = "SELECT item_desc, buy_price FROM buy_list WHERE item_desc LIKE '1988 Fleer Michael Jordan #17 PSA 8%';"
                cursor.execute(query)
                results = cursor.fetchall()

                #Send response status code
                self.send_response(200)
                
                #Send headers
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""

                #Compose HTML response in a string
                output += """<!DOCTYPE html>
<html>
<head>
<title>We&rsquo;re Buying</title>
<link rel="stylesheet" href="style.css">
<style>
p {
    text-indent: 650px;
}
</style>
</head>
<body>
<h1>Boca Cards</h1>
<h2>We&rsquo;re Buying</h2>
<p>PSA Graded Cards</p>
<p>Beckett Graded Cards</p>
<p>Ungraded Cards</p>
<h4>For large deals, we&rsquo;ll come to you</h4>
<div style="background-color:white;padding:20px;">
<h5>Contact us at: bocacards@gmail.com</h5>
<h5>Dealing in sports cards since 1991</h5>
</div>
<h3>Boca Cards: Over 25 years in business helping collectors buy and sell</h3>
"""
                # If query returns results append to output as a list
                if results:
                    output += "<ul>"
                    for row in results:
                        output += "<li>" + row + "</li>"
                    output += "</ul>"
                # If not results, append a message notifying that there is no matching inventory
                else:
                    output += "<h5>No Matching Inventory...</h5>"
                output += "</body></html>"
                #Write contents of the string to the output stream
                self.wfile.write(bytes(output, "utf8"))
                return
        except IOError:
            self.send_error(404, 'File Not Found: {}'.format(self.path))

# Filler class to allow each request to be handled by a separate thread
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def main():
    # '' means that the localhost will be assign as the address
    server_address = ''
    # Use port 8080 for testing
    port = 8080
    try:
        print("Starting server...")
        # Create a server object with the ThreadedHTTPServer class and the custom handler created above
        server = ThreadedHTTPServer((server_address,port), webServerHandler)
        print("Running server on localhost:{}...".format(port))
        # Set the server to run indefinitely
        server.serve_forever()
    except KeyboardInterrupt:
        # Close server if "ctrl+C" keyboard signal is sent
        print("^C received, shutting down server")
        server.socket.close()
        
if __name__ == '__main__':
    main()