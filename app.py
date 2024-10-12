from flask import Flask, request, jsonify
import os
from pathlib import Path

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

# Initialize Flask app
app = Flask(__name__)

# Sample data for the API
data = {
    "items": [
        {"id": 1, "name": "item1", "description": "This is item 1"},
        {"id": 2, "name": "item2", "description": "This is item 2"},
        {"id": 3, "name": "item3", "description": "This is item 3"},
    ]
}

# Define a route for the GET request with query parameter
@app.route('/api/items', methods=['GET'])
def get_items():
    """
    GET endpoint to retrieve items. Filters by name query parameter if provided.
    """
    # Get the 'name' query parameter from the request
    name = request.args.get('name')
    
    # If 'name' is provided, filter the data
    if name:
        filtered_items = [item for item in data["items"] if item["name"] == name]
        if filtered_items:
            write_to_sibling_file('target_file.txt', jsonify(filtered_items).get_data(as_text=True), 'sibling_directory')
            return jsonify(filtered_items), 200
        else:
            return jsonify({"message": "Item not found"}), 404
    
    # If no query parameter is provided, return all items
    return jsonify(data["items"]), 200

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
