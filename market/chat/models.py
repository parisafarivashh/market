from django.db import models

from user.models import User


class Direct(models.Model):
    title = models.CharField(max_length=20, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_direct')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_direct')
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Direct'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_messages')
    direct = models.ForeignKey(Direct, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(blank=True, null=False)
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Message'


class ChatMember(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direct_members')
    direct = models.ForeignKey(Direct, on_delete=models.CASCADE, related_name='members')

    class Meta:
        db_table = 'DirectMember'
        unique_together = [('direct', 'member'), ]




