from Habit import Habit
from datetime import datetime, timedelta
from storage import load_habits, save_habits


def filter_habits_unchecked(habits: list[Habit]):
    """
    Filters out habits that have not been completed in the current period.

    Args:
        habits (list[Habit]): List of Habit objects.

    Returns:
        list: Indices of habits that are not completed in the current period.
    """
    habit_indices = []
    current_date = datetime.today()
    for i, habit in enumerate(habits):
        if not habit.is_completed_in_this_period(current_date):
            habit_indices.append(i)

    return habit_indices


def filter_habits_per_period(habits: list[Habit], period: str):
    """
    Filters habits based on their frequency (e.g., DAILY or WEEKLY).

    Args:
        habits (list[Habit]): List of Habit objects.
        period (str): The frequency period to filter by.

    Returns:
        list: Indices of habits that match the specified frequency.
    """
    habit_indices = []
    for i, habit in enumerate(habits):
        if habit.frequency == period:
            habit_indices.append(i)

    return habit_indices


def count_streak_periods(habit: Habit):
    """
    Counts the total successful streak periods for a given habit, starting from today and going backwards.

    Args:
        habit (Habit): The Habit object to count streaks for.

    Returns:
        int: The count of streak periods.
    """
    streak_count = 0

    if len(habit.marked_dates) == 0:
        return 0
    
    current_date = datetime.today()
    while current_date >= habit.created:
        days_offset = 1

        if habit.frequency == "WEEKLY":
            days_offset = 7

        if habit.is_completed_in_this_period(current_date):
            streak_count += 1
        else:
            break

        current_date -= timedelta(days=days_offset)

    habit.longest_streak = streak_count

    return streak_count

def is_habit_on_the_list(habit_name: str, habit_file: str):
    """
    Checks if a habit with the given name exists in the habit file.

    Args:
        habit_name (str): The name of the habit to check.
        habit_file (str): The path to the habit file.

    Returns:
        bool: True if the habit exists, False otherwise.
    """
    habits = load_habits(habit_file)
    for habit in habits:
        if habit.name == habit_name:
            return True
    
    return False


def get_habit_list(habit_file: str):
    """
    Retrieves the list of habits from the specified habit file.

    Args:
        habit_file (str): The path to the habit file.

    Returns:
        list: The list of Habit objects.
    """
    habits = load_habits(habit_file)
    return habits

def save_habit_list(habits: list[Habit], habit_file: str):
    """
    Saves the list of habits to the specified habit file.

    Args:
        habits (list[Habit]): The list of Habit objects to save.
        habit_file (str): The path to the habit file.
    """
    save_habits(habits, habit_file)


def get_best_performing_tasks(habits: list[Habit]):
    """
    Retrieves the best-performing habits based on streak counts.

    Args:
        habits (list[Habit]): List of Habit objects.

    Returns:
        list: Sorted list of Habit objects in descending order of streak counts.
    """
    return get_top_performing_tasks(habits, True)


def get_most_struggled_tasks(habits: list[Habit]):
    """
    Retrieves the most struggled habits based on streak counts.

    Args:
        habits (list[Habit]): List of Habit objects.

    Returns:
        list: Sorted list of Habit objects in ascending order of streak counts.
    """
    return get_top_performing_tasks(habits, False)


def get_top_performing_tasks(habits: list[Habit], reverse: bool = True):
    """
    Retrieves the top-performing habits based on streak counts, sorted by the streak counts.

    Args:
        habits (list[Habit]): List of Habit objects.
        reverse (bool): If True, sort in descending order; if False, sort in ascending order.

    Returns:
        list: Sorted list of Habit objects based on streak counts.
    """
    # Create a list of habits with their corresponding streak counts
    habits_with_streaks = [(habit, count_streak_periods(habit)) for habit in habits]
    
    # Sort the list by streak count
    habits_with_streaks.sort(key=lambda x: x[1], reverse=reverse)
    
    # Extract the sorted habits
    sorted_habits = [habit for habit, streak in habits_with_streaks]
    
    return sorted_habits
