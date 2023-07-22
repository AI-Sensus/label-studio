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
    # Load data for given project and subject
    subject_presences = SubjectPresence.objects.filter(project=project, subject=subject)
    file_uploads = subject_presences.values('file_upload').distinct() # Get all unique files that contain subject
    video_sensordata = SensorData.objects.filter(file_upload__in=file_uploads)
    # Load IMU deployments in the project that contain the subject
    imu_deployments = Deployment.objects.filter(project=project,subject=subject,sensor__sensortype__sensortype='I')
    imu_sensordata = SensorData.objects.filter(sensor__in=imu_deployments.values('sensor')) # find all imu sensordata that has a sensor in imu_deployments
    # Iterate over unique video sensordata objects, this reduces computations
    for video in video_sensordata:
        b_dt = video.begin_datetime #begin_datetime video sensordata
        e_dt = video.end_datetime #end_datetime video sensordata
        # Iterate over all subject_presences for this video
        subject_presences_video = subject_presences.filter(file_upload=video.file_upload)
        for subj_pres in subject_presences_video:
            b = b_dt + timedelta(seconds=subj_pres.start_time) #begin_datetime of annotation
            e = e_dt + timedelta(seconds=subj_pres.end_time) #end_datetime of annotation
            imu_overlap_list = []
            # Iterate over imu sensordata of imu's that have been deployed with subject
            for imu in imu_sensordata:
                imu_sensor = imu.sensor
                camera_sensor = video.sensor
                # Check if there is an offset between camera and IMU
                if SensorOffset.objects.filter(sensor_A=camera_sensor,sensor_B=imu_sensor):
                    # Take the latest instance of offset before the begin_datetime of the video sensordata
                    offset = SensorOffset.objects.filter(sensor_A=camera_sensor,sensor_B=imu_sensor,
                                                        offset_Date__lt=b_dt).order_by('-offset_Date').first().offset
                else:
                    # If there is no SensorOffset defined set offset=0
                    offset = 0
                offset_delta = timedelta(milliseconds=offset) # Difference in datetime because of sensor offset
                # Check if there is any overlap whatsoever
                begin_inside = Q(begin_datetime__range=(b-offset_delta,e-offset_delta))
                end_inside = Q(end_datetime__range=(b-offset_delta,e-offset_delta))
                begin_out_and_end_over = ~Q(begin_datetime__range=(b-offset_delta,e-offset_delta)) & Q(end_datetime__gte=b-offset_delta)
                # if begin_inside:
                #     start_overlap = begin_datetime-offset_delta
                #     if end_inside:
                #         end_overlap = 
                            
                if imu_sensordata.filter(Q(sensor=imu_sensor) & begin_inside|end_inside|begin_out_and_end_over):
                    imu_overlap_list.append(imu)
            # for imu in imu_overlap:
                

            # choose imu sensordata for task (longest overlap)
            # (end-start)//duration = nr of segments
            # create TaskPairs
                
                


        
        
    
            
        

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

    