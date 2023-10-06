from django.shortcuts import render,redirect
from reminder.forms import RegistrationForm,LoginForm,TodoCreateForm
from django.views.generic import View,TemplateView,ListView,DetailView
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from reminder.models import Todos



class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"signup.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration completed successfully")
            return redirect("signin")
        else:
            messages.error(request,"Registration failed")
            return render(request,"signup.html",{"form":form})
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect("add-todo")
            else:
               messages.error(request,"invalid credentials!!!!")
               return render(request,"signin.html",{"form":form})
            
class IndexView(TemplateView):
    template_name="index.html"

class TodoCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TodoCreateForm()
        return render(request,"reminder/todo_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=TodoCreateForm(request.POST)
        if form.is_valid():
            # form.save()
            Todos.objects.create(**form.cleaned_data,user=request.user)
            messages.success(request,"Added success")
            return redirect("add-todo")
        else:
            messages.error(request,"insertion failed")
            return render(request,"reminder/todo_add.html",{"form":form})
        

class TodoListView(ListView):
    template_name="reminder/todo_list.html"
    context_object_name="todos"
    model=Todos

class TodoDetailView(DetailView):
    template_name="reminder/todo_detail.html"
    context_object_name="todo"
    model=Todos


    
    # def get(self,request,*args,**kwargs):
    #     qs=Todos.objects.all()
    #     return render(request,self.template_name,{"todos":qs})
