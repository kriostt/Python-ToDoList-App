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
    
    @classmethod
    def update_task(cls, task_id, new_title, new_description, new_due_date, new_priority, new_event=None, new_start_date=None):
        # Set new values to the user input
        new_values = { "$set": { 'title': new_title, 'description': new_description, 'due_date': new_due_date, 'priority': new_priority}}

        # Check if a new event is provided and update if it is 
        if new_event != None:
            new_values["$set"]['event'] = new_event

        # Check if a new start date is provided and update if it is 
        if new_start_date != None:
            new_values["$set"]['start_date'] = new_start_date

        # Update the task in the MongoDB collection
        tasks_collection.update_one({"_id": task_id}, new_values)
        
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