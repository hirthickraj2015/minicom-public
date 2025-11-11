from django.db import models
from django.utils import timezone


class Message(models.Model):
    """Model to store chat messages"""
    username = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    room = models.CharField(max_length=100, default='general')

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.username}: {self.content[:50]}"

    def to_dict(self):
        """Convert message to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'username': self.username,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'room': self.room
        }
