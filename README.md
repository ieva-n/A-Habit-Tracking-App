# Habit Tracking App

The Habit Tracking App is designed to help users manage and track their daily and weekly habits. Users can mark habits as complete, monitor streaks, and view statistics about their habits.

## Features

- **Create and manage habits:** Define habits with a name, description, and frequency (daily or weekly).
- **Mark habits as complete:** Track your progress by marking habits as complete.
- **View habit statistics:** Get insights on your longest streaks and overall progress.
- **Save and load habits:** Persist your habit data between sessions using JSON files.

## Project Structure

- `main.py`: Handles the CLI interface with the user.
- `Habit.py`: Contains the `Habit` class to define and manage individual habits.
- `analytics.py`: Provides functions to filter habits, count streaks and analyze habit performance.
- `storage.py`: Handles loading and saving habits from and to JSON files.
- `habits.json`: A data file containing the stored habits.
- `test_habit.py`: Unit tests for `Habit.py`.
- `test_analytics.py`: Unit tests for `analytics.py`.
- `test_habits.json`: Sample data file containing predefined habits for testing.

## Getting Started

### Prerequisites

- Python 3.7 or higher

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/habit-tracking-app.git
    cd habit-tracking-app
    ```

### Usage

1. Define your habits by creating instances of the `Habit` class.
2. Use the functions in `analytics.py` to filter and analyze your habits.
3. Save and load habits using the functions in `storage.py`.

### Example

Here's a basic example of how to create and manage a habit:

```python
from Habit import Habit
from storage import save_habits, load_habits

# Create a new habit
exercise = Habit("Exercise", "Daily exercise", "DAILY")

# Mark the habit as complete
exercise.mark_complete()

# Save the habit
save_habits([exercise])

# Load habits
habits = load_habits()
for habit in habits:
    habit.print_out()
```
### Running the Tests

Unit tests are provided to ensure the functionality of the application. The tests cover the Habit class, analytics functions, and storage functions.

To run the tests, use the following command:

```sh
python -m unittest discover tests
```
### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue to discuss any changes or improvements.
