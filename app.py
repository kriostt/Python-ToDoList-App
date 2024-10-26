import streamlit as st

from pages.add_task_page import add_task_page 
from pages.view_tasks_page import view_tasks_page
from pages.edit_task_page import edit_task_page
from pages.delete_task_page import delete_task_page

# -----Sidebar for navigation-----
# Define application pages
pages = [
        st.Page(add_task_page, title="Add a New Task"),
        st.Page(view_tasks_page, title="List of Tasks"),
        st.Page(edit_task_page, title="Edit an Existing Task"),
        st.Page(delete_task_page, title="Delete an Existing Task")
]
# Set the navigation items to the pages defined
page = st.navigation(pages)
# Render the page
page.run()

# Title of the sidebar
st.sidebar.title("To-Do List App") 
# Description of the app
st.sidebar.write("Stay organized with your personal task manager. Quickly add, view, edit, and delete tasks to keep track of what matters most.")
# Display logo image
st.sidebar.image("logo.png", use_column_width=True) 