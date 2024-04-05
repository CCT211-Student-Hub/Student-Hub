"""A script that populates the sqlite database with sample tasks and course
NOTE: This script deletes the existing database. Use with caution
"""

import os
from models import Course, Sqlite_Db, Task

def populate_db():
    # Remove existing database
    os.remove("student_hub.db")

    db = Sqlite_Db()

    course_1 = Course.create_course(db, "CCT211")
    Task.create_task(db, "Project 1", "This assignment focuses on the design, implementation and testing of a Python program to allow the user to play an arcade-style action or platformer game. This game will leverage the strengths of the Pygame library. ", False, course_1.course_id, 1)
    Task.create_task(db, "Project 2", "Project 2 is a creative exercise where students are expected to take what they have learned about Python and create a simple GUI application with a persistence layer.The core of the project should be a Tkinter GUI form that provides basic CRUD persistent functionality in the context of your choice. ", False, course_1.course_id, 3)

    course_2 = Course.create_course(db, "CCT212")
    Task.create_task(db, "Term Paper pt. 1", "This is part 1 of your final essay assignment for this course. For this assignment, you need to provide an abstract and annotated bibliography of your proposed final term paper. The purpose of this assignment is to get you to begin putting together a paper based on one of the four units of the course: The History of Hacking, Hacking In Popular Culture, Free and Open Source Software, and Hacking and Capitalism. In this assignment you’ll learn how to put together a proper summary of a proposed paper, locate relevant sources, and how to discuss those sources in a critical way. The essay you will be writing will be argumentative and critical. It is not just a summary or description of events, but offers an argument with an actual thesis statement. ", False, course_2.course_id, 1)
    Task.create_task(db, "Term Paper pt. 2", "In part 2 of your final term paper assignment you will be writing a critical essay based on the abstract and annotated bibliography that you submitted for term paper part 1. This assignment should be in proper essay format, with an introduction, a clear thesis statement, argumentative paragraphs, and a proper conclusion. Your essay should be based on the abstract and sources you submitted for part 1, but you can make changes based on the feedback you received from part 1. You are also allowed to add additional sources as long as they are reputable, reliable, and relevant to your topic. Do not completely change your topic - instead make any necessary changes or edits based on how you did on part 1 in order to have a strong final essay. ", False, course_2.course_id, 2)


if __name__ == "__main__":
    populate_db()
    