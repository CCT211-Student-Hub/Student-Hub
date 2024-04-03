from tkinter import *
from tkinter.messagebox import *
import tkinter.ttk as ttk
import sqlite3
from models import Course, Sqlite_Db
from sidebar import Sidebar
from pages import Page, OverviewPage, CoursePage, NewCourse

class App(Tk):
    """The root application class"""
    def __init__(self):
        super().__init__()

        self.db = Sqlite_Db()

        self.title = "Student Hub"
        self.geometry("800x600")

        self.page_frame = Frame(self, bg="gray88") # changed bg colours
        self.page_frame.app = self

        self.pages: list[Page] = [
            OverviewPage(self.page_frame), 
        ]

        for course in Course.get_all_courses(self.db):
            self.pages.append(CoursePage(self.page_frame, course.course_name))
        
        self.pages.append(NewCourse(self.page_frame))

        for page in self.pages:
            page.grid(row=0, column=0, sticky="nsew")

        self.sidebar = Sidebar(self, self.pages, self.change_page, bg="gray33") # changed bg colours
        self.sidebar.pack(side=LEFT, fill="y")

        self.page_frame.pack(side=RIGHT, expand=True, fill="both")
        
        self.change_page(0)
        self.create_menu()
        self.display_data()
        self.populate_widgets()

    def change_page(self, page_index):
        self.pages[page_index].tkraise()
        print("changing pages:", page_index)
        
    def add_page(self, course_name):
        """Adding a new page and updating sidebar when course is created"""
        # indexing the position to ensure insertion comes before the add course button
        new_course_page = CoursePage(self.page_frame, course_name)
        index = len(self.pages) - 1
        self.pages.insert(index, new_course_page)
        self.sidebar.update_pages(self.pages)
        print(f"added new course: {course_name}")
    
    def create_menu(self):
        """Creating a menu bar for user to choose from a variety of actions"""
        # initializing main menu bar
        menubar = Menu(self)
        main_menu = Menu(menubar, tearoff=0)
        
        # actions menu
        menubar.add_cascade(label="Actions", menu=main_menu)
        main_menu.add_command(label="Quit", command=self.user_quit)
        
        # display menu
        self.config(menu=menubar)
    
    def user_quit(self):
        """Prompting users with a warning message if they decide to quit the application"""
        if askyesno("Verify", "Are you sure you want to exit the application?"):
            showwarning("Yes", "Goodbye. Closing Student Hub.")
            exit()
        else:
            showinfo("No", "Redirecting you back to Student Hub.")
            
    def display_data(self):
        """Displays and sets up treeview for course tasks"""
        # set up the treeview
        self.tree = ttk.Treeview(self.page_frame, columns=("task id", "description", "completed"), height=10, selectmode="extended")
        # self.tree.heading("course name", text="Course Name", anchor=W)
        self.tree.heading("task id", text="Task ID", anchor=W)
        self.tree.heading("description", text="Description", anchor=W)
        self.tree.heading("completed", text="Completed", anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=200)
        self.tree.column('#2', stretch=NO, minwidth=0, width=200)
        self.tree.grid(row=1, column=0, sticky="nsew", padx=(20, 20), pady=(0, 80))

        # configuring vertical scrollbar
        scrollbary = Scrollbar(self.page_frame, orient=VERTICAL, command=self.tree.yview)
        scrollbary.grid(row=1, column=1, sticky="ns")
        self.tree.config(yscrollcommand=scrollbary.set)

        # configuring horizontal scrollbar
        scrollbarx = Scrollbar(self.page_frame, orient=HORIZONTAL, command=self.tree.xview)
        scrollbarx.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.tree.config(xscrollcommand=scrollbarx.set)
        
        # configuring page frame to accomodate the treeview and scrollbars
        self.page_frame.rowconfigure(1, weight=1) 
        self.page_frame.columnconfigure(0, weight=1) 
        
    def populate_widgets(self):
        """Populating treeview with data from SQLite Database"""
        
        # populate the treeview from a csv
        conn = sqlite3.connect("student_hub.db")
        c = conn.cursor()
        c.execute("SELECT task_id, title, description, completed FROM task ORDER BY task_id")
        task_info = c.fetchall()
        
        for row in task_info:
            self.tree.insert("", "end", values=row)        
        
if __name__ == "__main__":
    root = App()
    root.mainloop()
