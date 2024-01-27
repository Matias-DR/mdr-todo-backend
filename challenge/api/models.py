from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''
        Entity/Model for the users

        Attributes:
            email (str): User's email.
            first_name (str): User's first name.
            last_name (str): User's last name.
            password (str): User's password.
            username (str): User's username.
    '''

    def __str__(self):
        return f'Username: {self.username}\n'


class Task(models.Model):
    '''
        Entity/Model for the tasks

        Attributes:
            completed (bool): Determines if the user marked the task as completed.
            description (str): User-entered descriptive colloquial text for the task.
            title (str): Title of the task.
            user (django.contrib.auth.models.User): Task owner.
    '''

    completed = models.BooleanField(default=False)
    description = models.TextField()
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Title: {self.title}.\nUser: {self.user.__str__()}\n\n'
