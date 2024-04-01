from tkinter import *

from models import Sqlite_Db
from sidebar import Sidebar
from pages import Page, OverviewPage, CoursePage

class App(Tk):
    """The root application class"""
    def __init__(self):
        super().__init__()

        self.db = Sqlite_Db()

        self.title = "Student Hub"
        self.geometry("800x600")

        self.page_frame = Frame(self, bg="blue")
        self.page_frame.db = self.db

        self.pages: list[Page] = [
            OverviewPage(self.page_frame), 
            CoursePage(self.page_frame, "CCT211"), 
            CoursePage(self.page_frame, "CCT212")
        ]

        for page in self.pages:
            page.grid(row=0, column=0, sticky="nsew")

        self.sidebar = Sidebar(self, self.pages, self.change_page, bg="red")
        self.sidebar.pack(side=LEFT, fill="y")

        self.page_frame.pack(side=RIGHT, expand=True, fill="both")

        self.change_page(0)

    def change_page(self, page_index):
        self.pages[page_index].tkraise()
        print("changing pages:", page_index)



if __name__ == "__main__":
    root = App()
    root.mainloop()
