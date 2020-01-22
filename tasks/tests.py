from django.test import TestCase
from .models import Task

class TaskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Task.objects.create(title='first Task')
        Task.objects.create(description='a description here')

    def test_title_content(self):
        Task = Task.objects.get(id=1)
        expected_object_name = Task.title
        self.assertEquals(expected_object_name, 'first Task')

    def test_description_content(self):
        Task = Task.objects.get(id=2)
        expected_object_name = Task.description
        self.assertEquals(expected_object_name, 'a description here')
