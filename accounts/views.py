from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from article.models import Article
from .models import Profile
from .forms import UserRegistionForm, LoginForm, UserEditForm, ProfileEditForm
# Create your views here.

def signup_user(request):
    if request.method == 'POST':
        form = UserRegistionForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, 'Account Created Successfully, login to continue')
            return redirect('login')
        else:
            if 'password2' in form.errors:
                messages.error(request, 'Passwords do not match.')
            elif 'username' in form.errors:
                messages.error(request, 'A user with that username already exists.')
            elif 'email' in form.errors:
                messages.error(request, 'A user with that email address already exists.')
            else:
                messages.error(request, 'There was an error with your signup. Please try again.')
            return redirect('signup')
    else:
        form = UserRegistionForm()
    return render(request, 'registration/signup.html', {'form': form}) 


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password']) 
        
            if user is not None:
                if user.is_active:
                    login(request, user)  
                    messages.success(request, 'login successfully')
                    return redirect('article:article_list')      
                else:
                    messages.warning(request, 'something went wrong')
            else:
                messages.warning(request, 'Invalid username or password.')
                
        else:
            form = LoginForm()
            
    return render(request, 'registration/login.html')
    
def logout_user(request):
    logout(request)
    messages.info(request, "Your session has ended login to continue ")
    return redirect('login')

@login_required
def profile(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
    articles = Article.published.filter(author=request.user).order_by('-created')
    return render(request, 'profile/profile.html', {'profile':profile, 'articles':articles})

@login_required
def edit_profile(request):
    if request.method == 'POST':
       user_form = UserEditForm(instance=request.user, data=request.POST)
       profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
       if user_form.is_valid() and profile_form.is_valid():
           user_form.save()
           profile_form.save()
           messages.success(request, 'Your Profile Has been Updated Successfully')
       else:
           messages.error(request, 'Error updating your profile')
           
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
 'profile_form': profile_form}
    return render(request, 'profile/profile_edit.html', context)


@login_required
def profile_delete(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, Ayaah so sorry Koh!')
        return redirect('article:home')
    return render(request, 'users/profile_delete.html')

