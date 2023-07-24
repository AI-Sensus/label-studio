from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SubjectAnnotationForm
from .utils.annotationtemplate import createSubjectAnnotationTemplate
import requests
from rest_framework.authtoken.models import Token
from sensormodel.models import Subject

# Create your views here.
def annotationtaskpage(request):
    subjectannotationform = SubjectAnnotationForm()
    return render(request, 'annotationtaskpage.html', {'subjectannotationform':subjectannotationform})

def createannotationtask(request):
    # Functions that creates an API call to create a task with subjects as labels for subject annotation
    if request.method == 'POST':
        subjectannotationform = SubjectAnnotationForm(request.POST, request.FILES)
        if subjectannotationform.is_valid():
            # Get the dataimport project name from the form
            selected_project = subjectannotationform.cleaned_data.get("project")
                        
            # Retrieve the subject list
            subjects = Subject.objects.all()
            
            # Create labels for subject annotation
            labels = ", ".join([f"Subject: {subject.name}" for subject in subjects])
            
            # Get url for displaying all projects
            projects_url = request.build_absolute_uri(reverse('projects:api:project-list'))
            
            # Get current user token for authentication
            user = request.user
            token = Token.objects.get(user=user)

            # Get ID of project
            list_projects_response = requests.get(projects_url, headers={'Authorization': f'Token {token}'})
            projects = list_projects_response.json()["results"]
            
            project_id = selected_project.id
            
            if project_id is not None:
                project_id += 1
                
                title = None
                for project in projects:
                    
                    if project["id"] == project_id:
                        title = project["title"]
                        break
                if title == None:
                    # error for not finding subjectannotation project
                    raise ValueError(f'Could not find subject annotation project {title}')
                # Create a XML markup for annotatings
                template = createSubjectAnnotationTemplate(labels)

                # Get url for displaying project detail
                project_detail_url = request.build_absolute_uri(reverse('projects:api:project-detail', args=[project_id]))

                # Create tasks using LS API
                requests.patch(project_detail_url, headers={'Authorization': f'Token {token}'}, data={'label_config':template})

                return redirect('landingpage:landingpage')
            
            else:
                # Handle the case when the project with project_name was not found
                raise ValueError(f"No project found with the provided project_name: {selected_project.title}")
            
    subjectannotationform = SubjectAnnotationForm()
    return render(request, 'annotationtaskpage.html', {'subjectannotationform':subjectannotationform})