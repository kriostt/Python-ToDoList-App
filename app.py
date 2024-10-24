import streamlit as st
from datetime import datetime
from task import Task, PersonalTask, WorkTask

# Sidebar for navigation
st.sidebar.title("To-Do List App") # Title of the sidebar
# Description of the app
st.sidebar.write("Stay organized with your personal task manager. Quickly add, view, edit, and delete tasks to keep track of what matters most.")
page = st.sidebar.radio("Go to", ["Add Task", "View Tasks", "Edit Tasks", "Delete Tasks"]) # Navigation options in the sidebar
st.sidebar.image("logo.png", use_column_width=True) # Display logo image

# Section to add a new task
if page == "Add Task":
    st.title("Add a New Task") # Title for the add task page

    # Dropdown to select task type
    task_type = st.selectbox("Select Task Type", ["Personal Task", "Work Task"])
    
    # Inputs for task details
    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    due_date = st.date_input("Due Date", min_value=datetime.today())
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    
    # Logic for adding a personal task
    if task_type == "Personal Task":
        event = st.selectbox("Select Event Type", ["Chore","Hobby", "Occasion","Activity", "Errand"])
        if st.button("Add Personal Task"):
            task = PersonalTask(title, description, due_date, priority, event)
            task.save_to_db() # Save the task to the database
            st.success(f"Personal Task '{title}' added successfully!") 
    
    # Logic for adding a work task
    elif task_type == "Work Task":
        start_date = st.date_input("Start Date", min_value=datetime.today()) 
        if st.button("Add Work Task"):
            task = WorkTask(title, description, due_date, priority, start_date)
            task.save_to_db() # Save the task to the database
            st.success(f"Work Task '{title}' added successfully!")

# Section to view existing tasks
elif page == "View Tasks":
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

    


