from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from .models import Student


# =========================================================
# REGISTER
# =========================================================
def register(request):
  if request.method == "POST":
    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password")
    role = request.POST.get("role")

    if not username or not password:
      messages.error(request, "Username and password are required.")
      return render(request, "registeration/register.html")

    # Guard against duplicate username (prevents IntegrityError)
    if User.objects.filter(username=username).exists():
      messages.error(
          request, "This username is already taken. Please choose another."
      )
      return render(request, "registeration/register.html")

    # Guard against duplicate email
    if email and User.objects.filter(email=email).exists():
      messages.error(request, "An account with this email already exists.")
      return render(request, "registeration/register.html")

    # Create user safely
    user = User.objects.create_user(
        username=username, email=email, password=password
    )

    if role:
      group, _ = Group.objects.get_or_create(name=role)
      user.groups.add(group) 
      

      if role == "Student":
        Student.objects.create(
            user=user,
            name=username,
            email=email,
            age=18,
        )

    messages.success(
        request, "Account created successfully. Please sign in below."
    )
    return redirect("login")

  return render(request, "registeration/register.html")


# =========================================================
# LOGIN
# =========================================================
def user_login(request):
  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)

      if user.groups.filter(name="Admin").exists():
        return redirect("admin-dashboard")
      elif user.groups.filter(name="Teacher").exists():
        return redirect("teacher-dashboard")
      elif user.groups.filter(name="Student").exists():
        return redirect("student-dashboard")

    messages.error(request, "Invalid username or password.")

  return render(request, "auth/login.html")


# =========================================================
# LOGOUT
# =========================================================
def user_logout(request):
  logout(request)
  return redirect("login")