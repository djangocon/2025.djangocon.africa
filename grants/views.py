# grants/views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import GrantApplication, VerificationCode
from django.contrib import messages
import re
import random
import string
from django.utils import timezone
from datetime import timedelta

def parse_budget(budget_text):
    """Parse budget text into a structured dictionary."""
    budget = {'total_amount': '0$', 'items': []}
    if not budget_text.strip():
        return budget
    total_match = re.search(r'Total.*?\$(\d+)', budget_text, re.IGNORECASE)
    if total_match:
        budget['total_amount'] = total_match.group(1) + '$'
    items = re.findall(r'(\w+(?:\s*\w+)*)\s*:\s*\$?(\d+)(?:\s*\([^)]+\))?', budget_text, re.IGNORECASE)
    for item_name, item_cost in items:
        budget['items'].append({'name': item_name.strip(), 'cost': '$' + item_cost})
    return budget

def request_code(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if not email:
            messages.error(request, 'Please enter a valid email.')
            return render(request, 'grants/request_code.html')

        try:
            GrantApplication.objects.get(email=email)
        except GrantApplication.DoesNotExist:
            messages.error(request, 'Email not found in our database.')
            return render(request, 'grants/request_code.html')

        code = ''.join(random.choices(string.digits, k=6))
        VerificationCode.objects.update_or_create(
            email=email,
            defaults={
                'code': code,
                'expires_at': timezone.now() + timedelta(minutes=10)
            }
        )

        subject = 'DjangoCon Africa Grant Verification Code'
        message = f'Your verification code is: {code}\nThis code expires in 10 minutes.'
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Verification code sent to your email.')
        except Exception as e:
            messages.error(request, 'Failed to send email. Please try again.')
            return render(request, 'grants/request_code.html')

        return redirect('verify_code', email=email)

    return render(request, 'grants/request_code.html')

def verify_code(request, email):
    email = email.lower()
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()

        try:
            verification = VerificationCode.objects.get(email=email, code=code)
            if not verification.is_valid():
                verification.delete()
                messages.error(request, 'Invalid or expired code.')
                return render(request, 'grants/verify_code.html', {'email': email})
            verification.delete()
        except VerificationCode.DoesNotExist:
            messages.error(request, 'Invalid or expired code.')
            return render(request, 'grants/verify_code.html', {'email': email})

        try:
            application = GrantApplication.objects.get(email=email)
            budget = parse_budget(application.budget_details)
            return render(request, 'grants/grant_status.html', {
                'application': application,
                'budget': budget
            })
        except GrantApplication.DoesNotExist:
            messages.error(request, 'Email not found in our database.')
            return redirect('request_code')

    return render(request, 'grants/verify_code.html', {'email': email})