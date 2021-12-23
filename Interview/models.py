from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True

class Interview(models.Model):
    participants = models.ManyToManyField(User , related_name='participants')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # def __str__(self):
    #     s = ""
    #     for participant in self.participants.all():
    #         s += participant.username + " "
    #     return s