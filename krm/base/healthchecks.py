from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def simpleHealthCheck(request, *callback_args, **callback_kwargs):
    return HttpResponse('ok')