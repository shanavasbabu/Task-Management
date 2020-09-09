from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import PasswordChangeView
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import SignUpForm
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
# from django.urls import reverse_lazy
# from django.views import generic



def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':SignUpForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':SignUpForm(), 'error':'That username has already been taken. Please choose a new username'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'todo/signupuser.html', {'form': SignUpForm(), 'error': 'Email is already taken'})
        else:
            return render(request, 'todo/signupuser.html', {'form':SignUpForm(), 'error':'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todos})


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error':'Big Data passed in. Try again.'})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk= todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error':'Bad Info'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos':todos})


@login_required
def view_profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'todo/profile_1.html', context)

# @login_required
# class UserEditView(generic.UpdateView):
#     form_class = EditProfileForm
#     template_name = 'todo/edit_profile.html'
#     success_url = reverse_lazy('home')
#
#     def get_object(self):
#         return self.request.user

# @login_required
# class PasswordsChangeView(PasswordChangeView):
#     # form_class = PasswordChangeForm
#     form_class = PasswordChangingForm
#     #success_url = reverse_lazy('home')
#     success_url = reverse_lazy('password_success')
#
# @login_required
# def password_success(request):
#     return render(request, 'todo/password_success.html', {})










