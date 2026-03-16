from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Board(models.Model):
    id = models.IntegerField(primary_key=True, unique=True,auto_created=True)
    title = models.CharField(max_length=200, verbose_name="Karzinka")
    slug = models.SlugField(max_length=200, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    password = models.CharField(max_length=128, blank=True, null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) +'-' +str(self.id)[:8]
        super(Board, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class BoardParticipant(models.Model):
    ROLE_CHOICES = (
        ('admin', "Admin"),
        ('editor', "Tahrirchi"),
        ('viewer', "Kuzatuvchi"),
    )

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    last_seen = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('board', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Stroke(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="strokes")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['created_at']


class ChatMessage(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('timestamp',)
