from .. import base


class CustomDeletionTests(base.TestCase):
    def setUp(self):
        self.project1 = self.models.Project.objects.create()
        self.project2 = self.models.Project.objects.create()
        self.links = self.models.Links.objects.create()

    def test_delete_src(self):
        self.links.related_objects = [self.project1, self.project2]
        self.links.delete()
        # no more Links instances
        self.assertEqual(self.models.Links.objects.count(), 0)
        # but the through model instances have not been deleted
        self.assertEqual(self.project1.links_set.through.objects.count(), 2)
        # clean up to avoid integrity error on teardown
        self.links.related_objects.through.objects.all().delete()

    def test_delete_tgt(self):
        self.links.related_objects = [self.project1, self.project2]
        self.project1.delete()
        self.project2.delete()
        # no more Project instances
        self.assertEqual(self.models.Project.objects.count(), 0)
        # but the through model instances have not been deleted
        self.assertEqual(self.links.related_objects.through.objects.count(), 2)
