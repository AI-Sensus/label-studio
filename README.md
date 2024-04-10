## M-MOVE-IT: Multimodal Machine Observation and Video-Enhanced Integration Tool for Data Annotation

AI-Sensus has been built on the open source data labeling tool Label Studio (LS). The 1.4.1 version of Label Studio was forked and extra features were added to this version. The workflow overview, project management and sensor data parsing were thereafter improved.

The version of LS is important. We use an older version because this version still supports a ‘hack’ that allows time series being synchronized with videos when annotating. The way this feature works will be explained later in this documentation. What is important for now is that by upgrading the fork of LS to a version higher than v1.4.1 one disables this functionality.

### Set up local project for development
```bash
# Set-up virtual environment (python v3.10)
pip install virtualenv #(only if not yet installed virtualenv)
python -m venv <venv-name>
<venv-name>/Scripts/activate
# Clone the repository
git clone https://github.com/AI-Sensus/label-studio
# Go to the directory label-studio
cd label-studio
# Install all package dependencies
pip install -e .
# Run database migrations. This creates the database for Django
python label_studio/manage.py migrate
# Configure the static files from the React project
python label_studio/manage.py collectstatic
# Run the server locally at http://localhost:8080
python label_studio/manage.py runserver
```
After setting up the local development project, sign up for label-studio at the first webpage when running the app.

### Apply frontend changes

The frontend part of Label Studio app lies in the `frontend/` folder and written in React JSX. In case you've made some changes there, the following commands should be run before building / starting the instance:

```
cd label_studio/frontend/
npm ci
npx webpack
cd ../..
python label_studio/manage.py collectstatic --no-input
```

### Django
Label Studio has been built using the Django framework. We keep our additions separate from the code from LS. Django allows this by making use of apps for different functionalities of the web app. All of our work is the following apps: landingpage, sensormodel, sensordata, subjectannoation, taskgeneration. To integrate these apps in the functionality of the complete project adjustments have been made in the ‘core’ app. These can be found in ‘core/urls.py’ and ‘core/settings/base.py’.

### Landingpage
The ‘landingpage’ app handles the overview of all projects, this is called the dashboard. Also, it handles the project pages of all the projects. Here one can find all functionality explained in the steps one should take.

When one creates a project in the dashboard in the backend four LS subprojects are created per project. An LS project is what one normally would use in LS to upload, annotate and export. LS shows all the data in a project all the time and allows for one annotation setup per project. However since we cut up the files and use annotation for several use cases we chose to use the project structure from LS for our data management and create several LS projects per AI Sensus project. The AI Sensus projects are stored as django models. It creates the following LS projects: data import, subject annotation, activity  annotation. It also handles the exportation of a project when finished by exporting all annotations as a JSON file together with the corresponding data files. 

The ‘landingpage’ app contains the static files used by the AI Sensus html pages. These are stored in ‘landingpage/static/main.css’.

### Sensormodel
The ‘sensormodel’ app handles all the used sensors, subject and the relationships between these per project. It stores them as objects in this model and uses a ForeignKey relationship with the project to make sure all sensors and subjects are related to a certain project. It contains the following models: Sensor, SensorType, Subject and Deployment. The view methods handle adding, adjusting and deleting sensors, subjects and deployments. SensorTypes contain information for specific sensors that is necessary for parsing the data. SensorTypes are different since they are stored in label-studio/sensortypes as .yaml files and are parsed to django models by the method sync_sensor_parser_templates(). This method checks for updates in the files in the label-studio/sensortypes folder and adds or updates the SensorType objects accordingly.

### Sensordata
The ‘sensordata’ app handles all imported sensor data and stores them into the ‘dataimport’ subproject. It extracts all data files from an uploaded zip file and parses the sensor information from the data. It then creates a LS object Sensordata for all files. The uploaded zip file should contain only files from the same sensor.

The ‘sensordata’ app also handles the offsets between sensors. When a project is created, a subproject ‘offsetannotation’ is created. This project is used to annotate the offset between overlapping data from different sensors and these offsets are stored in Django objects. For more information on offset annotation see ‘Efficient Synchronization of Video and IMU Data for Activity Recognition’.

### Subjectannotation
The ‘subjectannotation’ app handles the ‘subjectannotation’ subproject and creates annotation labels from all project subjects. The mp4 data is converted into annotation tasks inside this subproject. The subject presence annotations are automatically parsed into SubjectPresence objects when generating activity annotation tasks in the ‘taskgeneration’ app. The parsing method is in the ‘subjectannotation’ app. 

### Taskgeneration
The ‘taskgeneration’ app generates tasks by selecting all data where the input subject is present and slicing it in segments of a chosen length. The mp4 and csv data are synchronized using the SensorOffset objects. Using the offset and the datetimes that were parsed when uploading sensor data it is possible to determine the overlap two SensorData objects really have. These are stored as SensorOverlap objects. Using these objects and a user-chosen segment length, segments can be cut up, uploaded and tasks can be generated. 

### Time series and video annotation: Synchronization trick
The power of the AI Sensus annotation tool is the ability to annotate several sensor modes at the same time and have them synchronized. LS does not offer this functionality. An old post on the LS site, that has now been deleted (it has been replaced on the site 2024-03-12), shows a way to allow synchronization between a time series and a video. As has been said earlier, this functionality has been removed from LS in versions later than 1.4.1. Therefore sticking to this version is important. 

The synchronization works one way. This means that changing the timestamp of the timeseries moves the timestamp of the video, but changing the timestamp of the video does not move the timestamp of the timeseries.

[Click here for more explanation](https://labelstud.io/guide/ts+video.html)

### LABEL-STUDIO
If you're interested in exploring the original README for Label Studio, you can [click here.](LABEL-STUDIO.md) It contains detailed information about the original Label Studio software and its features.
