from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView,View,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.contrib import messages
from .forms import UserProfileForm,ChangePasswordForm,BlogForm,CommentForm
from account.models import UserProfile,Blogs,Comments,Followers
from django.utils.decorators import method_decorator

def signin_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            return redirect('login')
    return wrapper  

# Create your views here.

# Viewing home_page using TemplateView - [no need of get func.] - simplified
@method_decorator(signin_required,name='dispatch')
class HomeView(CreateView):
    form_class = BlogForm
    model = Blogs
    template_name = 'main_home.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user  # getting form instance and accessing user and then assigning current user to it
        self.object = form.save()
        messages.success(self.request, "Blog Posted")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        following = Followers.objects.filter(follower=self.request.user).values_list('following',flat=True)
        lists = list(following)
        lists.append(self.request.user.id)
        print(lists)

        context['data'] = Blogs.objects.filter(user_id__in=lists).order_by('user')
        context['following_users'] = User.objects.filter(id__in=following)
        context['users'] = User.objects.all().exclude(username=self.request.user.username)
        context['comment_form'] = CommentForm() # comment form context to pass to front end
        context['comments'] = Comments.objects.all() # comments obj context to pass to front end
        return context

@method_decorator(signin_required,name='dispatch')
class MyBlogs(TemplateView):
    template_name = 'my_blogs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = Blogs.objects.filter(user=self.request.user).order_by('-date')
        return context

# Update Blog Using UpdateView
@method_decorator(signin_required,name='dispatch')
class UpdateBlog(UpdateView):
    form_class = BlogForm
    model = Blogs
    template_name = 'update_blogs.html'
    success_url = reverse_lazy('my_blogs')

# Delete Blog Using DeleteView
@method_decorator(signin_required,name='dispatch')
class DeleteBlog(DeleteView):
    model = Blogs
    template_name = 'delete_blog.html'
    success_url = reverse_lazy('my_blogs')

@method_decorator(signin_required,name='dispatch')
class NUserProfile(TemplateView):
    template_name = 'userprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_count'] = Blogs.objects.filter(user=self.request.user).count()

        following = Followers.objects.filter(follower=self.request.user).values('following')
        context['following_users_count'] = User.objects.filter(id__in=following).count()

        follower = Followers.objects.filter(following=self.request.user).values('follower')
        context['follower_users_count'] = User.objects.filter(id__in=follower).count()
        return context

@method_decorator(signin_required,name='dispatch')
class AddProfile(CreateView):
    form_class = UserProfileForm
    model = UserProfile
    template_name = 'add_profile.html'
    success_url = reverse_lazy('user_profile')

    # overriding form_valid method to create profile - best approach
    def form_valid(self, form):
        form.instance.user = self.request.user  # getting form instance and accessing user and then assigning current user to it
        self.object = form.save()
        messages.success(self.request, "Profile Added")
        return super().form_valid(form)

    # overriding post method to create profile - not best approach
    # def post(self,request,*args,**kwargs):
    #     form = self.form_class(data=request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
    #         return redirect('user_profile')
    #     else:
    #         return render(request,'userprofile.html',{'form':form})

@method_decorator(signin_required,name='dispatch')
class ChangePassword(FormView):
    template_name = 'change_password.html'
    form_class = ChangePasswordForm

    def post(self,request,*args,**kwargs):
        old_pass = request.POST['old_password']
        new_pass = request.POST['new_password']
        c_pass = request.POST['c_password']

        user = authenticate(username=request.user.username,password=old_pass)
        if user:
            if new_pass == c_pass:
                user.set_password(new_pass)
                user.save()
                logout(request)
                messages.success(request,'Passsword changed successfully')
                return redirect('login')
            else:
                messages.error(request,'Password Mismatch')
                return redirect('change_password')
        else:
            messages.error(request,'Old password was invalid')
            return redirect('change_password')

@method_decorator(signin_required,name='dispatch')
class UpdateProfile(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        user = UserProfile.objects.get(id=id)
        form = UserProfileForm(instance=user)
        return render(request,'update_profile.html', {'form':form})

    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        user = UserProfile.objects.get(id=id)
        form = UserProfileForm(instance=user,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
        return render(request,'update_profile.html', {'form':form})

def AddComments(request,bid):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        blog = Blogs.objects.get(id=bid)
        user = request.user
        Comments.objects.create(user=user, blog=blog, comment=comment)
        messages.success(request, 'Comment Added!')
        return redirect('home')

def AddLike(request,id):
    blog = Blogs.objects.get(id=id)
    blog.liked_by.add(request.user)
    blog.save()
    return redirect('home')

def RemoveLike(request,id):
    blog = Blogs.objects.get(id=id)
    blog.liked_by.remove(request.user)
    blog.save()
    return redirect('home')

def Follow(request,id):
    if Followers.objects.filter(follower=request.user.id , following=id).exists():
        followObj = Followers.objects.filter(follower=request.user.id , following=id)
        followObj.delete()
    else:
        user = User.objects.get(id=id)  
        followObj = Followers.objects.create(follower=request.user , following=user) 
        followObj.save()   
    return redirect('home')





    