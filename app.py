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
        self.geometry("950x600")
        # Preventing resizing of window, adapted from 
        # https://www.tutorialspoint.com/how-can-i-prevent-a-window-from-being-resized-with-tkinter#:~:text=Tkinter%20windows%20can%20be%20resized,resizable(boolean%20value)%20method.
        self.resizable(False, False)

        self.page_frame = Frame(self)
        self.page_frame.app = self

        self.pages: list[Page] = [
            OverviewPage(self.page_frame), 
        ]

        for course in Course.get_all_courses(self.db):
            self.pages.append(CoursePage(self.page_frame, course))
        
        self.pages.append(NewCourse(self.page_frame))

        for page in self.pages:
            page.grid(row=0, column=0, sticky="nsew")

        self.sidebar = Sidebar(self, self.pages) # changed bg colours
        self.sidebar.pack(side=LEFT, fill="y")

        self.page_frame.pack(side=RIGHT, expand=True, fill="both")
        
        self.change_page(0)
        self.create_menu()

    def change_page(self, page_index):
        page = self.pages[page_index]
        page.tkraise()
        if isinstance(page, Page):
            page.tree.delete(*page.tree.get_children())
            if isinstance(page, CoursePage):
                page.populate_by_course(page.course)
            else:
                page.populate_all_tasks()
        print("changing pages:", page_index)
        
    def add_page(self, course):
        """Adding a new page and updating sidebar when course is created, takes a Course object as input"""
        # Indexing the position to ensure insertion comes before the add course button
        new_course_page = CoursePage(self.page_frame, course)
        index = len(self.pages) - 1
        self.pages.insert(index, new_course_page)
        new_course_page.grid(row=0, column=0, sticky="nsew")

        self.sidebar.update_pages(self.pages)
        print(f"added new course: {course.course_name}")

    def delete_page(self, index):
        """Deletes a page by deleting the course and removing it from the menu"""
        print("deleting page:", index)
        page = self.pages[index]
        if askyesno("Delete Course", f"Are you sure you want to delete course {page.course.course_name}?\n\nThis will also delete all tasks associated with this course."):
            page.course.delete(self.db)
            self.pages.pop(index)
            page.destroy()

            self.sidebar.update_pages(self.pages)
    
    def create_menu(self):
        """Creating a menu bar for user to choose from a variety of actions"""
        # Initializing main menu bar
        menubar = Menu(self)
        main_menu = Menu(menubar, tearoff=0)
        
        # Actions menu
        menubar.add_cascade(label="Actions", menu=main_menu)
        main_menu.add_command(label="Quit", command=self.user_quit)
        
        # Display menu
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
