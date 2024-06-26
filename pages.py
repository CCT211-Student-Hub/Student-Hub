from tkinter import *
import tkinter.ttk as ttk
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
        self.tree = ttk.Treeview(self.data_frame, columns=( "title", "description", "completed", "course_id", "priority"), height=28, selectmode="extended", yscrollcommand=scrollbary.set)
        scrollbary.config(command=self.tree.yview)
        scrollbary.grid(row=2, column=1, sticky="ns")
        self.tree.heading("title", text="Title", anchor=W)
        self.tree.heading("description", text="Description", anchor=W)
        self.tree.heading("completed", text="Completed", anchor=W)
        self.tree.heading("course_id", text="Course ID", anchor=W)
        self.tree.heading("priority", text="Priority", anchor=W)
        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=200)
        self.tree.column("#2", stretch=NO, minwidth=0, width=330)
        self.tree.column("#3", stretch=NO, minwidth=0, width=75)
        self.tree.column("#4", stretch=NO, minwidth=0, width=100)
        self.tree.column("#5", stretch=NO, minwidth=0, width=75)
        self.tree.bind('<<TreeviewSelect>>', self.data_selected) # Adapted from Bryan Oakley on https://stackoverflow.com/questions/61404261/tkinter-selecting-an-item-from-a-treeview-using-single-click-instead-of-double
        self.tree.grid(row=2, column=0, sticky="nsew")
    
    def data_selected(self, event):
        """Obtain task information from the row selection. Includes task_id, title, description, completed, and course_id"""
        if not event.widget.selection():
            return
        
        self.task_id = event.widget.selection()[0] # Obtaining task_id from user selection in treeview (first value in tuple)
        self.task_id_data = event.widget.item(self.task_id) # Obtaining data from selected task_id
        self.task_id_values = self.task_id_data["values"]
        
        # Storing task information in task variable obtained from student hub database
        self.selected_task = Task.get_task(self.db, self.task_id)
        
        # Switching state of edit button to normal if user selects a row in the treeview
        # State of button adapted from # adapted from https://www.geeksforgeeks.org/how-to-change-tkinter-button-state/
        if self.task_id:
            self.edit_task_button.config(state=NORMAL)
            self.delete_task_button.config(state=NORMAL)
        
    def populate_all_tasks(self):
        """Populating treeview with tasks from the SQLite Student Hub database"""
        tasks = Task.get_all_tasks(self.db)
        for task in tasks:
            self.tree.insert("", "end", task.task_id, values=(task.title, task.description, task.completed, Course.get_course(self.app.db, task.course_id).course_name, task.priority))
    
    def populate_by_course(self, course):
        """Populating the treeview with data filtered by the course name of a page"""
        tasks_by_course_id = Task.get_tasks_by_course(self.db, course.course_id)
        for task in tasks_by_course_id:
            self.tree.insert("", "end", task.task_id, values=(task.title, task.description, task.completed, course.course_name, task.priority))
            
    def display_task_buttons(self):
        """Creating frame to hold buttons to add, edit, and delete tasks"""
        self.button_frame = Frame(self)
        self.button_frame.grid(row=3, column=0, sticky="s")
        
        self.add_task_button = Button(self.button_frame, text="Add Task", command=self.add_task_handler)
        self.add_task_button.pack(side="left", anchor=W)
        self.edit_task_button = Button(self.button_frame, text="Edit Task", command=self.edit_task_handler, state=DISABLED)
        self.edit_task_button.pack(side="left", anchor=W)
        self.delete_task_button = Button(self.button_frame, text="Delete Task", command=self.delete_task_hander, state=DISABLED)
        self.delete_task_button.pack(side="left", anchor=W)
        
    def add_task_handler(self):
        """Raises a new frame to display entry boxes for a new task"""
        self.add_task_frame = Frame(self)
        self.add_task_frame.grid(row=0, column=0, sticky="nsew", rowspan=self.grid_size()[1], columnspan=self.grid_size()[0])
        self.curr_frame = self.add_task_frame
        self.add_task_frame.tkraise()
        
        self.label = Label(self.add_task_frame, text="Add Task", font=self.title_font, anchor="center")
        self.label.grid(row=0, column=0, columnspan=2)
        
        # Entry forms for relevant data
        self.task_title = Label(self.add_task_frame, text="Title")
        self.task_title.grid(row=1, column=0)
        self.task_title_entry = Entry(self.add_task_frame)
        self.task_title_entry.grid(row=1, column=1)
        self.task_title_entry.focus() # Adapted from user unutbu from https://stackoverflow.com/questions/13626406/setting-focus-to-specific-tkinter-entry-widget 
        
        self.task_desc = Label(self.add_task_frame, text="Description")
        self.task_desc.grid(row=2, column=0)
        self.task_desc_entry = Entry(self.add_task_frame)
        self.task_desc_entry.grid(row=2, column=1)

        self.task_course_name = Label(self.add_task_frame, text="Course Name")
        self.task_course_name.grid(row=4, column=0)
        self.task_course_selection = StringVar()
        self.task_course_dropdown = OptionMenu(self.add_task_frame, self.task_course_selection, *[course.course_name for course in Course.get_all_courses(self.app.db)])
        if isinstance(self, CoursePage):
            self.task_course_selection.set(self.course.course_name)
        self.task_course_dropdown.grid(row=4, column=1)
        
        # Radio button selection adapted from https://www.tutorialspoint.com/python/tk_radiobutton.htm
        self.task_priority = Label(self.add_task_frame, text="Task Priority")
        self.task_priority.grid(row=5, column=0)
        self.task_priority_value = IntVar()
        self.task_priority1 = Radiobutton(self.add_task_frame, text="1", variable=self.task_priority_value, value=1)
        self.task_priority1.grid(row=5, column=1)
        self.task_priority2 = Radiobutton(self.add_task_frame, text="2", variable=self.task_priority_value, value=2)
        self.task_priority2.grid(row=6, column=1)
        self.task_priority3 = Radiobutton(self.add_task_frame, text="3", variable=self.task_priority_value, value=3)
        self.task_priority3.grid(row=7, column=1)
        self.task_priority4 = Radiobutton(self.add_task_frame, text="4", variable=self.task_priority_value, value=4)
        self.task_priority4.grid(row=8, column=1)
        self.task_priority5 = Radiobutton(self.add_task_frame, text="5", variable=self.task_priority_value, value=5)
        self.task_priority5.grid(row=9, column=1)

        # Adding buttons to submit/cancel changes
        self.submit = Button(self.add_task_frame, text="Submit", command = self.submit_action)
        self.submit.grid(row=12, column = 0)
        self.cancel = Button(self.add_task_frame, text="Cancel", command=lambda: self.cancel_action(self.add_task_frame))
        self.cancel.grid(row=12, column=1)
        
    def edit_task_handler(self):
        """Raises a new frame to display entry boxes to edit task"""
        self.edit_task_frame = Frame(self)
        self.edit_task_frame.grid(row=0, column=0, sticky="nsew", rowspan=self.grid_size()[1], columnspan=self.grid_size()[0])
        self.curr_frame = self.edit_task_frame
        self.edit_task_frame.tkraise()
        
        self.label = Label(self.edit_task_frame, text="Edit Task", font=self.title_font, anchor="center")
        self.label.grid(row=0, column=0, columnspan=2)
        
        # Entry forms for relevant data
        self.edited_title = Label(self.edit_task_frame, text="Title")
        self.edited_title.grid(row=1, column=0)
        self.edited_title_entry = Entry(self.edit_task_frame)
        self.edited_title_entry.grid(row=1, column=1)
        self.edited_title_entry.insert(0, self.task_id_data["values"][0])
        self.edited_title_entry.focus() 
        
        self.edited_desc = Label(self.edit_task_frame, text="Description")
        self.edited_desc.grid(row=2, column=0)
        self.edited_desc_entry = Entry(self.edit_task_frame)
        self.edited_desc_entry.grid(row=2, column=1)
        self.edited_desc_entry.insert(0, self.task_id_data["values"][1])

        self.edited_completion = Label(self.edit_task_frame, text="Completion")
        self.edited_completion.grid(row=3, column=0)
        self.complete_var = IntVar()
        self.complete_var.set(int(self.selected_task.completed))
        self.edited_completion_entry = Checkbutton(self.edit_task_frame, variable=self.complete_var)
        self.edited_completion_entry.grid(row=3, column=1)

        self.edited_course_name = Label(self.edit_task_frame, text="Course Name")
        self.edited_course_name.grid(row=4, column=0)
        self.edited_course_name_entry = Entry(self.edit_task_frame)
        self.course_name = self.task_id_data["values"][3]
        self.edited_course_name_entry.insert(0, self.course_name)
        self.edited_course_name_entry.config(state=DISABLED)
        self.edited_course_name_entry.grid(row=4, column=1)
        
        self.edited_priority = Label(self.edit_task_frame, text="Task Priority")
        self.edited_priority.grid(row=5, column=0)
        self.edited_priority_value = IntVar()
        self.edited_priority_value.set(self.task_id_data["values"][4])
        self.task_priority1 = Radiobutton(self.edit_task_frame, text="1", variable=self.edited_priority_value, value=1)
        self.task_priority1.grid(row=5, column=1)
        self.task_priority2 = Radiobutton(self.edit_task_frame, text="2", variable=self.edited_priority_value, value=2)
        self.task_priority2.grid(row=6, column=1)
        self.task_priority3 = Radiobutton(self.edit_task_frame, text="3", variable=self.edited_priority_value, value=3)
        self.task_priority3.grid(row=7, column=1)
        self.task_priority4 = Radiobutton(self.edit_task_frame, text="4", variable=self.edited_priority_value, value=4)
        self.task_priority4.grid(row=8, column=1)
        self.task_priority5 = Radiobutton(self.edit_task_frame, text="5", variable=self.edited_priority_value, value=5)
        self.task_priority5.grid(row=9, column=1)
        
        # Adding buttons to save/cancel actions
        self.save_changes_btn = Button(self.edit_task_frame, text="Save", command = self.save_changes, state=NORMAL)
        self.save_changes_btn.grid(row=10, column = 0)
        self.cancel = Button(self.edit_task_frame, text="Cancel", command=lambda: self.cancel_action(self.edit_task_frame), state=NORMAL)
        self.cancel.grid(row=10, column=1)
    
    def save_changes(self):
        """Asks user if they are certain of saving the changes"""
        # Obtaining edited values
        new_title = self.edited_title_entry.get()
        new_desc = self.edited_desc_entry.get()
        completion_status = bool(self.complete_var.get())
        new_priority = self.edited_priority_value.get()
        
        if askyesno("Verify", "Are you sure you want to save this task? You cannot undo this action."):
            if len(new_desc) >= 52: # Ensuring user enters a description less than 52 characters
                showerror("Description Error", "The description must be less than 52 characters.")
            elif completion_status == True: # If the task is complete, delete
                showinfo("Completed Task", "Task marked as completed. Now deleting from treeview.")
                self.selected_task.delete(self.db)
                self.tree.delete(self.task_id)
            else:
                showinfo("Yes", "Changes updated. Redirecting you back to course overview.")
                self.selected_task.update(self.db, new_title, new_desc, completion_status, priority=new_priority)
            self.app.change_page(0)
            self.curr_frame.destroy()
        else:
            showinfo("No", "Task has NOT been deleted.")
    
    def delete_task_hander(self):
        """Asks user if they are certain of deleting the task. If yes, task is deleted from database and treeview."""
        if askyesno("Verify", "Are you sure you want to delete this task? You cannot undo this action."):
            showinfo("Yes", "Task Deleted.")
            self.selected_task.delete(self.db)
            self.tree.delete(self.task_id)
        else:
            showinfo("No", "Task has NOT been deleted.")
    
    def submit_action(self):    
        # Obtaining user info    
        self.title = self.task_title_entry.get()
        self.description = self.task_desc_entry.get()
        self.priority = self.task_priority_value.get()

        course_id = -1
        for course in Course.get_all_courses(self.app.db):
            if course.course_name == self.task_course_selection.get():
                course_id = course.course_id
                break
            
        # Error handling to ensure user enters in a description less than 56 characters
        if course_id == -1:
            showerror("Error", "Invalid course selected.")
            return
        if len(self.description) <= 52:
            self.add_task = Task.create_task(self.db, self.title, self.description, 0, course_id, self.priority)
            # self.tree.insert("", "end", values=(self.title, self.description, False, self.course_name, self.priority))
            showinfo("Task Created", "Task creation success.")
            self.app.change_page(0)
            self.curr_frame.destroy()
        else:
            showerror("Error", "Please ensure your description is less than 52 characters.")
    
    def cancel_action(self, frame):
        """Prompts user if they are certain of cancelling task entry."""
        if askyesno("Verify", "Are you sure you want to cancel?"):
            showinfo("Yes", "Redirecting you back to course overview.")
            frame.destroy()
            self.app.change_page(0)

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
            showinfo("Yes", "Redirecting you back to course overview.")
            self.app.change_page(0)
        else:
            # Maintaining entry box to prevent it disappearing after the user selects 
            self.course_name_entry.insert(0, user_course)
            