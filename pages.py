from tkinter import *

from models import Sqlite_Db, Task

class Page(Frame):
    """An abstract class representing a page. Implemented as an overview page or course page"""
    db: Sqlite_Db
    page_name: str

    def __init__(self, parent, *args, **kwargs):
        self.db = parent.db
        super().__init__(parent, *args, **kwargs, bg="pink")

        self.page_name = "Page"


class OverviewPage(Page):
    """The page that shows all tasks, sorted by date"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.page_name = "Overview"
        self.label = Label(self, text=self.page_name)
        self.label.pack()


class CoursePage(Page):
    """The page that shows all tasks for a given course, sorted by date"""
    def __init__(self, parent, course_name, *args, **kwargs):
        """Takes a `course_name` which is set as the page name"""
        super().__init__(parent, *args, **kwargs)

        self.page_name = course_name
        self.label = Label(self, text=self.page_name)
        self.label.pack()
