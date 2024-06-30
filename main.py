from Habit import Habit
import analytics 
import os
import time

habit_file = "habits.json"  # Path to the JSON file where habits are stored

# Convert a digit to a frequency string
def get_frequency_string(digit: str):
    """
    Converts a digit to a corresponding frequency string.

    Args:
        digit (str): The digit representing the frequency.

    Returns:
        str: The corresponding frequency string or 'WRONG' if the input is invalid.
    """
    if digit == '1':
        return "DAILY"
    elif digit == '2':
        return "WEEKLY"
    else:
        return "WRONG"

# Clear the console
def clear():
    """
    Clears the console screen.
    """
    os.system("cls")

# Print out the list of habits based on the provided indices
def print_out_habit_list(habits: list[Habit], indices: list[int] = None):
    """
    Prints out the list of habits based on the provided indices.

    Args:
        habits (list[Habit]): List of Habit objects.
        indices (list[int], optional): List of indices to print. Defaults to None.
    """
    if indices is None: 
        return
    
    for i, value in enumerate(indices):
        print(f"{value+1}. {habits[value].name}")

# Print out the top streaks from the habit list
def print_out_streak_top(habits: list[Habit], top_count: int = None):
    """
    Prints out the top streaks from the habit list.

    Args:
        habits (list[Habit]): List of Habit objects.
        top_count (int, optional): Number of top streaks to print. Defaults to None.
    """
    for i, habit in enumerate(habits):
        if habit.longest_streak == 1:
            print(f"            {i+1} - {habit.name} ({habit.longest_streak} period)")
        else:
            print(f"            {i+1} - {habit.name} ({habit.longest_streak} periods)")

        if top_count is not None and i >= top_count - 1:
            break

# Create a new habit
def create_new_habit():
    """
    Creates a new habit by collecting user input and saving it to the habit list.
    """
    while True:
        name = input("Enter the name of the new habit: ")

        if name == "":
            print("Name cannot be empty, please use a different name!")
            time.sleep(3)  # Pause to let user see the message
            break
        elif analytics.is_habit_on_the_list(name, habit_file):
            print("Habit with such name is already being tracked, please choose another name")  
            time.sleep(3)  # Pause to let user see the message
            break

        description = input("Enter a short description of the habit (optional): ")
        freq_digit = input("Enter the habit frequency: \n1. DAILY \n2. WEEKLY:\nSelect an option (1-2): ")

        # Check for input validity
        frequency = get_frequency_string(freq_digit)
        if frequency == "WRONG":
            print("Incorrect habit frequency, try again!")  
        else:
            # Create a new habit object
            habit = Habit(name, description, frequency)

            # Dynamically update the habits list
            habits = analytics.get_habit_list(habit_file)
            habits.append(habit)
            analytics.save_habit_list(habits, habit_file)
            clear()
            print(f"Habit '{name}' added successfully!")
            time.sleep(3)  # Pause to let user see the message
            break

# Menu for individual habit actions
def individual_habit_menu(selected_habit: Habit, habits: list[Habit]):
    """
    Displays the menu for individual habit actions.

    Args:
        selected_habit (Habit): The selected habit object.
        habits (list[Habit]): List of all habit objects.
    """
    while True:
        clear()

        print("Your selected habit details:\n")
        selected_habit.print_out()
        longest_streak = analytics.count_streak_periods(selected_habit)

        if longest_streak == 1:
            print(f"Current longest streak: {longest_streak} period.")
        else:
            print(f"Current longest streak: {longest_streak} periods.")
            
        print("\nActions:")
        print("1. Mark task completed")
        print("2. Delete habit")
        print("3. Return back to habit list")

        selected_option = input("Select an option (1-3): ")

        if selected_option == '1':
            selected_habit.mark_complete()
            print("Task completed!")
            time.sleep(2)  # Pause to let user see the message
            # Save the changes
            analytics.save_habit_list(habits, habit_file)

            # Return back to main list
            break

        elif selected_option == '2':
            delete_option = input("Are you sure you want to delete this habit? y/n: ")

            if delete_option.lower() == 'y':
                habits.remove(selected_habit)

                # Save the changes
                analytics.save_habit_list(habits, habit_file)
                print("Habit deleted.")
                time.sleep(3)  # Pause to let user see the message
                break  # Exit loop to return to habit list
            else:
                continue  # Continue to show the menu again

        elif selected_option == '3':
            break  # Exit loop to return to habit list

        else:
            print("Invalid input. Please enter a valid option 1-3")
            time.sleep(3)  # Pause to let user read the message

# List all habits
def list_all_habits():
    """
    Lists all habits, categorized by their status and frequency.
    """
    while True:
        clear()
        habits = analytics.get_habit_list(habit_file)
        if not habits:  
            print("No habits found.")
            time.sleep(2)  # Pause to let user see the message
            break
        else:
            print("Tasks not yet checked-off:")
            uncheck_indices = analytics.filter_habits_unchecked(habits)
            print_out_habit_list(habits, uncheck_indices)

            print("\nWeekly habits:")
            weekly_indices = analytics.filter_habits_per_period(habits, "WEEKLY")
            print_out_habit_list(habits, weekly_indices)

            print("\nDaily habits:")
            daily_indices = analytics.filter_habits_per_period(habits, "DAILY")
            print_out_habit_list(habits, daily_indices)

            print("\n0. Back to Main Menu\n")
            selected_option = input(f"Select an option (0-{len(habits)}): ")
            try:
                selected_int = int(selected_option)
                if selected_int <= 0:
                    break
                elif selected_int > len(habits):
                    print(f"Selected habit out of range. Please enter a valid option (0-{len(habits)})")
                    time.sleep(3)
                else:
                    selected_habit = habits[selected_int-1]
                    individual_habit_menu(selected_habit, habits)
            except ValueError:
                print("Invalid input. Please enter an integer value.")
                time.sleep(3)

# Habits analytics
def habits_analytics():
    """
    Displays analytics for the habits, including the total number of habits,
    top performing habits, and most struggled habits.
    """
    habits = analytics.get_habit_list(habit_file)
    clear()
    if not habits:
        print("No habits found.")
        time.sleep(2)  # Pause to let user see the message
    else:
        print(f"Total number of habits: {len(habits)}")
        print("\nTop 5 longest streaks:")
        best_habit_list = analytics.get_best_performing_tasks(habits)
        print_out_streak_top(best_habit_list, 5)

        print("\nTop 5 most struggling habits:")
        worst_habit_list = analytics.get_most_struggled_tasks(habits)
        print_out_streak_top(worst_habit_list, 5)

        print("\nActions:")

        selected_option = input("0. Return back to Main Menu: ")

# Main menu
def main_menu():
    """
    Displays the main menu and handles user input to navigate through different options.
    """
    while True:
        clear()
        print("\nMain Menu:")
        print("1. Create New Habit")
        print("2. List All Habits")
        print("3. Habits Analytics")
        print("4. Exit")
        choice = input("Select an option (1-4): ")

        if choice == '1':
            create_new_habit()
        elif choice == '2':
            list_all_habits()
        elif choice == '3':
            habits_analytics()
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main_menu()
