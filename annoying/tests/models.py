from django.db import models
from annoying.fields import AutoOneToOneField


class SuperVillain(models.Model):
    name = models.CharField(max_length="20", default="Dr Horrible")


class SuperHero(models.Model):
    name = models.CharField(max_length="20", default="Captain Hammer")
    mortal_enemy = AutoOneToOneField(SuperVillain, related_name='mortal_enemy')
