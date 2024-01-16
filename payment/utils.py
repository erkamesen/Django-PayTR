from functools import wraps
from django.shortcuts import redirect


def complete_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        profile = request.user.profile
        if profile.is_complete:
            return function(request, *args, **kwargs)
        else:
            return redirect("complete")

    return wrap
