import json

from django.test import TestCase
from . import models


def dump_dict(d):
    """
    Returns a JSON string sorted by keys
    """
    return json.dumps(d, sort_keys=True)


class FieldsTestCase(TestCase):
    def test_auto_one_to_one(self):
        super_villain = models.SuperVillain.objects.create()
        self.assertEqual(super_villain.mortal_enemy.name, "Captain Hammer")

    def test_json_field_create(self):
        stats = {
            'strength': 100,
            'defence': 50,
        }
        sv = models.SuperVillain.objects.create(stats=stats)

        # Refresh from DB
        super_villain = models.SuperVillain.objects.get(pk=sv.pk)

        self.assertEqual(super_villain.stats['strength'], 100)
        self.assertEqual(super_villain.stats['defence'], 50)
        self.assertEqual(dump_dict(super_villain.stats), dump_dict(stats))

    def test_json_field_update(self):
        super_villain = models.SuperVillain.objects.create()
        stats = {
            'strength': 100,
            'defence': 50,
        }
        super_villain.stats = stats
        super_villain.save()

        # Refresh from DB
        super_villain = models.SuperVillain.objects.get(pk=super_villain.pk)

        self.assertEqual(super_villain.stats['strength'], 100)
        self.assertEqual(super_villain.stats['defence'], 50)
        self.assertEqual(dump_dict(super_villain.stats), dump_dict(stats))
