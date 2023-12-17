import datetime
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from .models import Project, ProjectVolunteer, Task, Volunteer, Application
from .forms import ApplicationForm, ProjectForm, RegisterForm, RegisterVolunteerForm, TaskForm


def home(request):
    return render(request, 'main/home.html')

def view_projects(request):
    projects = Project.objects.all()

    if request.method == "POST":
        project_id = request.POST.get("project-id")

        if project_id:
            project = Project.objects.filter(id=project_id).first()
            if project and (project.coordinator == request.user):
                project.delete()

    return render(request, 'main/view_projects.html', {'projects': projects})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/view-projects')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'user_form': form})

@login_required(login_url='/login')
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def sign_up_volunteer(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        volunteer_form = RegisterVolunteerForm(request.POST)
        if user_form.is_valid() and volunteer_form.is_valid():
            user = user_form.save()
            volunteer= volunteer_form.save(commit=False)
            Volunteer.objects.create(
            user_id=user.id,
            location=volunteer.location,
            phone_number=volunteer.phone_number,
        )
            user = User.objects.filter(id=user.id).first()
            group = Group.objects.get(name='volunteer_perms')
            user.groups.add(group)

            login(request, user)
            return redirect('/view-projects')
    else:
        user_form = RegisterForm()
        volunteer_form = RegisterVolunteerForm()
    return render(request, 'registration/sign_up.html', {'user_form': user_form,
                                                         'volunteer_form': volunteer_form})

@login_required(login_url='/login')
@permission_required("main.add_project", login_url="/login", raise_exception=True)
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.coordinator = request.user
            project.save()
            return redirect('/view-projects')
    else:
        form = ProjectForm()
    return render(request, 'main/create_project.html', {'form': form})

@login_required(login_url='/login')
@permission_required("main.add_project", login_url="/login", raise_exception=True)
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.coordinator != request.user:
        return HttpResponseForbidden("You don't have permission to update this project.")

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect('/home')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'main/update_project.html', {'form': form, 'project': project})

def view_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.is_authenticated:
        application = Application.objects.filter(project=project, applicant=request.user).first()
    else:
        application = None
    return render(request, 'main/view_project.html', {'project': project, 'application': application})

def search_project(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''
    projects = Project.objects.filter(name__contains=search_text)
    return render(request, 'main/home.html', {'projects': projects})

@login_required(login_url='/login')
@permission_required("main.add_project", login_url="/login", raise_exception=True)
def view_project_volunteers(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    volunteers = ProjectVolunteer.objects.filter(project=project)
    if request.method == "POST":
        volunteer_id = request.POST.get("volunteer-id")
        if volunteer_id:
            volunteer = ProjectVolunteer.objects.filter(id=volunteer_id).first()
            volunteer.delete()
            return redirect('view_project_volunteers', project_id=project_id)
    return render(request, 'main/view_project_volunteers.html', {'volunteers': volunteers, 'project': project})

@login_required(login_url='/login')
@permission_required("main.add_application", login_url="/login", raise_exception=True)
def create_application(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.project = project
            application.applicant = request.user
            application.application_date = datetime.date.today()
            application.save()
            return redirect('view_project', project_id=project_id)
    else:
        form = ApplicationForm()
    return render(request, 'main/create_application.html', {'form': form, 'project': project})

@login_required(login_url='/login')
@permission_required("main.add_application", login_url="/login", raise_exception=True)
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if application.applicant != request.user:
        return HttpResponseForbidden("You don't have permission to delete this application.")
    application.delete()
    return redirect('view_applications')

@login_required(login_url='/login')
@permission_required("main.add_project", login_url="/login", raise_exception=True)
def view_applications(request):
    user_projects = Project.objects.filter(coordinator=request.user)
    applications = Application.objects.filter(project__in=user_projects)
    return render(request, 'main/view_applications.html', {'applications': applications})

@login_required(login_url='/login')
@permission_required("main.add_project", login_url="/login", raise_exception=True)
def view_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    volunteer = Volunteer.objects.filter(user=application.applicant).first()
    user = volunteer.user
    if request.method == 'POST':
        application_status= request.POST.get("application-status")
        if application_status == "True":
            application.is_approved = True
            application.save()
            ProjectVolunteer.objects.create(
            project=application.project, 
            volunteer=user)
        else:
            application.delete()
        return redirect('view_applications')
    return render(request, 'main/view_application.html', {'application': application, 'volunteer': volunteer})

@login_required(login_url='/login')
@permission_required("main.add_project", login_url="/login", raise_exception=True)
def create_task(request, project_id, user_id):
    project = get_object_or_404(Project, id=project_id)
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.volunteer = user
            task.save()
            return redirect('view_project', project_id=project_id)
    else:
        form = TaskForm()
    return render(request, 'main/create_task.html', {'form': form, 'project': project, 'volunteer': user})

@login_required(login_url='/login')
@permission_required("main.add_application", login_url="/login", raise_exception=True)
def view_tasks_volunteer(request):
    user = request.user
    tasks = Task.objects.filter(volunteer=user)
    return render(request, 'main/view_tasks_volunteer.html', {'tasks': tasks})

@login_required(login_url='/login')
@permission_required("main.add_project", login_url="/login", raise_exception=True)
def view_project_tasks(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)
    return render(request, 'main/view_project_tasks.html', {'tasks': tasks})

@login_required(login_url='/login')
def view_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'main/view_task.html', {'task': task})

def support_project(request):
    return render(request, 'main/support_project.html')
