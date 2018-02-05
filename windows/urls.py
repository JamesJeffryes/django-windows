from django.urls import path

from . import views

app_name = 'windows'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list/', views.ListView.as_view(), name='list'),
    path('<uuid:pk>/', views.DonorView.as_view(), name='donor'),
    path('<uuid:pk>/select', views.SelectView.as_view(), name='select'),
    path('<uuid:pk>/confirm', views.ConfirmView.as_view(), name='confirm')
]