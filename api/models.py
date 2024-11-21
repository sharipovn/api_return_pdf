from django.db import models
from django.contrib.auth.models import User

class UserToken(models.Model):
    username = models.CharField(max_length=50)
    access_token = models.TextField()
    refresh_token = models.TextField()
    access_token_expiry = models.DateTimeField()
    refresh_token_expiry = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.username}"

    class Meta:
        db_table='user_tokens'






class Report(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


