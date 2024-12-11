from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

class PostPermissionMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.method == "POST" and not request.user.is_authenticated:
            return HttpResponseForbidden('Not allowed')
        return super().dispatch(request, *args, **kwargs)