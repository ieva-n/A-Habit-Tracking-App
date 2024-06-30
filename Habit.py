from datetime import datetime

class Habit:
    def __init__(self, name: str, description: str, frequency: str):
        """
        Initializes a new habit with the given name, description, and frequency.
        
        Args:
            name (str): The name of the habit.
            description (str): A brief description of the habit.
            frequency (str): The frequency of the habit, e.g., 'DAILY' or 'WEEKLY'.
        """
        self.name = name
        self.description = description
        self.frequency = frequency 
        self.created = datetime.today()  # The date and time when the habit was created
        self.marked_dates = []  # List to store dates when the habit is marked as complete
        self.longest_streak = 0  # Placeholder for the longest streak of habit completion

    def mark_complete(self):
        """
        Marks the habit as complete for the current date. If the current date is not already in the marked_dates list, it adds it.
        """
        current_date = datetime.today()  # Get the current date and time
        # Check if the current date is not already marked as complete
        if current_date.date() not in [date.date() for date in self.marked_dates]:
            self.marked_dates.append(current_date)  # Add the current date to marked_dates

    def is_completed_in_this_period(self, current_date):
        """
        Checks if the habit has been completed in the current period based on its frequency.

        Args:
            current_date (datetime): The date to check for completion.

        Returns:
            bool: True if the habit is completed in the current period, False otherwise.
        """
        if self.frequency == "DAILY":
            # Check if the habit is marked complete for the current day
            if current_date.date() in [date.date() for date in self.marked_dates]:
                return True
            
        elif self.frequency == "WEEKLY":
            # Get the current calendar week
            current_calendar_week = current_date.isocalendar()[1]
            # Check if the habit is marked complete for the current week
            if len(self.marked_dates) > 0:  # Ensure there are marked dates
                for i in range(len(self.marked_dates)-1, -1, -1):
                    last_completed_week = self.marked_dates[i].isocalendar()[1]
                    if current_calendar_week == last_completed_week:
                        return True
        return False

    def print_out(self):
        """
        Prints the details of the habit, including name, description, frequency, and creation date.
        """
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Frequency: {self.frequency}")
        print(f"Created: {self.created.strftime('%Y-%m-%d %H:%M:%S')}")

    def to_dict(self):
        """
        Converts the habit object to a dictionary.

        Returns:
            dict: A dictionary representation of the habit.
        """
        return {
            'name': self.name,
            'description': self.description,
            'frequency': self.frequency,
            'created': self.created.isoformat(),  # Convert datetime to string
            'marked_dates': [date.isoformat() for date in self.marked_dates]  # Convert list of datetimes to strings
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a habit object from a dictionary.

        Args:
            data (dict): A dictionary containing habit data.

        Returns:
            Habit: A habit object created from the dictionary data.
        """
        habit = cls(data['name'], data['description'], data['frequency'])
        habit.created = datetime.fromisoformat(data['created'])  # Convert string to datetime
        habit.marked_dates = [datetime.fromisoformat(date) for date in data['marked_dates']]  # Convert list of strings to datetimes
        return habit
