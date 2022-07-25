from django.db import models
from django.conf import settings
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
        settings.AUTH_USER_MODEL, related_name="members", null=True, blank=True)
    host = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='room')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class Messages(models.Model):
    text = models.TextField()
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
