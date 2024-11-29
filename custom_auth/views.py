from django.shortcuts import render, redirect
from django.contrib import messages
from django.template import Context

from .forms import UserRegisterForm
from  .utils import send_registration_email

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            send_registration_email(email, username)
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('account_login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form, 'title':'register here'})
