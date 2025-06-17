from django.db import models

class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    thread_id = models.CharField(max_length=36)
    user_id = models.BigIntegerField()
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['thread_id', 'user_id'], name='unique_conversation'
            )
        ]
        ordering = ['-created_at']
        db_table = 'chatbot.conversation'

class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_user = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    relevant_chunks = models.JSONField(blank=True, null=True)
    class Meta:
        ordering = ['timestamp']
        db_table = 'chatbot.message'
