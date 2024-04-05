from tkinter import *
from sys import platform

from models import Sqlite_Db
from pages import CoursePage, Page

class SidebarButton(Button):
    """An individual sidebar button"""
    db: Sqlite_Db

    def __init__(self, parent, page, index, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = parent.app

        self.config(text=page.page_name, command=lambda i=index: self.app.change_page(i))

        if isinstance(page, CoursePage):
            # Context menu adapted from: https://www.geeksforgeeks.org/right-click-menu-using-tkinter/
            context_menu = Menu(self, tearoff=0)
            context_menu.add_command(label="Delete Course", command=lambda i=index: self.app.delete_page(i))

            def do_popup(event): 
                try: 
                    context_menu.tk_popup(event.x_root, event.y_root) 
                finally: 
                    context_menu.grab_release() 
            
            if platform == "darwin":
                self.bind("<Button-2>", do_popup)
            else:
                self.bind("<Button-3>", do_popup)

class Sidebar(Frame):
    """The sidebar class, containing menu buttons to change pages"""
    db: Sqlite_Db

    def __init__(self, parent, pages: list[Page], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = parent
        
        for i in range(len(pages)):
            page = pages[i]
            btn = SidebarButton(self, page, i)
            btn.pack(side=TOP, fill=X)
            
    
    def update_pages(self, pages):
        # Clear existing buttons to update sidebar with new course pages
        for widget in self.winfo_children():
            widget.destroy()

        # Add buttons for the new pages starting from the current number of buttons
        for i in range(len(pages)):
            page = pages[i]
            btn = SidebarButton(self, page, i)
            btn.pack(side=TOP, fill=X)
            