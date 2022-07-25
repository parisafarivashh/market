from django.db import models

from user.models import User


class PrivateChat(models.Model):
    title = models.CharField(max_length=20, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_chat')
    date_create = models.DateTimeField(auto_created=True)

    class Meta:
        db_table = 'PrivateChat'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_messages')
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(blank=True, null=False)
    date_create = models.DateTimeField(auto_created=True)

    class Meta:
        db_table = 'Message'


class ChatMember(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatmembers')
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name='members')

    class Meta:
        db_table = 'ChatMember'
        unique_together = [('chat', 'member'), ]




