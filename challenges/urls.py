from django.urls import path
from . import views


app_name = 'challenges'
urlpatterns = [
    path('', views.basic, name='basic'),
    path('challenge_index/', views.challenge_index, name='challenge_index'),
    path('quiz_index/', views.quiz_index, name='quiz_index'),
    path('mypage/', views.mypage, name='mypage'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/submitpage', views.submitpage, name='submitpage'),
]
