from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,CreateView
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
# Create your views here.

# Register View Simplified using Inheriting CreateView - ClassBasedView - Advanced ....   
class RegView(CreateView):
    template_name = 'reg.html'
    form_class = RegisterForm
    model = User
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        send_mail(
        'Open Blog',
        'Thanks for registering with us .',
        settings.EMAIL_HOST_USER,
        [form.cleaned_data.get('email')],
        )
        messages.success(self.request, "User Registration Successfull!")
        self.object = form.save()
        return super().form_valid(form)

# Register View using Inheriting View - ClassBasedView - Basic ....   
# class RegView(View):
#     def get(self,request,*args,**kwargs):
#         form = RegisterForm()
#         return render(request,'reg.html', {'form':form,})
#     def post(self,request,*args,**kwargs):
#         form = RegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,'User Registered Successfully!')
#             return redirect('login')
#         else:
#             messages.error(request,'User Registration Failed!')
#             return render(request,'reg.html', {'form':form,})


class LoginView(View):
    def get(self,request,*args,**kwargs):
        form = LoginForm()
        return render(request,'login.html', {'form':form,})
    def post(self,request,*args,**kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('Username')
            password = form.cleaned_data.get('Password')
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user) 
                return redirect('home')
            else:
                messages.error(request,'Invalid Credentials!')
                return redirect('login')
        else:
            return render(request,'login.html',{'form':form,})
        

class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,'User Logged Out Successfully!')
        return redirect('login')



