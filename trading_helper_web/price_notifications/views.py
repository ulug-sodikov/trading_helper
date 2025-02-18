import decimal

import requests
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed,
    HttpResponseBadRequest
)
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from .models import Notification
from .adjust_mt5_buffer import adjust_mt5_buffer


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('auth_telegram:index'))

    template = loader.get_template('price_notifications/index.html')
    notifications = (
        Notification.objects.filter(user=request.user).order_by('-created_at')
    )
    context = {'notifications': notifications}

    return HttpResponse(template.render(context, request))


def create_notification(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('auth_telegram:index'))

    def create_error_context_response(error_message):
        return render(
            request,
            'price_notifications/index.html',
            context={
                'error_message': error_message,
                'notifications': (
                    Notification.objects
                    .filter(user=request.user)
                    .order_by('-created_at')
                )
            }
        )

    data = request.POST.dict()

    # Check if all required fields have been received.
    fields = {}
    try:
        fields['symbol'] = data['symbol']
        fields['target_price'] = data['target_price']
        fields['comparison_type'] = (
            Notification.ComparisonType[data['comparison_type']]
        )
        fields['tracking_price_type'] = (
            Notification.PriceType[data['tracking_price_type']]
        )
    except KeyError:
        return create_error_context_response('Missing required param.')

    # Check if received "target_price" field is valid number type.
    try:
        fields['target_price'] = decimal.Decimal(str(fields['target_price']))
    except decimal.InvalidOperation:
        return create_error_context_response('Invalid "target_price" param.')

    # Check if received symbol exists in mt5.
    response = requests.get(
        f'http://metatrader5_api_service:8080/symbol_exists/{fields["symbol"]}'
    )
    if response.status_code != 200:
        return create_error_context_response(
            f"\"{fields['symbol']}\" Symbol doesn't exist in mt5."
        )

    fields['symbol'] = fields['symbol'].upper()
    fields['user'] = request.user
    Notification.objects.create(**fields)
    adjust_mt5_buffer()

    return HttpResponseRedirect(reverse('price_notifications:index'))


def delete_notification(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest('Unauthorized.')

    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])

    notification = get_object_or_404(Notification, pk=pk)
    notification.delete()
    adjust_mt5_buffer()

    return HttpResponse()
