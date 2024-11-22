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



class UsersForTkn(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    key = models.CharField(max_length=255)
    
    class Meta:
        db_table = u'"ies\".\"users_for_tkn"'
        managed = False

