from django.urls import path

from . import views

app_name = 'mtce'
urlpatterns = [
    path('', views.index, name='index'),
    path('comparison/<int:comparison_id>/', views.comparison_detail, name='comparison_detail'),
    path('help', views.help, name='help'),
    path('edit', views.edit, name='edit'),
]