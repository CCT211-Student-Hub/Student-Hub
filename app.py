from tkinter import *
from tkinter.messagebox import *
from models import Course, Sqlite_Db
from sidebar import Sidebar
from pages import Page, OverviewPage, CoursePage, NewCourse

class App(Tk):
    """The root application class"""
    def __init__(self):
        super().__init__()

        self.db = Sqlite_Db()

        self.title = "Student Hub"
        self.geometry("1150x600")

        self.page_frame = Frame(self, bg="gray33") # changed bg colours
        self.page_frame.app = self

        self.pages: list[Page] = [
            OverviewPage(self.page_frame), 
        ]

        for course in Course.get_all_courses(self.db):
            self.pages.append(CoursePage(self.page_frame, course.course_name))
        
        self.pages.append(NewCourse(self.page_frame))

        for page in self.pages:
            page.grid(row=0, column=0, sticky="nsew")

        self.sidebar = Sidebar(self, self.pages, self.change_page) # changed bg colours
        self.sidebar.pack(side=LEFT, fill="y")

        self.page_frame.pack(side=RIGHT, expand=True, fill="both")
        
        self.change_page(0)
        self.create_menu()

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
        
if __name__ == "__main__":
    root = App()
    root.mainloop()
