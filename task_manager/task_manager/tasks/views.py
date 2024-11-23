from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests

def home(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'tasks/home.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    context = {
        'tasks': tasks,
        'pending_count': tasks.filter(completed=False).count(),
        'completed_count': tasks.filter(completed=True).count()
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})

@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    messages.success(request, f'Task marked as {"completed" if task.completed else "pending"}')
    return redirect('task_list')

# Google OAuth Views
def google_login(request):
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email']
    )
    flow.redirect_uri = request.build_absolute_uri('/oauth2callback/')
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    return redirect(authorization_url)

def oauth2callback(request):
    state = request.session['state']
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email'],
        state=state
    )
    flow.redirect_uri = request.build_absolute_uri('/oauth2callback/')
    
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    id_info = credentials.id_token
    email = id_info['email']
    
    user, created = User.objects.get_or_create(
        username=email,
        defaults={'email': email}
    )
    
    login(request, user)
    messages.success(request, f'Welcome, {email}!')
    return redirect('task_list')