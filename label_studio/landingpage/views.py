from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import requests
from . forms import CreateProject
from rest_framework.authtoken.models import Token

def landingpage(request):
    return render(request, 'landingpage.html')

def createProject(request):
    if request.method == 'POST':
        createprojectform = CreateProject(request.POST)
        if createprojectform.is_valid():
            name = createprojectform.cleaned_data['project_name']
            #description = createprojectform.cleaned_data['optional_description']
            
            # Get current user token for authentication
            user = request.user
            token = Token.objects.get(user=user)

            # Get url for displaying all projects
            projects_url = request.build_absolute_uri(reverse('projects:api:project-list'))

            ### Create three projects from here
            # Create data import project
            #requests.post(projects_url, headers={'Authorization': f'Token {token}'}, data={'title':})
            

        return redirect('landingpage:landingpage')
    
    else:
        createprojectform = CreateProject(request.POST)
    
    return render(request, 'createproject.html', {'createprojectform':createprojectform})