from django.urls import path

from jchart.views import ChartView

from . import views

from .charts import *



def here(*a, **kw):
    line_chart = RadarChart()
    return ChartView.from_chart(line_chart)(*a, **kw)



app_name = 'mtce'
urlpatterns = [
    path('', views.index, name='index'),
    path('comparison/<int:comparison_id>/', views.comparison_overview, name='comparison_detail'),
    path('system/<int:system_id>/', views.system_overview, name='system_detail'),
    path('help', views.help, name='help'),
    path('edit', views.edit, name='edit'),



    path('charts/line_chart/', here, name='line_chart'),

]