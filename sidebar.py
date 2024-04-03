from tkinter import *

from models import Sqlite_Db
from pages import Page

class SidebarButton(Button):
    """An individual sidebar button"""
    db: Sqlite_Db

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = parent.app

class Sidebar(Frame):
    """The sidebar class, containing menu buttons to change pages"""
    db: Sqlite_Db

    def __init__(self, parent, pages: list[Page], change_page, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = parent
        self.change_page = change_page
        
        for i in range(len(pages)):
            page = pages[i]
            SidebarButton(self, text=page.page_name, command=lambda index=i: self.change_page(index)).pack(side=TOP, fill=X)
    
    def update_pages(self, pages):
        # Clear existing buttons to update sidebar with new course pages
        for widget in self.winfo_children():
            widget.destroy()

        # Add buttons for the new pages starting from the current number of buttons
        for i in range(len(pages)):
            page = pages[i]
            SidebarButton(self, text=page.page_name, command=lambda index=i: self.change_page(index)).pack(side=TOP, fill=X)
            
            