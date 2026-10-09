from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Todo


class TaskApiTests(APITestCase):
    def setUp(self):
        self.list_url = reverse("task-list")

    def test_create_read_update_and_delete_task(self):
        # Create through the API and verify the database received the task.
        response = self.client.post(
            self.list_url,
            {"title": "Prepare portfolio", "description": "Explain the backend", "completed": False},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task_id = response.data["id"]
        detail_url = reverse("task-detail", args=[task_id])
        self.assertEqual(Todo.objects.count(), 1)

        # Read the same record, update it, and confirm no duplicate was created.
        response = self.client.get(detail_url)
        self.assertEqual(response.data["title"], "Prepare portfolio")
        response = self.client.patch(detail_url, {"completed": True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Todo.objects.get(pk=task_id).completed)
        self.assertEqual(Todo.objects.count(), 1)

        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 1)
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(pk=task_id).exists())

    def test_blank_title_is_rejected(self):
        response = self.client.post(
            self.list_url,
            {"title": "", "description": "Invalid task", "completed": False},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertEqual(Todo.objects.count(), 0)

    def test_missing_task_returns_not_found(self):
        response = self.client.get(reverse("task-detail", args=[999999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_local_frontend_is_allowed_by_cors(self):
        response = self.client.options(
            self.list_url,
            HTTP_ORIGIN="http://127.0.0.1:3000",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
        )
        self.assertEqual(response["Access-Control-Allow-Origin"], "http://127.0.0.1:3000")

    def test_unrelated_origin_is_not_allowed_by_cors(self):
        response = self.client.options(
            self.list_url,
            HTTP_ORIGIN="https://unrelated.example",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
        )
        self.assertNotIn("Access-Control-Allow-Origin", response)
