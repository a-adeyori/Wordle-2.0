import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logic #import module for game logic

class GameServer(BaseHTTPRequestHandler):
    """Custom HTTP server class to handle game-related requests."""

    def _send_response(self, response_data):
        """Helper function to send JSON response back to client."""
        self.send_response(200) # Set HTTP status code to 200 (OK).
        self.send_header('Content-type', 'application/json') # Specify response content as JSON.
        self.end_headers() #signals end of HTTP end_headers
        #write the json-encoded response data to the output stream
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    
    def do_GET(self):
        """handle GET requests to retrieve hints, scores, or start agame."""
        #Check if the path is request for a hint, e.g., /hint?word=smile
        if self.path.startswith('/hint'):
            try:
                #Extract thw word from the query starting
                word=self.path.split("=")[1]
                #call the get_hint function fro logic with the specified word
                response = logic.get_hint(word)
                self._send_response(response)
            except IndexError:
            #send an error response if thw word is missing
                self._send_response({"error": "Invalid request, missing word parameter"})


            #check if the path is a request to request for a score, e.g, /score
            try: 
                #Extract the username from the query string 
                username=self.path.split('=')[1]
                    #call the get_score function from logi with the specified username
                response=logic.get_scores(username)
                self._send_response(response)
            except IndexError:
                #send an error response if thw word is missing
                self._send_response({"error": "Invalid request, missing word parameter"})

        elif self.path == '/start':
            # Call the start_game function from endpoints to retrieve a new random word
            response = logic.main()
            self._send_response(response)
        else:
            # Send an error response for unrecognized endpoints
            self._send_response({"error": "Invalid endpoint"})
    
    def do_POST(self):
        """Handle POST requests to update scores."""
        # Check if the path is for updating a score, e.g., /update_score
        if self.path == '/update_score':
            # Get the length of the request body content
            content_length = int(self.headers['Content-Length'])
            # Read the body of the request
            post_data = self.rfile.read(content_length)
            # Parse the request body as JSON
            data = json.loads(post_data.decode('utf-8'))
            # Extract the username and score from the JSON data
            username = data.get("username")
            score = data.get("score")

            # Check if both username and score are provided
            if username is None or score is None:
                # Send an error response if any required parameter is missing
                self._send_response({"error": "Missing username or score in request"})
            else:
                # Call the update_score function from endpoints and send the result
                response = logic.update_score(username, score)
                self._send_response(response)
        
        else:
            # Send an error response for unrecognized endpoints
            self._send_response({"error": "Invalid endpoint"})

def run(server_class=HTTPServer, handler_class=GameServer, port=8080):
        """Initialize and run the HTTP server on the specified port."""
        server_address = ('', port)  # Listen on all available IP addresses.
        httpd = server_class(server_address, handler_class)  # Create the server instance.
        print(f"Starting server on port {port}")  # Log server startup to console.
        httpd.serve_forever()  # Keep the server running indefinitely.

    # If the script is run directly (not imported), start the server
if __name__ == '__main__':
        run()


























