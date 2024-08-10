from django.db import models

class Sake(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    aroma = models.CharField(max_length=100)
    sweetness = models.FloatField()
    bitterness = models.FloatField()
    sourness = models.FloatField()
    alcohol_content = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Wari(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    aroma = models.CharField(max_length=100)
    sweetness = models.FloatField()
    bitterness = models.FloatField()
    sourness = models.FloatField()

    def __str__(self):
        return self.name

class Other(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
