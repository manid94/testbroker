
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
# Function to access or create a file in a sibling directory and write a new value
def write_to_sibling_file(file_name, new_value, sibling_dir_name):
    """
    Writes a new value to a file in a sibling directory. 
    If the file or directory does not exist, it creates them.
    """
    # Get the path of the current script
    current_directory = Path(__file__).parent

    # Go one level up and then to the sibling directory
    sibling_directory = current_directory.parent / sibling_dir_name

    # Create the sibling directory if it doesn't exist
    sibling_directory.mkdir(parents=True, exist_ok=True)

    # Define the file path within the sibling directory
    file_path = sibling_directory / file_name

    # Write the new value to the file, creating or overwriting as necessary
    with open(file_path, 'w') as file:
        file.write(f"{new_value}\n")
    
    print(f"File '{file_name}' written in the sibling directory '{sibling_dir_name}' with new value.")



# Sample data for the API
data = {
    "items": [
        {"id": 1, "name": "item1", "description": "This is item 1"},
        {"id": 2, "name": "item2", "description": "This is item 2"},
        {"id": 3, "name": "item3", "description": "This is item 3"},
    ]
}

# Define a route for the GET request with query parameter






# Sample data
data = {
    "items": [
        {"id": 1, "name": "item1", "description": "This is item 1"},
        {"id": 2, "name": "item2", "description": "This is item 2"},
        {"id": 3, "name": "item3", "description": "This is item 3"}
    ]
}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # Parse query parameters from the URL
        url_parts = urlparse(self.path)
        query_params = parse_qs(url_parts.query)
        name = query_params.get('name', [None])[0]  # Extract the 'name' query parameter
        
        # Set the response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # If 'name' query parameter exists, filter the data
        if name:
            filtered_items = [item for item in data["items"] if item["name"] == name]
            write_to_sibling_file('target_file.txt', str(filtered_items), 'sibling_directory')
            if filtered_items:
                self.wfile.write(json.dumps(filtered_items).encode())
            else:
                # Return 404 if no item is found
                self.send_response(404)
                self.wfile.write(json.dumps({"message": "Item not found"}).encode())
        else:
            # Return all items if no query parameter is provided
            self.wfile.write(json.dumps(data["items"]).encode())

# Set up and start the HTTP server
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
