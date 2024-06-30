import json
import os
from datetime import datetime
from Habit import Habit  # Import the Habit class from the Habit module

# Custom JSON Encoder for handling datetime objects and Habit objects
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        Override the default method to handle datetime and Habit objects.

        Args:
            obj: The object to encode.

        Returns:
            The JSON-serializable representation of the object.
        """
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()  # Convert Habit objects to dictionary
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime objects to ISO format string
        return json.JSONEncoder.default(self, obj)  # Use default encoding for other types

# Load habits from a JSON file
def load_habits(habits_file: str):
    """
    Loads habits from a specified JSON file.

    Args:
        habits_file (str): The path to the file containing the habits data.

    Returns:
        list: A list of Habit objects.
    """
    if not os.path.exists(habits_file):  # Check if the file exists
        return []
    try:
        with open(habits_file, 'r') as file:
            habits_data = json.load(file)  # Load the JSON data from the file
            # Convert each dictionary in the JSON data to a Habit object
            return [Habit.from_dict(habit_data) for habit_data in habits_data]
    except json.JSONDecodeError:  # Handle JSON decoding errors
        return []

# Save habits to a JSON file
def save_habits(habits: list[Habit], habits_file: str):
    """
    Saves a list of Habit objects to a specified JSON file.

    Args:
        habits (list[Habit]): The list of Habit objects to save.
        habits_file (str): The path to the file where the habits data will be saved.
    """
    try:
        with open(habits_file, 'w') as file:
            try:
                # Convert the list of Habit objects to a list of dictionaries
                habits_dict_list = [habit.to_dict() for habit in habits]

                # Serialize the list of dictionaries to JSON with indentation for readability
                json_data = json.dumps(habits_dict_list, indent=4)

                # Write the JSON data to the file
                file.write(json_data)
            except IOError:  # Handle file I/O errors
                print("Error: File is busy.")
    except Exception as e:  # Catch all other exceptions
        print(f"An error occurred: {e}")
