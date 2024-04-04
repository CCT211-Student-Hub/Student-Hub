from tkinter import *
import tkinter.ttk as ttk
import sqlite3
from tkinter.messagebox import *
from tkinter import font as tkfont
from models import Sqlite_Db, Task, Course

class Page(Frame):
    """An abstract class representing a page. Implemented as an overview page or course page"""
    db: Sqlite_Db
    page_name: str

    def __init__(self, parent, *args, **kwargs):
        self.app = parent.app
        self.db = Sqlite_Db()
        super().__init__(parent, *args, **kwargs)
        self.page_name = "Page"
        
        # Title font
        self.title_font = tkfont.Font(family='Montserrat', size=18, weight="bold")
        
        # Frame for holding treeview
        self.data_frame = Frame(self)
        self.data_frame.grid(row=2, column=0, sticky="nsew")
        
    def display_data(self):
        """Displays and sets up treeview for course tasks"""
        # Setting up treeview
        scrollbary = Scrollbar(self.data_frame, orient=VERTICAL)
        scrollbarx = Scrollbar(self.data_frame, orient=HORIZONTAL)
        self.tree = ttk.Treeview(self.data_frame, columns=("task id", "title", "description", "completed", "course_id"), height=10, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.tree.yview)
        scrollbary.grid(row=2, column=1, sticky="ns")
        scrollbarx.config(command=self.tree.xview)
        scrollbarx.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.tree.configure(yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.heading("task id", text="Task ID", anchor=W)
        self.tree.heading("title", text="Title", anchor=W)
        self.tree.heading("description", text="Description", anchor=W)
        self.tree.heading("completed", text="Completed", anchor=W)
        self.tree.heading("course_id", text="Course ID", anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=200)
        self.tree.column('#2', stretch=NO, minwidth=0, width=200)
        self.tree.column('#3', stretch=NO, minwidth=0, width=200)
        self.tree.column('#4', stretch=NO, minwidth=0, width=200)
        self.tree.column('#5', stretch=NO, minwidth=0, width=200)
        self.tree.grid(row=2, column=0, sticky="nsew")
        
    def populate_all_tasks(self):
        """Populating treeview with tasks from the SQLite Student Hub database"""
        tasks = Task.get_all_tasks(self.db)
        for task in tasks:
            self.tree.insert("", "end", values=(task.task_id, task.title, task.description, task.completed, task.course_id))
    
    def populate_by_course(self, course):
        """Populating the treeview with data filtered by the course name of a page"""
        tasks_by_course_id = Task.get_tasks_by_course(self.db, course.course_id)
        for task in tasks_by_course_id:
            self.tree.insert("", "end", values=(task.task_id, task.title, task.description, task.completed, task.course_id))
            
    def display_task_buttons(self):
        """Creating frame to hold buttons to add, edit, and delete tasks"""
        self.button_frame = Frame(self)
        self.button_frame.grid(row=3, column=0, sticky="s")
        
        self.add_task_button = Button(self.button_frame, text="Add Task")
        self.add_task_button.pack(side="left", anchor=W)
        self.edit_task_button = Button(self.button_frame, text="Edit Task")
        self.edit_task_button.pack(side="left", anchor=W)
        self.delete_task_button = Button(self.button_frame, text="Delete Task")
        self.delete_task_button.pack(side="left", anchor=W)

class OverviewPage(Page):
    """The page that shows all tasks, sorted by date"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.page_name = "Overview"
        self.label = Label(self, text=self.page_name, font=self.title_font, anchor="center")
        self.label.grid(row=0, column=0)
        
        self.display_data()
        self.populate_all_tasks()
        self.display_task_buttons()

    def get(self):
        return self.dataentry.get()

class CoursePage(Page):
    """The page that shows all tasks for a given course, sorted by date"""
    def __init__(self, parent, course, *args, **kwargs):
        """Takes a `course_name` which is set as the page name"""
        super().__init__(parent, *args, **kwargs)

        self.course = course
        self.page_name = course.course_name
        self.label = Label(self, text=self.page_name, font=self.title_font, anchor="center")
        self.label.grid(row=0, column=0)
        
        self.display_data()
        self.populate_by_course(course)
        self.display_task_buttons()

class NewCourse(Page):
    """The page that provides form to create a new course"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.page_name = "Create New Course"
        self.label = Label(self, text=self.page_name, font=self.title_font).grid(row=0, column=0)
        
        # Entry forms for relevant data
        self.course_name = Label(self, text="Course Name").grid(row=3, column=0)
        self.course_name_entry = Entry(self)
        self.course_name_entry.grid(row=3, column=1)
        
        # Adding buttons to submit/cancel changes
        self.submit = Button(self, text="Submit", command = self.submit_creation).grid(row=5, column = 0)
        self.cancel = Button(self, text="Cancel", command=self.cancel_creation).grid(row=5, column=1)
        
    def submit_creation(self):
        """Submits valid user input as a course in the sidebar and redirects them to the new course page"""
        user_course = self.course_name_entry.get()
        if len(user_course) == 0:
            # Adapted from https://docs.python.org/3/library/tkinter.messagebox.html
            showerror(title="Error: Empty Course", message="Please enter a course name.")
        else:
            course = Course.create_course(self.app.db, user_course)
            self.app.add_page(course)
            
            # Clearing text in entry box adapted from
            # https://www.tutorialspoint.com/how-to-clear-the-entry-widget-after-a-button-is-pressed-in-tkinter
            self.course_name_entry.delete(0, END)
        
    def cancel_creation(self):
        """Prompts user if they are certain of cancelling course entry."""
        user_course = self.course_name_entry.get()  # Retaining entry box
        if askyesno("Verify", "Are you sure you want to cancel course creation?"):
            showwarning("Yes", "Redirecting you back to course overview.")
            self.app.change_page(0)
        else:
            # Maintaining entry box to prevent it disappearing after the user selects 
            self.course_name_entry.insert(0, user_course) 
            