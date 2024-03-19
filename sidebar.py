from tkinter import *

from pages import Page

class SidebarButton(Button):
    """An individual sidebar button"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Sidebar(Frame):
    """The sidebar class, containing menu buttons to change pages"""
    def __init__(self, parent, pages: list[Page], change_page, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        for i in range(len(pages)):
            page = pages[i]
            SidebarButton(self, text=page.page_name, command=lambda index=i: change_page(index)).pack(side=TOP)
