from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, RegForm,ChangeUserForm
from django.contrib.auth.models import User
from blog0315.models import Profile
from django.contrib.auth.forms import UserCreationForm


def user_message(requset):
    user = requset.user
    context = {}
    context['user'] = user
    return render(requset, 'users/user_imf.html', context)


def user_change(request):
    # if request.method != 'POST':
    #     # 未提交数据：创建一个新表单
    #     form = UsermesForm()
    # else:
    #     # POST提交的数据,对数据进行处理
    #     form = UsermesForm(request.POST)
    #     if form.is_valid():
    #         user_mess = form.save(commit=False)
    #         user_mess.user = request.user
    #         user_mess.save()
    #         return HttpResponseRedirect(reverse('blog0315:index'))
    redirect_to = request.GET.get('from', reverse('blog0315:index'))

    if request.method == 'POST':
        form = ChangeUserForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            logo_new = form.cleaned_data['logo_new']
            tel_new = form.cleaned_data['tel_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            if nickname_new != '':
                profile.nickname = nickname_new
            if logo_new != '':
                profile.logo = logo_new
            if tel_new != '':
                profile.telephone = tel_new
            profile.save()
            return redirect(redirect_to)
        pass
    else:
        form = ChangeUserForm()

    context = {}
    context['changeuserform'] = form
    return render(request, 'users/user_mes.html', context)


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('blog0315:index')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            if email == '':
                email = '记得添加邮箱哟'
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username,email, password)
            user.save()
            # 登录用户
            # user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('blog0315:index')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'users/register.html', context)
# def login_view(request):
#     """登陆"""
#     if request.method == 'GET':
#         return render(request, 'users/login.html')
#
#     username = request.POST.get('username', '')
#     password = request.POST.get('password', '')
#
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect(reverse('blog0315:index'))
#     else:
#         return render(request, 'users/login.html', {
#             'username': username,
#             'password': password,
#         })


def logout_view(request):
    """注销用户"""
    logout(request)
    return HttpResponseRedirect(reverse('blog0315:index'))


# def register(request):
#     """注册新用户"""
#     if request.method != 'POST':
#         # 显示空的注册表单
#         form = UserCreationForm()
#     else:
#         # 处理填写好的表单
#         form = UserCreationForm(data=request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             #  让用户自动登录，再重定向到主页
#             authenticated_user = authenticate(username=new_user.username,
#             password=request.POST['password1'])
#             login(request, authenticated_user)
#             return HttpResponseRedirect(reverse('blog0315:index'))
#     context = {'form': form}
#     return render(request, 'users/register.html', context)

# Create your views here.
