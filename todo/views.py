from django.conf import settings
from django.db import connection, transaction
from rest_framework import permissions, viewsets
from rest_framework.exceptions import ValidationError

from .models import Todo
from .serializers import TodoSerializer
from .throttles import DemoReadThrottle, DemoWriteThrottle


class TodoView(viewsets.ModelViewSet):
    """Shared public demo. Use sample data only; other visitors can change tasks."""

    serializer_class = TodoSerializer
    queryset = Todo.objects.order_by("id")
    permission_classes = [permissions.AllowAny]
    throttle_classes = [DemoReadThrottle, DemoWriteThrottle]

    @transaction.atomic
    def perform_create(self, serializer):
        if connection.vendor == "postgresql":
            table = connection.ops.quote_name(Todo._meta.db_table)
            with connection.cursor() as cursor:
                cursor.execute(f"LOCK TABLE {table} IN SHARE ROW EXCLUSIVE MODE")
        if Todo.objects.count() >= settings.DEMO_TASK_LIMIT:
            raise ValidationError("The demo is full. Remove a sample task before adding another.")
        serializer.save()
