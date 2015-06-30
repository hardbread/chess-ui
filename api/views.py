from django.views.decorators.http import require_safe
from django.http import JsonResponse
from api.utils import to_camel_case
from models import Tournament, Match, Player


def _json_api_response(data):
    response_format = {
        'responses': isinstance(data, list) and data or [data],
        'meta': {
            'count': len(data)
        }
    }
    return JsonResponse(to_camel_case(response_format))


@require_safe
def tournaments_all(request):
    resp = []
    for t in Tournament.objects.select_related('winner').order_by('start_date', 'end_date').all():
        resp.append(t.to_dict())
    return _json_api_response(resp)
