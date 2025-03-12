from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile, Job
from .forms import JobForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
            username=cd['username'],
            password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})



@login_required
def dashboard(request):
    return render(request,
                'account/dashboard.html',
                {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя,
            # но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохранить объект User
            new_user.save()

            #создаем профиль и записываем роль
            role = user_form.cleaned_data['role']
            Profile.objects.create(user=new_user, role=role)

            return render(request,'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})


def is_employer(user):
    if not user.is_authenticated:
        return False
    return Profile.objects.get(user=user).role == 'employer'

@login_required
@user_passes_test(is_employer)  # Ограничиваем доступ только для работодателей
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user  # Привязываем вакансию к работодателю
            job.save()
            return redirect('job_list')  # Перенаправляем на список вакансий
    else:
        form = JobForm()
    return render(request, 'jobs/create.html', {'form': form})


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/list.html', {'jobs': jobs})
