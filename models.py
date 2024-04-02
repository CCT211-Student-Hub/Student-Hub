from __future__ import annotations
import sqlite3
from typing import Optional

db_path = "student_hub.db"

class Sqlite_Db:
    """A class that handles connections to the database"""
    con: sqlite3.Connection

    def __init__(self) -> None:
        # connect to db
        self.con = sqlite3.connect(db_path)
        self.con.execute("PRAGMA foreign_keys = 1")
        cur = self.con.cursor()

        # initialize db
        cur.execute("""
                         CREATE TABLE IF NOT EXISTS course (
                            course_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                            course_name TEXT NOT NULL
                         );
                         """)
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS task (
                            task_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                            title       TEXT NOT NULL,
                            description TEXT NOT NULL,
                            completed   INTEGER NOT NULL DEFAULT 0,
                            course_id   INTEGER NOT NULL,
                            FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE
                        );
                        """)


class Task:
    """A model that represents a task
    
    Instance methods:
        task.update() - Updates the task
        task.delete() - Deletes the task

    Static methods:
        Task.get_task() - Gets a task by task_id
        Task.get_all_tasks() - Gets all tasks
        Task.get_tasks_by_course() - Gets all tasks of a given course
        Task.create_task() - Creates a new task
    """
    task_id: int
    title: str
    description: str
    completed: bool
    course_id: int

    def __init__(self, task_id: int, title: str, description: str, completed: bool, course_id: int) -> None:
        self.task_id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.course_id = course_id

    def update(self, db: Sqlite_Db, title: str=None, description:str=None, completed:bool=None, course_id:int=None):
        """Update a task that already exists"""
        if title is None: title = self.title
        if description is None: description = self.description
        if completed is None: completed = self.completed
        if course_id is None: course_id = self.course_id
        cur = db.con.cursor()
        cur.execute("UPDATE task SET title=?, description=?, completed=?, course_id=? WHERE task_id=?;", (title, description, int(completed), course_id, self.task_id))
        db.con.commit()
        self.title = title
        self.description = description
        self.completed = completed
        self.course_id = course_id

    def delete(self, db: Sqlite_Db):
        """Delete a task from the database"""
        cur = db.con.cursor()
        cur.execute("DELETE FROM task WHERE task_id=?;", (self.task_id,))
        db.con.commit()

    def get_task(db: Sqlite_Db, task_id: int) -> Optional[Task]:
        """Retrieves a task by task_id. Returns the task"""
        cur = db.con.cursor()
        res = cur.execute("SELECT task_id, title, description, completed, course_id FROM task WHERE task_id=?;", (task_id, ))
        result = res.fetchone()
        if result is None:
            return None
        task = Task(result[0], result[1], result[2], bool(result[3]), result[4])
        return task
        
    def get_all_tasks(db: Sqlite_Db) -> list[Task]:
        """Retrieves a user's tasks. Returns a list of Task objects"""
        cur = db.con.cursor()
        res = cur.execute("SELECT task_id, title, description, completed, course_id FROM task;")
        results = res.fetchall()
        tasks = []
        for task in results:
            tasks.append(Task(task[0], task[1], task[2], bool(task[3]), task[4]))
        return tasks

    def get_tasks_by_course(db: Sqlite_Db, course_id: int) -> list[Task]:
        """Retrieves a user's tasks from a given course id"""
        cur = db.con.cursor()
        res = cur.execute("SELECT task_id, title, description, completed, course_id FROM task WHERE course_id = ?;", (course_id, ))
        results = res.fetchall()
        tasks = []
        for task in results:
            tasks.append(Task(task[0], task[1], task[2], bool(task[3]), task[4]))
        return tasks

    def create_task(db: Sqlite_Db, title, description, completed, course_id) -> Task:
        """Create a task and enter into database. Returns the task_id of the task"""
        cur = db.con.cursor()
        cur.execute("INSERT INTO task (title, description, completed, course_id) VALUES (?, ?, ?, ?);", (title, description, int(completed), course_id))
        db.con.commit()
        return Task.get_task(db, cur.lastrowid)


class Course:
    """A model that represents a course

    Instance methods:
        course.update() - Updates the course
        course.delete() - Deletes the course

    Static methods:
        Course.get_course() - Gets a course by course_id
        Course.get_all_courses() - Gets all courses
        Course.create_course() - Creates a new course
    """
    course_id: int
    course_name: str

    def __init__(self, course_id: int, course_name: str) -> None:
        self.course_id = course_id
        self.course_name = course_name

    def update(self, db: Sqlite_Db, course_name: str=None):
        """Update a course that already exists"""
        if course_name is None: course_name = self.course_name
        cur = db.con.cursor()
        cur.execute("UPDATE course SET course_name=? WHERE course_id=?;", (course_name, self.course_id))
        db.con.commit()
        self.course_name = course_name

    def delete(self, db: Sqlite_Db) -> bool:
        """Delete a course from the database"""
        cur = db.con.cursor()
        cur.execute("DELETE FROM course WHERE course_id=?;", (self.course_id,))
        db.con.commit()

    def get_all_courses(db: Sqlite_Db) -> list[Course]:
        """Retrieves a user's courses"""
        cur = db.con.cursor()
        res = cur.execute("SELECT course_id, course_name FROM course;")
        results = res.fetchall()
        courses = []
        for course in results:
            courses.append(Course(course[0], course[1]))
        return courses

    def get_course(db: Sqlite_Db, course_id: int) -> Optional[Course]:
        """Retrieves a single course by course_id"""
        cur = db.con.cursor()
        res = cur.execute("SELECT course_id, course_name FROM course WHERE course_id = ?;", (course_id, ))
        result = res.fetchone()
        if result is None:
            return None
        course = Course(result[0], result[1])
        return course

    def create_course(db: Sqlite_Db, course_name: str) -> Course:
        """Create a course and enter into database. Returns the course_id of the course"""
        cur = db.con.cursor()
        cur.execute("INSERT INTO course (course_name) VALUES (?);", (course_name,))
        db.con.commit()
        return Course.get_course(db, cur.lastrowid)
