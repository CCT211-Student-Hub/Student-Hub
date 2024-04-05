# Student Hub

## Introducing Student Hub

Created by students, for students, Student Hub is a digital to-do list repository that is seamlessly accessible through any operating system with Python. Student Hub emerged from the need to keep track of assignments, upcoming deadlines, and daily tasks – activities that can quickly feel overwhelming for students with the busy nature of every semester. To combat the universal struggle of disorganization, Student Hub has made it easy for students to catalogue tasks for academic or daily use. Students can log due dates and flag the priority of each task, which are then displayed in an organized manner. By visualizing the number of tasks that need to be completed and categorizing tasks based on importance and urgency, Student Hub can help alleviate the potential stresses and academic downfalls that come with disorganization and procrastination, steering students towards academic success one task at a time.

## User Guide

To begin streamlining your task management, run `app.py` for an empty database or run `populate_db.py` to see examples of pre-existing tasks in the database. The left sidebar toggles between different pages, offering users an ***Overview**** of all their tasks, sorting tasks by ***Course***, or ***Creating a new course*** by entering the course name. 

Three buttons can be found below the databases on the Overview and Course pages and can be selected to control task functions: adding, editing, and deleting. To ***Add*** a task, simply press the add button and fill in/select the required fields: __title, description, course name (chosen from the list of existing courses), and priority (ranged from 1-5). Adding a task assumes that the task has yet to be completed, so the completed status is automatically set to False. ***Editing*** a task will allow users to update existing tasks and change their attributes. In this section, users can also mark tasks as complete, which will subsequently delete the task. The ***Delete*** button will delete the task from the database as well.

**NOTE**: Edit and delete buttons will only be clickable upon the user selecting a task from the database.

## Running the app

To run the app, run the command `python app.py`, which will start the program, creating a `student_hub.db` database file if one does not exist.

## Sample database

To demonstrate how Student Hub works from the perspective of a student, we have provided a script to create a sample database prefilled with courses and tasks. To run this script, run the command `python populate_db.py`. 

⚠️ Note that this will delete the existing database, meaning all exisiting work will be lost. 

## Authors

Created by [Jannine Uy](https://github.com/meiilktea) and [William Ma](https://github.com/willmadev)

## Acknowledgements

This program was created as a project for CCT211: Fundamentals of User Interface Programming. This project was created with help and guidance from Professor Michael Nixon.
