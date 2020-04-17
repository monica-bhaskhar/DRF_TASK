from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('user/signup/', views.UserRegistrationAPIView.as_view(), name="signup"),
    path('user/login/', views.UserLoginAPIView.as_view(), name="login"),
    path('tasks/', views.TodoListCreateAPIView.as_view(), name="list"),
    path('tasks/<int:pk>/', views.TodoDetailAPIView.as_view(), name="detail"),

]
