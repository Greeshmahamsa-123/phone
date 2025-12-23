import csv
import os
from datetime import datetime

class Activity:
    """Represents a single fitness activity."""
    def __init__(self, date, activity_type, duration_minutes, calories_burned):
        self.date = date
        self.activity_type = activity_type
        self.duration_minutes = duration_minutes
        self.calories_burned = calories_burned

class FitnessTracker:
    """Manages fitness activities, file operations, and user interactions."""
    def __init__(self, filename="fitness_data.csv"):
        self.filename = filename
        self.activities = []
        self.load_data()

    def load_data(self):
        """Loads activities from the CSV file, handling potential errors."""
        if not os.path.exists(self.filename):
            print(f"[{self.filename}] not found. Starting with empty data.")
            return

        try:
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Type conversion with potential error handling (implicit in normal use)
                    try:
                        activity = Activity(
                            row['Date'],
                            row['Activity Type'],
                            int(row['Duration (min)']),
                            int(row['Calories Burned'])
                        )
                        self.activities.append(activity)
                    except ValueError:
                        print(f"Skipping invalid data row: {row}")
        except IOError as e:
            print(f"Error reading file [{self.filename}]: {e}")

    def save_data(self):
        """Saves current activities to the CSV file."""
        try:
            with open(self.filename, mode='w', newline='') as file:
                fieldnames = ['Date', 'Activity Type', 'Duration (min)', 'Calories Burned']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for activity in self.activities:
                    writer.writerow({
                        'Date': activity.date,
                        'Activity Type': activity.activity_type,
                        'Duration (min)': activity.duration_minutes,
                        'Calories Burned': activity.calories_burned
                    })
            print("Data saved successfully.")
        except IOError as e:
            print(f"Error saving file [{self.filename}]: {e}")

    def add_activity(self):
        """Prompts user for input and adds a new activity."""
        date = datetime.now().strftime("%Y-%m-%d")
        activity_type = input("Enter activity type: ")
        
        while True:
            try:
                duration = int(input("Enter duration in minutes: "))
                calories = int(input("Enter calories burned: "))
                if duration <= 0 or calories <= 0:
                    raise ValueError("Duration and calories must be positive numbers.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter numeric values.")
        
        new_activity = Activity(date, activity_type, duration, calories)
        self.activities.append(new_activity)
        self.save_data()

    def view_summary(self):
        """Displays a summary of logged activities."""
        if not self.activities:
            print("No activities logged yet.")
            return

        total_calories = sum(a.calories_burned for a in self.activities)
        total_duration = sum(a.duration_minutes for a in self.activities)
        print("\n--- Fitness Summary ---")
        for act in self.activities:
            print(f"{act.date}: {act.activity_type} for {act.duration_minutes} min, {act.calories_burned} kcal")
        print(f"Total Duration: {total_duration} minutes")
        print(f"Total Calories Burned: {total_calories} kcal")
        print("-----------------------\n")

# Main application loop
if __name__ == "__main__":
    tracker = FitnessTracker()
    while True:
        print("\n1. Add Activity")
        print("2. View Summary")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            tracker.add_activity()
        elif choice == '2':
            tracker.view_summary()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")