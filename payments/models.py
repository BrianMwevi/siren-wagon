from django.db import models
from django.utils import timezone


class DarajaToken(models.Model):
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def update_token(cls, new_token):
        old_token, expired = cls.get_credentials()
        old_token.token = new_token
        updated_token = old_token.save()
        return updated_token

    def has_expired(self):
        time_diff = (timezone.now() - self.updated_at).seconds
        if time_diff >= 3480:
            return True
        return False

    @classmethod
    def get_credentials(cls):
        token = cls.objects.first()
        if not token:
            return (None, None)
        expired = token.has_expired()
        return (token, expired)

    def __str__(self):
        return f'Expired: {self.get_credentials()[1]}'
