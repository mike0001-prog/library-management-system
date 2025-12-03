from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

# custom decorator functions
def superuser_validator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        session_user = request.user
        if session_user.is_superuser and session_user.is_active and session_user.is_authenticated:
            return view_func(request, *args, **kwargs)
        # return HttpResponseForbidden("You are not authorized to view this page. Only Admin is Authorized...")
        return redirect("forbidden")
    return _wrapped_view    
