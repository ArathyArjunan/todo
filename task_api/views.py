from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from task.models import Todos
from task_api.serializers import TodoSerializer
from rest_framework.decorators import action



class TodoViewSetView(ModelViewSet):
    serializer_class=TodoSerializer
    queryset=Todos.objects.all()
                                       #--|
    #localhost:8000/api/todos/completed/  |
    # method:get                         _| --->completed todos
    @action(methods=["get"],detail=False)
    def completed(self,request,*args, **kwargs):
        qs=Todos.objects.filter(status=True)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    
                                     #    |
    #localhost:8000/api/todos/pending/    |
    # method:get                         _| --->pending todos


    @action(methods=["get"],detail=False)
    def pending(slef,request,*args, **kwargs):
        qs=Todos.objects.filter(status=False)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)



# class TodoViewSetView(ViewSet):
#     def list(self,request,*args,**kwargs):
#         qs=Todos.objects.all()
#         serializer=TodoSerializer(qs,many=True)           #deserialization
#         return Response(data=serializer.data)
    


#     def retrieve(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         qs=Todos.objects.get(id=id)
#         serializer=TodoSerializer(qs)                      #deserialization
#         return Response(data=serializer.data)
    


#     def create(self,request,*args,**kwargs):
#         serializer=TodoSerializer(data=request.data)        #serialization
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         else:
#             return Response(data=serializer.errors)
        

#     def update(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         obj=Todos.objects.get(id=id)
#         serializer=TodoSerializer(data=request.data,instance=obj)  #serialization
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         else:
#             return Response(data=serializer.errors)
        

#     def delete(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         Todos.objects.filter(id=id).delete()
#         return Response(data={"message":"deleted"})

        
