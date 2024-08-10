from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from core.models import Sake, Wari, Other

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"))


from django.conf import settings
from django.db import models
from core.models import Sake, Wari, Other

class UserSake(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sake = models.ForeignKey(Sake, on_delete=models.CASCADE)
    owned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.sake.name}'

class UserWari(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wari = models.ForeignKey(Wari, on_delete=models.CASCADE)
    owned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.wari.name}'

class UserOther(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    other = models.ForeignKey(Other, on_delete=models.CASCADE)
    owned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.other.name}'

