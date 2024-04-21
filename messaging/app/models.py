from django.db import models


class CustomUser(models.Model):
    """ Class representing a user. """
    username = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.username


class Message(models.Model):
    """ Class representing a message. """
    created = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(
        CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"From {self.sender} to {self.recipient}. Sent: {self.created}"
