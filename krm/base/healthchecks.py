from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def simpleHealthCheck(request, *callback_args, **callback_kwargs):
    return JsonResponse({'status':'Success'})