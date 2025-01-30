from django.urls import path

from task_manager.labels import views

app_name = 'labels'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.LabelCreate.as_view(), name='create'),
    path('<int:pk>/delete/', views.LabelDelete.as_view(), name='delete'),
    path('<int:pk>/update/', views.LabelUpdate.as_view(), name='update'),
]
