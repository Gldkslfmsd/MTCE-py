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
    path('comparison/<int:comparison_id>/', views.corpus_metrics, name='comparison_index'),

    path('comparison/<int:comparison_id>/sentences/', views.sentences, name='comparison_sentences'),

    path('system/<int:system_id>/', views.system_index, name='system_index'),
    path('system/<int:system_id>/sentences/', views.system_sentences, name='system_sentences'),



   # path('show_sentences/<int:comparison_id>/', views.show_sentences, name="show_sentences"),

   # path('charts/line_chart/', here, name='line_chart'),


   # path('help', views.help, name='help'),
   # path('edit', views.edit, name='edit'),

]