from django.shortcuts import redirect, render
from django.contrib import messages
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

from django.shortcuts import redirect
from django.urls import reverse


"""
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email_user = request.POST.get('email')
            password = request.POST.get('password')

            # Attempt to authenticate using email
            user = authenticate(request, email=email_user, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect(reverse('blog:post_list'))
            else:
                messages.error(request, 'Invalid email or password.')

        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'accounts/login.html', context)
    else:
        return redirect(reverse('blog:post_list'))
"""

from django.shortcuts import render

def login_view(request):
    return render(request, 'registration/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        return render(request, 'accounts/login.html' ) 
    return redirect(reverse('blog:post_list'))


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():                
                form.save()
                return redirect('accounts:login')  # Redirect to login page after signup
            else:
                return render(request, 'accounts/signup.html', {'form': form})  # Show form with errors
        else:
            form = CustomUserCreationForm()  # Use the custom form here
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        return render(request, 'blog/post_list.html' )