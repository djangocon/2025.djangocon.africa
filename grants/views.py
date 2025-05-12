# grants/views.py
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages

import logging
import random
import string
import re

from django.conf import settings
from .models import GrantApplication, VerificationCode
from .utils.email import send_email  # Import the new function


logger = logging.getLogger(__name__)


def parse_budget(budget_text):
    """Parse budget text into total amount (if present) and details."""
    budget = {"details": ""}
    if not budget_text.strip():
        return budget

    # Normalize input: replace commas
    budget_text = budget_text.replace(",", "")

    # Extract total amount (integer or decimal, with $ before or after)
    total_match = re.search(r"Total\s*.*?\$?([\d.]+)\$?", budget_text, re.IGNORECASE | re.DOTALL)
    if total_match:
        total_amount = total_match.group(1)
        # Format total as $X.XX
        if "." not in total_amount:
            total_amount += ".00"
        budget["total_amount"] = "$" + total_amount

    # Capture details: everything except the total line
    details = []
    for line in budget_text.splitlines():
        # Match lines with "Total" followed by a number (with optional $)
        if not re.search(r"Total\s*.*?\b[\d.]+", line, re.IGNORECASE):
            if line.strip():  # Skip empty lines
                details.append(line.strip())
    budget["details"] = "\n".join(details) if details else ""

    return budget

def request_code(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        if not email:
            messages.error(request, "Please enter a valid email.")
            return render(request, "grants/request_code.html")
        try:
            GrantApplication.objects.get(email=email)
        except GrantApplication.DoesNotExist:
            messages.error(request, "Email not found in our database.")
            return render(request, "grants/request_code.html")
        code = "".join(random.choices(string.digits, k=6))
        VerificationCode.objects.update_or_create(
            email=email,
            defaults={
                "code": code,
                "expires_at": timezone.now() + timedelta(minutes=10),
            },
        )
        subject = "DjangoCon Africa Grant Verification Code"
        context = {"code": code}
        html_content = render_to_string("grants/verification_email.html", context)
        text_content = (
            f"Your verification code is: {code}\nThis code expires in 10 minutes."
        )
        success = send_email(
            subject=subject,
            text_content=text_content,
            html_content=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            from_name=settings.DEFAULT_FROM_NAME,
            to_email=email,
            to_name=None,
        )
        if success:
            messages.success(request, "Verification code sent to your email.")
            return redirect("verify_code", email=email)
        else:
            messages.error(request, "Failed to send email. Please try again.")
            return render(request, "grants/request_code.html")
    return render(request, "grants/request_code.html")


def verify_code(request, email):
    try:
        application = GrantApplication.objects.get(email=email)
    except GrantApplication.DoesNotExist:
        messages.error(request, "Email not found in our database.")
        return redirect("request_code")
    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        try:
            verification = VerificationCode.objects.get(email=email, code=code)
            if not verification.is_valid():
                verification.delete()
                messages.error(request, "Invalid or expired code.")
                return render(request, "grants/verify_code.html")
            verification.delete()
            parsed_budget = parse_budget(application.budget_details)
            context = {
                "application": application,
                "budget": parsed_budget,
            }
            return render(request, "grants/grant_status.html", context)
        except VerificationCode.DoesNotExist:
            VerificationCode.objects.filter(email=email).delete()  # Delete on invalid code
            messages.error(request, "Invalid or expired code.")
            return render(request, "grants/verify_code.html")
    return render(request, "grants/verify_code.html", {"email": email})