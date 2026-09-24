from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        group = Group.objects.get(name=role)
        user.groups.add(group)

        messages.success(
            request,
            "Account created successfully."
        )

        return redirect("login")

    return render(
        request,
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.groups.filter(name="Admin").exists():
                return redirect("admin-dashboard")

            elif user.groups.filter(name="Teacher").exists():
                return redirect("teacher-dashboard")

            elif user.groups.filter(name="Student").exists():
                return redirect("student-dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )
    return render(request, "auth/login.html")

# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):

    logout(request)

    return redirect("login")