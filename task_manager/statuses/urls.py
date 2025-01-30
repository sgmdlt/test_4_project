from django.urls import path

from task_manager.statuses import views

app_name = 'statuses'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.TaskStatusCreate.as_view(), name='create'),
    path('<int:pk>/delete/', views.TaskStatusDelete.as_view(), name='delete'),
    path('<int:pk>/update/', views.TaskStatusUpdate.as_view(), name='update'),
]
