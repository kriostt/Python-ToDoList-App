import streamlit as st
from datetime import datetime
from task import Task, PersonalTask, WorkTask

# Method to add a new task
def add_task_page():
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