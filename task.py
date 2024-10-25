from pymongo import MongoClient # Import MongoClient for MongoDB operations

# MongoDB connection
client = MongoClient("mongodb+srv://ahavendicacion:nc2cWwmdqNDgZ3QB@cluster0.zpjulrc.mongodb.net/")
db = client['task_management'] # Access the 'task_management' database
tasks_collection = db['tasks'] # Access the 'tasks' collection within the database

# Base Task class
class Task:
    def __init__(self, title, description, due_date, priority):
        self._title = title  # protected attribute
        self._description = description  # protected attribute
        self._due_date = due_date  # protected attribute
        self._priority = priority  # protected attribute

    @classmethod
    def get_all_tasks(cls):
        tasks = list(tasks_collection.find())  # Fetch all tasks from the MongoDB collection
        return tasks # Return the list of tasks

# Subclass for PersonalTask
class PersonalTask(Task):
    def __init__(self, title, description, due_date, priority, event):
        super().__init__(title, description, due_date, priority) # Call the initializer of the base Task class
        self._event = event

    def save_to_db(self):
        # Prepare task data for saving to the database
        task_data = {
            'title': self._title,
            'description': self._description,
            'due_date': self._due_date.strftime("%Y-%m-%d"), # Format due date as a string
            'priority': self._priority,
            'event': self._event
        }
        tasks_collection.insert_one(task_data)  # Insert the task data into the MongoDB collection
        return f"Personal Task '{self._title}' saved to the database." # Return a confirmation message

# Subclass for WorkTask
class WorkTask(Task):
    def __init__(self, title, description, due_date, priority, start_date):
        super().__init__(title, description, due_date, priority) # Call the initializer of the base Task class
        self._start_date = start_date  # protected attribute

    def save_to_db(self):
        # Prepare task data for saving to the database
        task_data = {
            'title': self._title,
            'description': self._description,
            'due_date': self._due_date.strftime("%Y-%m-%d"), # Format due date as a string
            'priority': self._priority,
            'start_date': self._start_date.strftime("%Y-%m-%d"), # Format start date as a string
        }
        tasks_collection.insert_one(task_data) # Insert the task data into the MongoDB collection
        return f"Work Task '{self._title}' saved to the database."  # Return a confirmation message




