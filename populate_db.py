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
    Task.create_task(db, "Project 1", "Desc 1 ", False, course_1.course_id, 1)
    Task.create_task(db, "Project 2", "Desc2", False, course_1.course_id, 3)

    course_2 = Course.create_course(db, "CCT212")
    Task.create_task(db, "Term Paper pt. 1", "Desc 3", False, course_2.course_id, 1)
    Task.create_task(db, "Term Paper pt. 2", "Desc 4", False, course_2.course_id, 2)


if __name__ == "__main__":
    populate_db()
    