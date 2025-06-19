from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def is_valid_user(self):
        return self.first_name != self.last_name
