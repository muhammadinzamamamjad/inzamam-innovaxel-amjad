from django.db import models
import string
import random

def generate_short_code(length=6):
    """Generate a random string of given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class ShortURL(models.Model):
    url = models.URLField()
    shortCode = models.CharField(max_length=10, unique=True, default=generate_short_code)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    accessCount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.shortCode} -> {self.url}"
