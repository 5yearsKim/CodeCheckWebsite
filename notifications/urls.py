from django.urls import path

from . import views


app_name = 'notifications'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:notification_id>/', views.detail, name='detail'),

]