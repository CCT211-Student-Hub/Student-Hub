from tkinter import *

class Page(Frame):
    """An abstract class representing a page. Implemented as an overview page or course page"""
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)


class OverviewPage(Page):
    """The page that shows all tasks, sorted by date"""
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)


class CoursePage(Page):
    """The page that shows all tasks for a given course, sorted by date"""
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)