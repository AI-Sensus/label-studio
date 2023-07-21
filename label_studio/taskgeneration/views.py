from django.shortcuts import render, redirect
from django.db.models import Q
from subjectannotation.views import parse_subject_presence_annotations
from timeset import TimeRange
from datetime import timedelta

from sensormodel.models import Deployment
from sensordata.models import SensorData, SensorOffset
from subjectannotation.models import SubjectPresence
from taskgeneration.models import TaskPair
from taskgeneration.forms import TaskGenerationForm


def task_generation_page(request):
    taskgenerationform = TaskGenerationForm()
    return render(request, 'taskgeneration.html', {'taskgenerationform':taskgenerationform})

def create_task_pairs(request, project, subject, duration):
    subject_presences = SubjectPresence.objects.filter(project=project, subject=subject)
    file_uploads = subject_presences.values('file_upload').distinct()
    video_sensordata = SensorData.objects.filter(file_upload__in=file_uploads)
    imu_deployments = Deployment.objects.filter(project=project,subject=subject,sensor__sensortype__sensortype='I')
    imu_sensordata = SensorData.objects.filter(sensor__in=imu_deployments.values('sensor'))
    for video in video_sensordata:
        b_dt = video.begin_datetime
        e_dt = video.end_datetime
        subject_presences_video = subject_presences.filter(file_upload=video.file_upload)
        for subj_pres in subject_presences_video:
            b = b_dt + timedelta(seconds=subj_pres.start_time)
            e = e_dt + timedelta(seconds=subj_pres.end_time)
            imu_overlap = []
            for imu in imu_sensordata:
                imu_sensor = imu.sensor
                camera_sensor = video.sensor
                if SensorOffset.objects.filter(sensor_A=camera_sensor,sensor_B=imu_sensor):
                    offset = SensorOffset.objects.filter(sensor_A=camera_sensor,sensor_B=imu_sensor,
                                                        offset_Date__lt=b).order_by('-offset_Date').first().offset
                else:
                    offset = 0
                offset_delta = timedelta(milliseconds=offset)
                begin_inside = Q(begin_datetime__range=(b-offset_delta,e-offset_delta))
                end_inside = Q(end_datetime__range=(b-offset_delta,e-offset_delta))
                begin_out_and_end_over = ~Q(begin_datetime__range=(b-offset_delta,e-offset_delta)) & Q(end_datetime__gte=b-offset_delta)               
                if imu_sensordata.filter(Q(sensor=imu_sensor) & begin_inside|end_inside|begin_out_and_end_over):
                    imu_overlap.append(imu)
                
                


        
        
    
            
        

def create_annotation_data_chunks(request):
    pass

def parse_data_to_task(request):
    pass

def generate_activity_tasks(request, project, subject, duration):
    if request.method == 'POST':
        taskgenerationform = TaskGenerationForm(request.POST)
        if taskgenerationform.is_valid():
            # Get data from Form
            project = taskgenerationform.cleaned_data.get("project")
            subject = taskgenerationform.cleaned_data.get("subject")
            segment_duration = taskgenerationform.cleaned_data.get("segment_duration")
            # Fill SubjectPresence objects
            parse_subject_presence_annotations(request= request,project=project)
            
            create_task_pairs(request= request,project=project, subject=subject, duration=duration)
            
            
        return redirect()

    