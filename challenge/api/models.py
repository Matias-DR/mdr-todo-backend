from django.contrib.auth.models import User
from django.db import models


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
