from django.test import TestCase
from . import models


class FieldsTestCase(TestCase):
    def test_auto_one_to_one(self):
        super_villain = models.SuperVillain.objects.create()
        self.assertEqual(super_villain.mortal_enemy.name, "Captain Hammer")
