from __future__ import annotations

class Task:
    """A model that represents a task"""
    def __init__(self) -> None:
        self.task_id = 1

    def get_all_tasks() -> list[Task]:
        """Retrieves a user's tasks"""
        # TODO
        pass


    def get_tasks_by_course(course_code: str) -> list[Task]:
        """Retrieves a user's tasks from a given course code"""
        # TODO
        pass


    def create_task(course_code: str) -> Task:
        """Create a task and enter into database"""
        # TODO
        pass


    def update_task(task_id: str) -> Task:
        """Update a task that already exists"""
        # TODO
        pass


    def delete_task(task_id: str) -> bool:
        """Delete a task from the database"""
        # TODO
        pass



class Course:
    """A model that represents a course"""

    def get_all_courses() -> list[Course]:
        """Retrieves a user's courses"""
        # TODO
        pass


    def create_course(course_name: str) -> Course:
        """Create a course and enter into database"""
        # TODO
        pass


    def update_course(course_code: str) -> Course:
        """Update a course that already exists"""
        # TODO
        pass


    def delete_course(course_code: str) -> bool:
        """Delete a course from the database"""
        # TODO
        pass
