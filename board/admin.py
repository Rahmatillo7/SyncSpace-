from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_public', 'created_at')

@admin.register(BoardParticipant)
class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('role', 'board', 'user', 'last_seen')

@admin.register(Stroke)
class StrokeAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'data', 'created_at')

admin.site.register(ChatMessage)
