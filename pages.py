from tkinter import *
from tkinter.messagebox import *
from tkinter import font as tkfont
from models import Sqlite_Db, Task, Course

class Page(Frame):
    """An abstract class representing a page. Implemented as an overview page or course page"""
    db: Sqlite_Db
    page_name: str

    def __init__(self, parent, *args, **kwargs):
        self.app = parent.app
        super().__init__(parent, *args, **kwargs, bg="pink")

        self.page_name = "Page"
        # title font
        self.title_font = tkfont.Font(family='Montserrat', size=18, weight="bold")

class OverviewPage(Page):
    """The page that shows all tasks, sorted by date"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.page_name = "Overview"
        self.label = Label(self, text=self.page_name, font=self.title_font)
        self.label.grid(row=0, column=0)

    def get(self):
        return self.dataentry.get()

class CoursePage(Page):
    """The page that shows all tasks for a given course, sorted by date"""
    def __init__(self, parent, course_name, *args, **kwargs):
        """Takes a `course_name` which is set as the page name"""
        super().__init__(parent, *args, **kwargs)

        self.page_name = course_name
        self.label = Label(self, text=self.page_name, font=self.title_font)
        self.label.grid(row=0, column=0)

class NewCourse(Page):
    """The page that provides form to create a new course"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.page_name = "Create New Course"
        self.label = Label(self, text=self.page_name, font=self.title_font).grid(row=0, column=0)
        
        # entry forms for relevant data
        self.course_name = Label(self, text="Course Name").grid(row=3, column=0)
        self.course_name_entry = Entry(self)
        self.course_name_entry.grid(row=3, column = 1)
        
        self.submit = Button(self, text="Submit", command = self.submit_creation).grid(row=5, column = 0)
        self.cancel = Button(self, text="Cancel", command=self.cancel_creation).grid(row=5, column=1)
            
    def submit_creation(self):
        """Submits valid user input as a course in the sidebar and redirects them to the new course page"""
        user_course = self.course_name_entry.get()
        if len(user_course) == 0:
            # adapted from https://docs.python.org/3/library/tkinter.messagebox.html
            showerror(title="Error: Empty Course", message="Please enter a course name.")
        else:
            Course.create_course(self.app.db, course_name=user_course)
            self.app.add_page(course_name=user_course)
            
            # redirecting user to new page
            # self.app.change_page(len(self.app.pages)-2)
            
            # clearing text in entry box adapted from
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

            

        