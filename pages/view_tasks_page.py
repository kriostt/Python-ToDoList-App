import streamlit as st
from datetime import datetime

from task import Task

# Method to view existing tasks
def view_tasks_page():
    st.title("List of Tasks")  # Title for the view tasks page

    # Fetch all tasks from the database
    tasks = Task.get_all_tasks()  # Call the class method to get all tasks

    # Dropdown to filter tasks by type
    task_type_filter = st.selectbox("Filter by Task Type", ["All", "Personal Task", "Work Task"])

    # Filter tasks based on selected type
    if task_type_filter != "All":
        if task_type_filter == "Personal Task":
            tasks = [task for task in tasks if 'event' in task] # Keep only personal tasks
        elif task_type_filter == "Work Task":
            tasks = [task for task in tasks if 'start_date' in task] # Keep only work tasks
    
    # Dropdown to sort tasks by due date
    sort_order = st.selectbox("Sort by Due Date", ["Ascending", "Descending"])
    
    # Sort tasks by due date based on user selection
    if sort_order == "Descending":
        tasks = sorted(tasks, key=lambda task: task['due_date'], reverse=True) # Sort in descending order
    else: 
        tasks = sorted(tasks, key=lambda task: task['due_date']) # Sort in ascending order

    # Prepare data for displaying tasks in a table format
    if tasks:
        table_data = [] # Initialize a list to hold task data for the table
        for task in tasks:
            # Create a dictionary for each task's data
            task_data = {
                'Title': task['title'],
                'Description': task['description'],
                'Due Date': datetime.strptime(task['due_date'], "%Y-%m-%d").strftime("%B %d, %Y"),
                'Priority': task['priority']
            }
            # Check if the user has selected to view all task types
            if task_type_filter == "All":
                # Retrieve the event associated with the task, or default to 'Not Specified' if it doesn't exist
                task_data['Event'] = task.get('event', 'Not Specified') 
                # Format the start date for display; if 'start_date' is not present, default to 'Not Specified'
                task_data['Start Date'] = datetime.strptime(task['start_date'], "%Y-%m-%d").strftime("%B %d, %Y") if 'start_date' in task else 'Not Specified'
            
            # Check if the user has selected to view personal tasks only
            elif task_type_filter == "Personal Task":
                # Retrieve the event type for personal tasks
                task_data['Event'] = task['event']
            
            # Check if the user has selected to view work tasks only
            elif task_type_filter == "Work Task":
                # Format the start date for display
                task_data['Start Date'] = datetime.strptime(task['start_date'], "%Y-%m-%d").strftime("%B %d, %Y") 
                
            table_data.append(task_data) # Append task data to the table list

        # Display the tasks in a table format
        st.table(table_data) # Render the table of tasks
    else:
        st.write("No tasks found.") # Display a message when no tasks are available