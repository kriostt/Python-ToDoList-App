import streamlit as st
from datetime import datetime

from task import Task

# Method to delete an existing task
def delete_task_page():
    # Title for the delete task page
    st.title("Delete an Existing Task") 

    # Fetch all tasks from the database
    tasks = Task.get_all_tasks()
    # Get titles of all tasks for selection
    task_titles = ["Select a Task"] + [task['title'] for task in tasks] 

    # Dropdown to select the task to delete
    selected_task_title = st.selectbox("Select Task to Delete", task_titles)
    # Find the selected task's details
    selected_task = next((task for task in tasks if task['title'] == selected_task_title), None)

    if selected_task:
        # Show details for the selected task
        st.subheader("Task Details")
        st.write(f"**Title:** {selected_task['title']}")
        st.write(f"**Description:** {selected_task['description']}")
        st.write(f"**Due Date:** {selected_task['due_date']}")
        st.write(f"**Priority:** {selected_task['priority']}")
        if 'event' in selected_task:
            st.write(f"**Event Type:** {selected_task['event']}")         
        else:
            st.write("**Event Type:** N/A")

        if 'start_date' in selected_task:
            st.write(f"**Start Date:** {selected_task['start_date']}")
        else:
            st.write("**Start Date:** N/A")

        # Button to delete the task
        if st.button("Delete Task"):
            # Call method to delete the task in the database
            Task.delete_task(selected_task['_id'])

            # Success message
            st.success(f"Task '{selected_task_title}' deleted successfully!") 
            
            # Refresh the page
            st.rerun() 