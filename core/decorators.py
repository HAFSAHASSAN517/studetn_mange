from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def role_required(role):
    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # User is not logged in
            if not request.user.is_authenticated:
                return redirect("login")

            # User is logged in but has the wrong role
            if not request.user.groups.filter(name=role).exists():
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator