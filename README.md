## M-MOVE-IT: Multimodal Machine Observation and Video-Enhanced Integration Tool for Data Annotation

AI-Sensus has been built on the open source data labeling tool Label Studio (LS). The 1.4.1 version of Label Studio was forked and extra features were added to this version. The workflow overview, project management and sensor data parsing were thereafter improved.

The version of LS is important. We use an older version because this version still supports a ‘hack’ that allows time series being synchronized with videos when annotating. The way this feature works will be explained later in this documentation. What is important for now is that by upgrading the fork of LS to a version higher than v1.4.1 one disables this functionality.

### Set up local project for development
```bash
# Set-up virtual environment (python v3.10)
pip install virtualenv (only if not yet installed virtualenv)
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

