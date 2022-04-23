import os
import uuid

from django.db import models
from account.models import User


def get_file_path_post(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('support', filename)


class Support(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='supports',
                             null=True)
    HURT_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No')
    )
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField()
    place = models.CharField(max_length=100)
    is_hurted = models.CharField(choices=HURT_CHOICES, max_length=5)
    photo = models.ImageField(upload_to=get_file_path_post, blank=True, null=True)

    def __str__(self):
        return self.title
