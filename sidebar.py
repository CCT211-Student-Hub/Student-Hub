from tkinter import *

from models import Sqlite_Db
from pages import Page

class SidebarButton(Button):
    """An individual sidebar button"""
    db: Sqlite_Db

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.db = parent.db

class Sidebar(Frame):
    """The sidebar class, containing menu buttons to change pages"""
    db: Sqlite_Db

    def __init__(self, parent, pages: list[Page], change_page, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.db = parent.db

        for i in range(len(pages)):
            page = pages[i]
            SidebarButton(self, text=page.page_name, command=lambda index=i: change_page(index)).pack(side=TOP)
