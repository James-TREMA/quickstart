from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

class PostPermissionMixin:
    def post(self, request: HttpRequest, *args, **kwargs)->HttpResponse:
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return HttpResponseForbidden('You are not allowed to perform this action!')
        return super().post(request, *args, **kwargs)