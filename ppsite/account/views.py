from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile, Job, Response
from django.contrib.postgres.search import SearchVector
from .forms import JobForm, SearchForm, ResponseForm, ResponseStatusForm
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError
from django.core.exceptions import ValidationError


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


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Job.objects.annotate(
            search=SearchVector('title', 'description'),
        ).filter(search=query)
    return render(request, 'jobs/search.html', {'form': form,
                                                     'query': query,
                                                     'results': results})

@login_required
def my_jobs(request):
    if request.user.profile.role != 'employer':  # Проверяем, что это работодатель
        return render(request, 'error.html', {'message': 'У вас нет доступа к этой странице'})
    
    jobs = Job.objects.filter(employer=request.user)  # Получаем только его вакансии
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)  # Проверяем владельца

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')  # Возвращаем работодателя к списку его вакансий
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)  # Проверяем владельца

    if request.method == "POST":
        job.delete()
        return redirect('job_list')

    return render(request, 'jobs/delete_job.html', {'job': job})


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user == job.employer:
        return redirect('job_list')  # Работодатель не может откликаться

    if Response.objects.filter(student=request.user, job=job).exists():
        return redirect('job_list')  # Уже откликался

    if request.method == 'POST':
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid():
            response = form.save(commit=False)
            response.student = request.user
            response.job = job
            response.save()
            return redirect('job_list')  # После отклика перенаправляем на список вакансий
    else:
        form = ResponseForm()

    return render(request, 'jobs/apply.html', {'form': form, 'job': job})

@login_required
def employer_responses(request):
    jobs = Job.objects.filter(employer=request.user)
    responses = Response.objects.filter(job__in=jobs)

    return render(request, 'jobs/employer_responses.html', {'responses': responses})

@login_required
def student_responses(request):
    responses = Response.objects.filter(student=request.user)
    return render(request, 'jobs/student_responses.html', {'responses': responses})

@login_required
def update_response_status(request, response_id):
    response = get_object_or_404(Response, id=response_id)

    # Проверяем, что работодатель изменяет только свои вакансии
    if response.job.employer != request.user:
        return redirect('job_list')

    if request.method == "POST":
        form = ResponseStatusForm(request.POST, instance=response)
        if form.is_valid():
            form.save()
            return redirect('employer_responses')
    else:
        form = ResponseStatusForm(instance=response)

    return render(request, 'jobs/update_response_status.html', {'form': form, 'response': response})


from django.shortcuts import render, get_object_or_404
from .models import Job

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

