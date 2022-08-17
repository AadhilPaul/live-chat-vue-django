from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
import random
import string

# Create your models here.


def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break

    return code


class Room(models.Model):
    code = models.CharField(
        max_length=8, default=generate_unique_code, unique=True)
    member = models.ManyToManyField(
        User, related_name="members", blank=True)
    host = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='room')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class Messages(models.Model):
    text = models.TextField()
    room = models.CharField(max_length=12, null=True, blank=True)
    user = models.ForeignKey(User, related_name='message',
                             null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if Room.objects.filter(code=self.room).count() == 0:
            raise ValidationError(('Room with this code does not exist.'))

    def __str__(self):
        return self.text
