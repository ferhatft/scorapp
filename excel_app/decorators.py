from functools import wraps
from django.shortcuts import redirect

def authUser(redirect_url="/permissionDenied", permission_user=""):
    def wrapper(view_func):
        
        def wrap(request, *args, **kwargs):
            
            
            if permission_user == "bakimci" and request.user.profile.bakimci:
                return view_func(request, *args, **kwargs)
        
            elif permission_user == "kontrolcu" and request.user.profile.kontrolcu:
                return view_func(request, *args, **kwargs)
            
            else:
                # return redirect(redirect_url)
                return view_func(request, *args, **kwargs)
        return wrap
    return wrapper