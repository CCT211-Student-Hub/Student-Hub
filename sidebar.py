from tkinter import *

class SidebarButton(Button):
    """An individual sidebar button"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Sidebar(Frame):
    """The sidebar class, containing menu buttons to change pages"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        button = SidebarButton(self, text="Overview")
        button.pack(side=TOP)

        courses_label = Label(text="Courses")
        courses_label.pack(side=TOP)

        course_btn = SidebarButton(self, text="Course 1")
        course_btn.pack(side=TOP)
        
        