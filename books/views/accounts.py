from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from ..models import User
from ..forms import LoginForm, SignupForm

def accountsLogin(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)

    next_url = request.POST.get('next')

    if next_url is None: next_url = '/books'

    return redirect(next_url)
  else:
    return render(request, 'books/login.html',
      {'form': LoginForm(), 'next': request.GET.get('next')})

def accountsLogout(request):
  logout(request)
  return redirect('/books')

def accountsSignup(request):
  if request.user.is_authenticated:
    return redirect('/books')

  if request.method == 'POST':
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = User.objects.create_user(username, email, password)

    try:
      user.save()
    except Exception as e:
      return redirect('/accounts/signup')
    else:
      login(request, user)
      return redirect('/books')
  else:
    return render(request, 'books/signup.html', {'form': SignupForm()})
