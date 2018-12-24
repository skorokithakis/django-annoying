from json import dumps, loads

from django.db import models

from annoying.fields import AutoOneToOneField, JSONField


class SuperVillain(models.Model):
    name = models.CharField(max_length=20, default="Dr Horrible")
    stats = JSONField(default=None, blank=True, null=True)


class Minion(models.Model):
    _PREFIX = 'I can: '

    name = models.CharField(max_length=20, default="Igor")
    skills = JSONField(default=None, blank=True, null=True,
                       serializer=lambda value: '{0}{1}'.format(Minion._PREFIX, dumps(value)),
                       deserializer=lambda value: loads(value[len(Minion._PREFIX):]))


class SuperHero(models.Model):
    name = models.CharField(max_length=20, default="Captain Hammer")
    mortal_enemy = AutoOneToOneField(SuperVillain, on_delete=models.CASCADE, related_name='mortal_enemy')


class SuperHeroUnmanaged(models.Model):
    name = models.CharField(max_length=20, default="Captain Hammer")
    mortal_enemy_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tests_superhero'
