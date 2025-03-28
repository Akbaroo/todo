from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from tasks.models import Task, Category

User = get_user_model()

class TaskTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Work")
        self.task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="This is a test task.",
            category=self.category,
            status="pending"
        )

    def test_task_list_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("tasks:task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_task_detail_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("tasks:task_detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a test task.")
    
    def test_create_task(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("tasks:task_create"), {
            "title": "New Task",
            "description": "New Task Description",
            "category": self.category.id,
            "status": "pending"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="New Task").exists())
    
    def test_update_task(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("tasks:task_update", args=[self.task.id]), {
            "title": "Updated Task",
            "description": "Updated Description",
            "category": self.category.id,
            "status": "completed"
        })
        self.assertEqual(response.status_code, 302) 
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")
    
    def test_delete_task(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("tasks:task_delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())