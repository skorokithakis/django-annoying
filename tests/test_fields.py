import json
from contextlib import contextmanager

from django.db import IntegrityError
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

    def test_auto_one_to_one_race_condition(self):
        """
        Test for case:

        process #1 checks if related object exists
        process #2 checks if related object exists
        process #1 creates related object
        process #2 returns object created by process #1
        """
        @contextmanager
        def patch_get_or_create():
            old_get_or_create = models.SuperHero.objects.get_or_create

            def get_or_create(mortal_enemy):
                # create entity using unmanaged model to avoid caching
                obj = models.SuperHeroUnmanaged.objects.create(mortal_enemy_id=mortal_enemy.pk)
                return models.SuperHero.objects.get(pk=obj.pk), True

            try:
                models.SuperHero.objects.get_or_create = get_or_create
                yield
            finally:
                models.SuperHero.objects.get_or_create = old_get_or_create

        with patch_get_or_create():
            try:
                super_villain = models.SuperVillain.objects.create()
                # check if two calls to AutoOneToOneField descriptor returns the same object
                self.assertEqual(id(super_villain.mortal_enemy), id(super_villain.mortal_enemy))
            except (models.SuperHero.DoesNotExist, IntegrityError):
                self.fail("AutoOneToOneField cannot see related object created by another process")

    def test_json_field_create(self):
        stats = {
            'strength': 100,
            'defence': 50,
        }
        sv = models.SuperVillain.objects.create(stats=stats)

        # Refresh from DB
        super_villain = models.SuperVillain.objects.get(pk=sv.pk)

        self.assertEqual(super_villain.stats['strength'], stats['strength'])
        self.assertEqual(super_villain.stats['defence'], stats['defence'])
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

        self.assertEqual(super_villain.stats['strength'], stats['strength'])
        self.assertEqual(super_villain.stats['defence'], stats['defence'])
        self.assertEqual(dump_dict(super_villain.stats), dump_dict(stats))

    def test_json_field_custom_serializer_deserializer(self):
        skills = {
            'make': ['atomic_bomb', 'coffee'],
            'understand': ['string_theory', 'women'],
        }
        minion = models.Minion.objects.create(skills=skills)

        # Refresh from DB
        minion = models.Minion.objects.get(pk=minion.pk)

        self.assertEqual(minion.skills['make'], skills['make'])
        self.assertEqual(minion.skills['understand'], skills['understand'])
        self.assertEqual(dump_dict(minion.skills), dump_dict(skills))
