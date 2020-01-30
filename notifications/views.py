from django.shortcuts import render, get_object_or_404
from .models import Notification
from django.core.paginator import Paginator

def index(request):
    ntfs = Notification.objects.order_by('-pub_date')
    paginator = Paginator(ntfs, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'posts': posts}
    return render(request, 'notifications/index.html', context)


def detail(request, notification_id):
    ntf = get_object_or_404(Notification, pk=notification_id)
    return render(request, 'notifications/detail.html', {"notification": ntf})
