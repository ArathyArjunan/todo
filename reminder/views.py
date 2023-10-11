from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from reminder.forms import RegistrationForm,LoginForm,TodoCreateForm,TodoChangeForm
from django.views.generic import View,TemplateView,ListView,DetailView,UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from reminder.models import Todos
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session please login!!!!")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper





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
                return redirect("index")
            else:
               messages.error(request,"invalid credentials!!!!")
               return render(request,"signin.html",{"form":form})
            
@method_decorator(signin_required,name="dispatch")

class IndexView(TemplateView):
    template_name="index.html"
    def get(self,request,*args,**kwargs):
        form=TodoCreateForm()
        qs=Todos.objects.filter(user=request.user)
        return render(request,self.template_name,{"form":form,"todos":qs})
    def post(self,request,*args,**kwargs):
        form=TodoCreateForm(request.POST)
        if form.is_valid():
            Todos.objects.create(**form.cleaned_data,user=request.user)
            messages.success(request,"Added success")
            return redirect("index")


@method_decorator(signin_required,name="dispatch")

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
        
@method_decorator(signin_required,name="dispatch")

class TodoListView(ListView):
    template_name="reminder/todo_list.html"
    context_object_name="todos"
    model=Todos


    def get_queryset(self):
        qs=Todos.objects.filter(user=self.request.user)
        return qs
       
   
@method_decorator(signin_required,name="dispatch")

class TodoDetailView(DetailView):
    template_name="reminder/todo_detail.html"
    context_object_name="todo"
    model=Todos


    
    # def get(self,request,*args,**kwargs):
    #     qs=Todos.objects.all()
    #     return render(request,self.template_name,{"todos":qs})


@method_decorator(signin_required,name="dispatch")

class TodoUpdateView(UpdateView):
    template_name="reminder/todo_edit.html"
    form_class=TodoChangeForm
    model=Todos
    success_url=reverse_lazy("list-todo")

@signin_required

def remove_todo(request,*args,**kwargs):
    id=kwargs.get("pk")
    Todos.objects.filter(id=id).delete()
    return redirect("index")


@signin_required
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

