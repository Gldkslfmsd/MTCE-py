from django.urls import path

from . import views

app_name = 'mtce'
urlpatterns = [
    path('', views.index, name='index'),
    path('dataset/<int:dataset_id>/', views.dataset_detail, name='dataset'),
]