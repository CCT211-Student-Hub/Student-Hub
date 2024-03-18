from tkinter import *
from sidebar import Sidebar

from pages import Page, OverviewPage, CoursePage

class App(Tk):
    """The root application class"""
    def __init__(self):
        super().__init__()
        self.title = "Student Hub"
        self.geometry("800x600")

        self.sidebar = Sidebar(self, bg="red")
        self.sidebar.pack(side=LEFT, fill="y")

        self.page_frame = Frame()
        self.pages = {}
        for page in (OverviewPage, CoursePage):
            self.pages[page] = page()

        self.change_page(OverviewPage)

    def change_page(self, page: Page):
        self.pages[page].tkraise()



if __name__ == "__main__":
    root = App()
    root.mainloop()
