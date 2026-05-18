from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def csp_report(request):
    if request.method == 'POST':
        report = json.loads(request.body)
        print(json.dumps(report, indent=2))
    return HttpResponse(status=204)