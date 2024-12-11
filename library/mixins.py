from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

class PostPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        print("DEBUG: PostPermissionMixin dispatch is executed.")  # Debug
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request: HttpRequest)->HttpResponse:
        print("DEBUG: PostPermissionMixin post is executed.")  # Debug
        if not request.user.is_authenticated:
            return HttpResponseForbidden('You are not allowed to perform this action!')
        return super().post(request)