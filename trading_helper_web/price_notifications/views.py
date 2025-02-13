from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader

from .models import Notification


def index(request):
    template = loader.get_template('price_notifications/index.html')
    context = {}

    return HttpResponse(template.render(context, request))


def create_notification(request):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Unauthenticated.")

    data = request.POST.dict()

    notification = Notification(user=request.user)
    try:
        notification.symbol = data['symbol']
        notification.target_price = data['target_price']
        notification.comparison_type = (
            Notification.ComparisonType[data['comparison_type']]
        )
        notification.tracking_price_type = (
            Notification.PriceType[data['tracking_price_type']]
        )
    except KeyError:
        return HttpResponseBadRequest("Missing required param.")
    else:
        notification.save()

    return HttpResponse(status=201)
