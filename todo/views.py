from django.shortcuts import render
from django.http import HttpResponse
import mimetypes

from rest_framework import viewsets          
from .serializers import TodoSerializer
from .models import Todo

class TodoView(viewsets.ModelViewSet):       
  serializer_class = TodoSerializer          
  queryset = Todo.objects.all()

def css_view(request):
    # Replace 'path/to/your/style.css' with the actual path to your CSS file
    css_file_path = 'C:/Users/sfihl/Documents/code/django-react-app/backend/staticfiles/admin/css'

    # Open the CSS file and read its content
    with open(css_file_path, 'r') as css_file:
        css_content = css_file.read()

    # Create an HttpResponse with the CSS content
    response = HttpResponse(css_content, content_type='text/css')

    # Optionally, you can set other headers or cache-related directives
    # For example:
    # response['Cache-Control'] = 'max-age=3600'  # Cache for 1 hour

    return response