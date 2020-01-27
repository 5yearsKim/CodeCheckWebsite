from django.shortcuts import render, get_object_or_404
from .models import Notification


def index(request):
    ntfs = Notification.objects.order_by('-pub_date')
    context = {'notifications': ntfs}
    return render(request, 'notifications/index.html', context)


def detail(request, notification_id):
    ntf = get_object_or_404(Notification, pk=notification_id)
    return render(request, 'notifications/detail.html', {"notification": ntf})
