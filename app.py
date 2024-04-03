from tkinter import *
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

    def change_page(self, page_index):
        self.pages[page_index].tkraise()
        print("changing pages:", page_index)
        
    def add_page(self, course_name):
        # indexing the position to ensure insertion comes before the add course button
        new_course_page = CoursePage(self.page_frame, course_name)
        index = len(self.pages) - 1
        self.pages.insert(index, new_course_page)
            
        self.sidebar.update_pages(self.pages)
        print(f"added new course: {course_name}")
        
        
if __name__ == "__main__":
    root = App()
    root.mainloop()
