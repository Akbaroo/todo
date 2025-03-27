from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Task, Category

User = get_user_model()


class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Work")
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            user=self.user,
            category=self.category,
            status="pending"
        )

    def test_task_creation(self):
        """ saved? """
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.user.username, "testuser")
        self.assertEqual(self.task.status, "pending")

    def test_task_update(self):
        """ update """
        self.task.status = "completed"
        self.task.save()
        self.assertEqual(Task.objects.get(id=self.task.id).status, "completed")

    def test_task_delete(self):
        """ delete """
        task_id = self.task.id
        self.task.delete()
        self.assertFalse(Task.objects.filter(id=task_id).exists())

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Personal")

    def test_category_creation(self):
        """بررسی اینکه دسته‌بندی ساخته شده"""
        self.assertEqual(self.category.name, "Personal")
