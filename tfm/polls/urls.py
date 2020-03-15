from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create', views.create, name='create'), #GET?
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/', views.DetailView.as_view(), name='details'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
