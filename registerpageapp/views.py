from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import UserProfile


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        full_name = request.POST.get("full_name", "")
        phone = request.POST.get("phone")
        college = request.POST.get("college")
        city = request.POST.get("city")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect('register')

        User = get_user_model()

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            full_name=full_name,
            mobile_number=phone,
            password=password
        )
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "college_name": college,
                "city": city,
            },
        )

        messages.success(
            request,
            "Registration Successful."
        )

        return redirect('login')

    return render(
        request,
        'auth/signup.html'
    )
