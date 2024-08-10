from django.db import models
from django.contrib.auth.models import User
from core.models import Sake, Wari, Other

class UserSake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sake = models.ForeignKey(Sake, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.sake.name} - {self.quantity}"

class UserWari(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wari = models.ForeignKey(Wari, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.wari.name} - {self.quantity}"

class UserOther(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    other = models.ForeignKey(Other, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.other.name} - {self.quantity}"
