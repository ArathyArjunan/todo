from django.urls import path
from reminder_api import views


urlpatterns = [
    path("v2/Todos/register",views.UserCreationView.as_view())
    
]
