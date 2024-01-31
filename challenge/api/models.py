import logging

from django.contrib.auth.models import AbstractUser
from django.db.models import (
    Model,
    BooleanField,
    TextField,
    CharField,
    ForeignKey,
    DateField,
    CASCADE
)


logger = logging.getLogger(__name__)


class User(AbstractUser):
    '''
        Entity/Model for the users

        Attributes:
            password (str): User's password.
            username (str): User's username.
    '''

    def __str__(self) -> str:
        return f'Username: {self.username}'


class Task(Model):
    '''
        Entity/Model for the tasks

        Attributes:
            completed (bool): Determines if the user marked the task as completed.
            description (str): User-entered descriptive colloquial text for the task.
            title (str): Title of the task.
            user (django.contrib.auth.models.User): Task owner.
            created (datetime.datetime): Date and time of task creation.
    '''

    completed = BooleanField(default=False)
    description = TextField()
    title = CharField(max_length=100)
    user = ForeignKey(User, on_delete=CASCADE)
    created = DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Title: {self.title}. {self.user.__str__()}'

    def complete(
        self,
        save: bool = True
    ) -> None:
        '''
            Marks the task as complete.

            Args:
                save (bool): Determines if the task is saved in the database.
        '''

        logger.info(f'Task complete -> Task {self.pk} completed.')
        self.completed = True
        if (save):
            self.save()

    def incomplete(
        self,
        save: bool = True
    ) -> None:
        '''
            Marks the task as incomplete.

            Args:
                save (bool): Determines if the task is saved in the database.
        '''

        logger.info(f'Task incomplete -> Task {self.pk} incomplete.')
        self.completed = False
        if (save):
            self.save()
