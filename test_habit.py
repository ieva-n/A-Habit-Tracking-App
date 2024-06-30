import unittest
from datetime import datetime, timedelta
from Habit import Habit 

class TestHabit(unittest.TestCase):

    def setUp(self):
        self.habit_daily = Habit("Exercise", "Daily exercise", "DAILY")
        self.habit_weekly = Habit("Reading", "Read a book", "WEEKLY")

    def test_initialization(self):
        self.assertEqual(self.habit_daily.name, "Exercise")
        self.assertEqual(self.habit_daily.description, "Daily exercise")
        self.assertEqual(self.habit_daily.frequency, "DAILY")
        self.assertTrue(isinstance(self.habit_daily.created, datetime))
        self.assertEqual(self.habit_daily.marked_dates, [])
        self.assertEqual(self.habit_daily.longest_streak, 0)

    def test_mark_complete(self):
        self.habit_daily.mark_complete()
        self.assertEqual(len(self.habit_daily.marked_dates), 1)
        self.assertTrue(isinstance(self.habit_daily.marked_dates[0], datetime))
        self.habit_daily.mark_complete()  # Marking again on the same day should not add a new date
        self.assertEqual(len(self.habit_daily.marked_dates), 1)

    def test_is_completed_in_this_period_daily(self):
        today = datetime.today()
        self.habit_daily.mark_complete()
        self.assertTrue(self.habit_daily.is_completed_in_this_period(today))
        tomorrow = today + timedelta(days=1)
        self.assertFalse(self.habit_daily.is_completed_in_this_period(tomorrow))

    def test_is_completed_in_this_period_weekly(self):
        today = datetime.today()
        self.habit_weekly.mark_complete()
        self.assertTrue(self.habit_weekly.is_completed_in_this_period(today))
        next_week = today + timedelta(weeks=1)
        self.assertFalse(self.habit_weekly.is_completed_in_this_period(next_week))
        self.habit_weekly.marked_dates.append(next_week)
        self.assertTrue(self.habit_weekly.is_completed_in_this_period(next_week))

    def test_to_dict(self):
        self.habit_daily.mark_complete()
        habit_dict = self.habit_daily.to_dict()
        self.assertEqual(habit_dict['name'], "Exercise")
        self.assertEqual(habit_dict['description'], "Daily exercise")
        self.assertEqual(habit_dict['frequency'], "DAILY")
        self.assertTrue(isinstance(habit_dict['created'], str))
        self.assertTrue(isinstance(habit_dict['marked_dates'][0], str))

    def test_from_dict(self):
        self.habit_daily.mark_complete()
        habit_dict = self.habit_daily.to_dict()
        new_habit = Habit.from_dict(habit_dict)
        self.assertEqual(new_habit.name, self.habit_daily.name)
        self.assertEqual(new_habit.description, self.habit_daily.description)
        self.assertEqual(new_habit.frequency, self.habit_daily.frequency)
        self.assertEqual(new_habit.created, self.habit_daily.created)
        self.assertEqual(new_habit.marked_dates, self.habit_daily.marked_dates)

    def test_print_out(self):
        # This test captures the printed output and verifies its correctness
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output
        self.habit_daily.print_out()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip().split('\n')
        self.assertIn("Name: Exercise", output)
        self.assertIn("Description: Daily exercise", output)
        self.assertIn("Frequency: DAILY", output)
        self.assertTrue(any("Created: " in line for line in output))

if __name__ == '__main__':
    unittest.main()