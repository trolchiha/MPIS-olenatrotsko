from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('view-projects/', views.view_projects, name='view_projects'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-up-volunteer/', views.sign_up_volunteer, name='sign_up_volunteer'),
    path("logout/", views.log_out, name="logout"),
    path('create-project/', views.create_project, name='create_project'),
    path('view-project/<str:project_id>/', views.view_project, name='view_project'),
    path('update-project/<str:project_id>/', views.update_project, name='update_project'),
    path('сreate-application/<str:project_id>/', views.create_application, name='create_application'),
    path('delete-application/<str:application_id>/', views.delete_application, name='delete_application'),
    path('view-application/<str:application_id>/', views.view_application, name='view_application'),
    path('view-applications/', views.view_applications, name='view_applications'),
    path('search-project/', views.search_project, name='search_project'),
    path('view-project-volunteers/<str:project_id>/', views.view_project_volunteers, name='view_project_volunteers'),
    path('create-task/<str:project_id>/<str:user_id>/', views.create_task, name='create_task'),
    path('view-tasks/', views.view_tasks_volunteer, name='view_tasks_volunteer'),
    path('view-task/<str:task_id>/', views.view_task, name='view_task'),
    path('create-task/<str:project_id>/', views.view_project_tasks, name='view_project_tasks'),
    path('support-project/', views.support_project, name='support_project'),
]
