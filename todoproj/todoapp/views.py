from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Todo



@login_required
# Create your views here.
def home(request):
    if request.method == 'POST':
        # Handle form submission here
        # For example, you can process a form or perform some action
        title = request.POST.get('title')
        usertask = Todo(user=request.user,title=title)
        
        usertask.save()
        # Redirect to the same page or another page after processing
        return redirect('home')
    # This is the home page view
    todos = Todo.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'TodoApp/index.html', {'todos': todos})  # Render the index.html template with todos

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass_word')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            auth_login(request, user)
            messages.success(request, "Welcome , " + username )
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')  # Redirect back to the login page
    return render(request, 'TodoApp/login.html')  # Render the main.html template

#Logout function
def logout_view(request):
    auth_logout(request)
    return redirect('login')  # Redirect to the login page after logout


#creating register function
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # # Validate the form data
        # # Check if the passwords match
        if len(password) < 3:
            messages.error(request, 'Password is too short')
            return redirect('register')
        # # Check if the username already exists
        elif User.objects.filter(username=username).exists():
        #     # Handle the error (e.g., show a message to the user)
            messages.error(request, 'Username already exists')
            return redirect('register')
        else:
            # Create a new user
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            # Optionally, you can log the user in after registration
            # auth_login(request, new_user)
            messages.success(request, "Welcome , " + username + "!")
            # Redirect to a success page or the home page
            return redirect('home')
    return render(request, 'TodoApp/register.html')

@login_required
#update function
def complete_todo(request, title):
    get_todo = Todo.objects.get(user=request.user, title=title)
    if get_todo.status == True:
        get_todo.status = False
    else:
        get_todo.status = True
    get_todo.save()
    return redirect('home')

@login_required
#delete function
def delete_todo(request, pk):
    get_todo = Todo.objects.get(user=request.user, pk=pk)
    get_todo.delete()
    print("Deleted")
    print("Deleted")
    print("Deleted")
    print("Deleted")
    return redirect('home')

@login_required
#update function
def update_todo(request, todo_id):
    get_todo = Todo.objects.get(user=request.user, pk=todo_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        get_todo.title = title
        get_todo.save()
        return redirect('home')
   
    return render(request, 'TodoApp/editModal.html', {'todo': get_todo})
