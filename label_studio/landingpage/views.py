from django.shortcuts import render, redirect
from django.urls import reverse
import requests
from .forms import CreateProject
from rest_framework.authtoken.models import Token
from projects.models import Project
from .models import MainProject

def landingpage(request, project_id):
    main_project = MainProject.objects.get(project_id=project_id)
    return render(request, 'landingpage.html', {'main_project': main_project})

def homepage(request):
    # Reset main projects
    MainProject.objects.all().delete()
    # Get all projects
    all_projects = Project.objects.all()
    # Loop through projects and only keep projects with names ending on '_dataimport'
    filtered_projects = [project for project in all_projects if project.title.endswith('_dataimport')]

    main_projects = []
    for project in filtered_projects:
        main_project = MainProject(
            project_id=project.id,
            name=project.title[:-11]  # Remove '_dataimport' from the project name
        )
        main_project.save()
        
    main_projects = MainProject.objects.all()
    
    return render(request, 'homepage.html', {'projects': main_projects})

def createProject(request):
    if request.method == 'POST':
        createprojectform = CreateProject(request.POST)
        if createprojectform.is_valid():
            name = createprojectform.cleaned_data['project_name']
            # Get current user token for authentication
            user = request.user
            token = Token.objects.get(user=user)

            # Get url for displaying all projects
            projects_url = request.build_absolute_uri(reverse('projects:api:project-list'))

            ### Create three projects from here
            # Create data import project
            dataimport_title = f'{name}_dataimport'
            dataimport_response = requests.post(
                projects_url,
                headers={'Authorization': f'Token {token}'},
                data={'title': dataimport_title}
            )

            # Create subject annotation project
            subjectannotation_title = f'{name}_subjectannotation'
            subjectannotation_response = requests.post(
                projects_url,
                headers={'Authorization': f'Token {token}'},
                data={'title': subjectannotation_title}
            )

            # Create activity annotation project
            activityannotation_title = f'{name}_activityannotation'
            activityannotation_response = requests.post(
                projects_url,
                headers={'Authorization': f'Token {token}'},
                data={'title': activityannotation_title}
            )

            return redirect('landingpage:homepage')

    else:
        createprojectform = CreateProject()
    
    return render(request, 'createproject.html', {'createprojectform': createprojectform})
