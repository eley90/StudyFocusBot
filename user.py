"""
Authors: Daniela Cislaru, Elmira Moayedi
"""

__author__ = 'Daniela Cislaru, Elmira Moayedi'


from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.db')
Base = declarative_base()
Session = sessionmaker(engine)
session = Session()


class User(Base):
    """
    Represents a user in the system.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', String)
    user_name = Column('user_name', String)
    user_credit_points = Column('user_credit_points', Float, default=10)
    tasks = relationship('Task', back_populates="user")
    achievements = relationship("Achievement", back_populates="user")
    completed_tasks = Column(Integer, default=0)

    def __init__(self, user_name, user_id, user_credit_points=10, tasks=None, comp_tasks=0, achievements=None):
        """
        Initializes a User object with the provided parameters.

        Args:
            user_name (str): The user's name.
            user_id (str): The user's unique identifier.
            user_credit_points (float, optional): The user's credit points. Defaults to 10.
            tasks (list[Task], optional): List of tasks associated with the user. Defaults to None.
            comp_tasks (int, optional): The number of completed tasks. Defaults to 0.
            achievements (list[Achievement], optional): List of achievements associated with the user. Defaults to None.
        """
        super().__init__()
        self.user_name = user_name.split('#')[0]
        self.user_id = user_id
        self.user_credit_points = user_credit_points  # 10
        self.achievements = achievements or []
        self.tasks = tasks or []  # len(self.tasks)
        self.comp_tasks = comp_tasks

    def update_credit_points(self):
        """
        Updates the user's credit points by decrementing it by 1 if it's greater than 0.
        If the credit points are already 0, no change is made.

        After updating, the changes are committed to the session.

        """
        if self.user_credit_points > 0:
            self.user_credit_points -= 1
        else:
            self.user_credit_points = 0
        session.add(self)
        session.commit()

    def __repr__(self):
        """
           Returns a string representation of the User object.

           Returns:
               str: A formatted string representing the User object with its name and ID.
        """
        return '{} - {}'.format(self.user_name, self.user_id)

    def update_tasks(self, task_name, study_session):

        """
        Updates the user's tasks by adding a new task to the list of tasks.

        Args:
            task_name (str): The name of the task to be added.
            study_session (StudySession): The study session associated with the task.

        """
        task_db = session.query(Task).filter(Task.name == task_name).filter(
            Task.study_session_id == study_session.id).filter(Task.user_id == self.user_id).one_or_none()
        if not task_db:
            new_task = Task(name=task_name, user=self, study_session=study_session)
            self.tasks.append(new_task)
            session.add(new_task)
            session.commit()

    def delete_task(self, task_name, study_session):
        """
        Deletes a task associated with the user and a specific study session.

        Args:
            task_name (str): The name of the task to be deleted.
            study_session (StudySession): The study session associated with the task.

        Returns:
            str: A message indicating whether the task was successfully deleted or not.

        """
        task_db_to_delete = session.query(Task).filter(Task.name == task_name).filter(
            Task.study_session_id == study_session.id).filter(Task.user_id == self.user_id).one_or_none()
        if task_db_to_delete:
            self.tasks.remove(task_db_to_delete)
            return f"{task_name} was successfuly deleted"
        else:
            return f"{task_name} was not found"

    def calculate_points(self, study_session):
        """
            Calculate the points for the user based on completed tasks in a study session.

            Args:
                study_session: The study session for which to calculate the points.

            Returns:
                If the user has completed tasks in the study session and the number of completed tasks is less than or equal to
                the total tasks in the study session, it returns the calculated points. If the number of completed tasks exceeds
                the total tasks in the study session, it returns an error message. Otherwise, it returns 0.

        """
        num_of_tasks = [task for task in self.tasks if task.study_session == study_session]
        if len(num_of_tasks) > 0 and self.comp_tasks <= len(num_of_tasks):
            value = (self.comp_tasks / len(num_of_tasks)) * (self.user_credit_points / 10) * 100
            print(self.comp_tasks)
            achievement = Achievement(value=value, user=self, study_session=study_session)
            self.achievements.append(achievement)
            session.add(achievement)
            session.commit()
            return value
        elif self.comp_tasks > len(num_of_tasks):
            return "You can not have done so many tasks"
        else:
            return 0


class StudySession(Base):
    """
    Represents a study session in the system.
    """
    __tablename__ = 'study_sessions'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    task = relationship("Task", back_populates='study_session')
    achievement = relationship("Achievement", back_populates='study_session')


class Task(Base):
    """
    Represents a task associated with a user in the system.
    """
    __tablename__ = 'user_tasks'
    tid = Column('task_id', Integer, primary_key=True)
    name = Column('name', String)
    user_id = Column('user_owner', ForeignKey('users.user_id'))
    user = relationship("User", back_populates="tasks")
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"))
    study_session = relationship("StudySession", back_populates="task")

    def __init__(self, name, user, study_session):
        """
        Initializes a Task object with the provided parameters.

        Args:
            name (str): The name of the task.
            user (User): The user associated with the task.
            study_session (StudySession): The study session associated with the task.
        """
        self.name = name
        self.user = user
        self.study_session = study_session

    def __repr__(self):
        """
        Returns a string representation of the Task object.

        Returns:
            str: A formatted string representing the Task object with its name and associated user.
        """
        return "Task (name='%s', user='%s')" % (self.name, self.user)


class Achievement(Base):
    """
    Represents an achievement in the system.
    """
    __tablename__ = 'achievements'
    id = Column(Integer, primary_key=True)
    value = Column('credit_point', Float)
    user_id = Column('user', Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="achievements")
    study_session_id = Column(Integer, ForeignKey('study_sessions.id'))
    study_session = relationship("StudySession", back_populates='achievement')

    def __init__(self, value, user, study_session):
        """
        Initializes an Achievement object with the provided parameters.

        Args:
            value (float): The value or credit points associated with the achievement.
            user (User): The user associated with the achievement.
            study_session (StudySession): The study session associated with the achievement.
        """
        self.time_saved = datetime.utcnow()
        self.value = value
        self.user = user
        self.study_session = study_session

    def __repr__(self):
        return "<Achievement(time='%s', value='%d', user='%s')>" % (self.time_saved, self.value, self.user)


Base.metadata.create_all(engine)

