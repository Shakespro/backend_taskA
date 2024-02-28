To-Do List App
This To-Do List App is a web application that consists of both frontend and backend components.

This repository in particular being the backend component.

The app allows users to create, manage, and organize tasks with options to mark them as complete or incomplete. The app is designed to provide a seamless experience between the frontend interface and the backend database.

Features
Frontend Component: The frontend component of the app displays a user-friendly interface where users can add tasks with a title, description, and a checkbox to mark the task as complete or incomplete. The tasks are then separated based on their completion status for better organization.

Backend Component: The backend component of the app provides API endpoints to interact with the data stored in a PostgreSQL database. Users can retrieve task data by clicking the "Get" button, and any changes made to the tasks in the backend will reflect on both the frontend and the database.

Usage
Adding Tasks: Users can add tasks by providing a title, description, and selecting the completion status using checkboxes on the frontend. These changes are reflected in real-time on the frontend interface.

Backend Interaction: Clicking the "Get" button triggers an API call to fetch task data from the backend. Any modifications made to tasks in the backend database will automatically update both the frontend display and the database records.

Technologies Used
Frontend: HTML, CSS, JavaScript
Backend: Python, Flask (or Django), PostgreSQL
Other: JSON, RESTful API
Setup
Clone the repository to your local machine.
Install the necessary dependencies for both frontend and backend components.
Configure the PostgreSQL database connection.
Run the application to start using the To-Do List App.
Feel free to customize this README text further based on additional details or specific configurations of your app.

The frontend component is frontend_task under the same profile https://github.com/Shakespro/frontend_task
