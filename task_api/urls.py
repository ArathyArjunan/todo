from django.urls import path
from task_api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("Todos",views.TodoViewSetView,basename="Todos")



urlpatterns = [
 
    
]+router.urls
