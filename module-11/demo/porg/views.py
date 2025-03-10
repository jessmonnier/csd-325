'''
Jess Monnier, CSD-325 Assignment 11.2, 9 March 2025
The views defined in this script came from the following GitHub distro:
https://github.com/shreys7/django-todo/tree/develop
I've added my own comments partly to increase my understanding of them.
'''

from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import Todo

# This allows for the todo items to be pulled into
# the index in reverse creation order
class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        """Return all the latest todos."""
        return Todo.objects.order_by('-created_at')

# Allows a new todo item to be added and the page refreshed
def add(request):
    title = request.POST['title']
    Todo.objects.create(title=title)

    return redirect('todos:index')

# Allows an existing todo to be deleted and the page refreshed
def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect('todos:index')

# Allows an existing todo to be toggled between complete/incomplete
def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    isCompleted = request.POST.get('isCompleted', False)
    if isCompleted == 'on':
        isCompleted = True
    
    todo.isCompleted = isCompleted

    todo.save()
    return redirect('todos:index')

# This one I added. It just shows the contents of about.html.
def about(request):
    return render(request, "about.html")