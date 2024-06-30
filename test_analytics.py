import unittest
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
from Habit import Habit
from analytics import (
    filter_habits_unchecked,
    filter_habits_per_period,
    count_streak_periods,
    is_habit_on_the_list,
    get_habit_list,
    save_habit_list,
    get_best_performing_tasks,
    get_most_struggled_tasks
)
from storage import load_habits, save_habits



class TestAnalytics(unittest.TestCase):

   

    @patch('storage.load_habits')
    def setUp(self, mock_load_habits):
        self.habit_file = 'test_habits.json'
        with open(self.habit_file, 'r') as file:
            mock_load_habits.return_value = load_habits(self.habit_file)
        self.habits = get_habit_list(self.habit_file)
        

    def test_filter_habits_unchecked(self):
        unchecked_habits = filter_habits_unchecked(self.habits)
        self.assertIn(4, unchecked_habits)  # "Do yoga is unchecked always

    def test_filter_habits_per_period(self):
        daily_habits = filter_habits_per_period(self.habits, "DAILY")
        weekly_habits = filter_habits_per_period(self.habits, "WEEKLY")
        self.assertEqual(len(daily_habits), 3)
        self.assertEqual(len(weekly_habits), 2)

    def test_count_streak_periods(self):
        daily_streak = count_streak_periods(self.habits[1])  # "Eat vegetables"
        weekly_streak = count_streak_periods(self.habits[0])  # "Read a book"
        self.assertEqual(daily_streak, 4)
        self.assertEqual(weekly_streak, 4)

    @patch('storage.load_habits')
    def test_is_habit_on_the_list(self, mock_load_habits):
        mock_load_habits.return_value = self.habits
        self.assertTrue(is_habit_on_the_list("Read a book", self.habit_file))
        self.assertFalse(is_habit_on_the_list("Meditation", self.habit_file))

    @patch('storage.load_habits')
    def test_get_habit_list(self, mock_load_habits):
        mock_load_habits.return_value = self.habits
        habits = get_habit_list(self.habit_file)
        self.assertEqual(len(habits), 5)

    @patch('analytics.save_habits')
    def test_save_habit_list(self, mock_save_habits):
        save_habit_list(self.habits, self.habit_file)
        self.assertEqual(mock_save_habits.call_count, 1)

    def test_get_best_performing_tasks(self):
        best_tasks = get_best_performing_tasks(self.habits)
        self.assertEqual(best_tasks[0].name, "Read a book")
        self.assertEqual(best_tasks[1].name, "Eat vegetables")

    def test_get_most_struggled_tasks(self):
        struggled_tasks = get_most_struggled_tasks(self.habits)
        self.assertEqual(struggled_tasks[0].name, "Do yoga")
        self.assertEqual(struggled_tasks[1].name, "Drink water")


if __name__ == '__main__':
    unittest.main()