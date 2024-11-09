from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.views import LoginView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    #success_url = reverse_lazy('login')
    
    def form_valid(self,form):
        user = form.save()
        if user is not None:
            messages.success(self.request, 'Account created, you can now log in.')
            return redirect('login')
        return super(RegisterPage,self).form_valid(form)
    
class LoginPage(LoginView):
    template_name = 'base/login.html'
    fields = "__all__"
    redirect_authenticated_user = True       #if user is logged in this page is not shown
    #success_url = reverse_lazy('task')

    def get_success_url(self):
        return reverse_lazy('task')


class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'   
    #template_name = "base/task_list.html"(optional)   # it directly looks for the task_list.html file(name matters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete = False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            context['search_input'] = search_input
        return context
        

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    template_name = "base/task_detail.html"
    context_object_name = 'task'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('task')
    template_name = "base/task_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
    



class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('task')
    template_name = "base/task_form.html"

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
 
    success_url = reverse_lazy('task')
    template_name =  "base/task_confirm_delete.html"





