import streamlit as st
from datetime import datetime

from task import Task, PersonalTask, WorkTask
from pages.view_tasks_page import view_tasks_page

# Method to edit an existing task
def edit_task_page():
    # Title for the edit task page
    st.title("Edit an Existing Task") 

    # Fetch all tasks from the database
    tasks = Task.get_all_tasks()
    # Get titles of all tasks for selection
    task_titles = ["Select a Task"] + [task['title'] for task in tasks] 
        
    # Dropdown to select the task to edit
    selected_task_title = st.selectbox("Select Task to Edit", task_titles)
    # Find the selected task's details
    selected_task = next((task for task in tasks if task['title'] == selected_task_title), None)

    if selected_task:
        # Inputs for editing common task details
        new_title = st.text_input("Edit Task Title", value=selected_task['title'])
        new_description = st.text_area("Edit Task Description", value=selected_task['description'])
        new_due_date = st.date_input("Edit Due Date", value=datetime.strptime(selected_task['due_date'], "%Y-%m-%d"))
        new_due_date_str = new_due_date.strftime("%Y-%m-%d")
        new_priority = st.selectbox("Edit Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(selected_task['priority']))

        # Determine the task type for conditional input
        task_type = "Personal Task" if 'event' in selected_task else "Work Task"

        # Check if task type is personal task, add new event if it is
        if task_type == "Personal Task":
            new_event = st.selectbox("Edit Event Type", ["Chore", "Hobby", "Occasion", "Activity", "Errand"], index=["Chore", "Hobby", "Occasion", "Activity", "Errand"].index(selected_task['event']))
        else:
            new_event = None

        # Check if task type is work task, add new start date if it is
        if task_type == "Work Task":
            new_start_date = st.date_input("Edit Start Date", value=datetime.strptime(selected_task['start_date'], "%Y-%m-%d"))
            new_start_date_str = new_start_date.strftime("%Y-%m-%d")
        else:
            new_start_date_str = None

        # Button to update the task
        if st.button("Update Task"):
            # Call method to update the task in the database
            Task.update_task(selected_task['_id'], new_title, new_description, new_due_date_str, new_priority, new_event, new_start_date_str)  

            # Success message
            st.success(f"Task '{selected_task_title}' updated successfully!") 

            # Refresh the page
            st.rerun()