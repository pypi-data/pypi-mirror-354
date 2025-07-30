import time

import requests
import os
import json

if 'LOCI_BACKEND_URL' not in os.environ:
    print("ERROR: LOCI_BACKEND_URL not set.")
    exit(-1)
if 'LOCI_API_KEY' not in os.environ:
    print("ERROR: LOCI_API_KEY not set.")
    exit(-1)
backend_host_url = os.environ['LOCI_BACKEND_URL']
x_api_key = os.environ['LOCI_API_KEY']
debug = False if "LOCI_API_DEBUG" not in os.environ else os.environ['LOCI_API_DEBUG'] == 'true'


def upload_binary(file_path, version_name, compare_version_id, project_id, platform):
    """
    Uploads a file via POST request

    Args:
        file_path (str): Path to the file to upload
        version_name (str): the version name of the new version to be created
        compare_version_id (str): the version id against which we compare the new binary, if empty no comparison will be made
        project_id (str): the project id of the project for which we are creating the version
        platform (str): the platform of the new version (ARM|TRICORE)

    Returns:
        report_id: report id of the new report comparing the new version vs the compare_version
    """
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist")
        return None

    try:
        url = backend_host_url + '/api/v1/reports/xapi-upload'
        if debug:
            print(f"Uploading file: {file_path}")
            print(f"To URL: {url}")

        # Open the file in binary mode and send the request

        files = {'binaryFile': (file_path, open(file_path, 'rb'), 'application/octet-stream')}
        values = {'versionName': version_name,
                  'compareVersionId': compare_version_id,
                  'projectId': project_id,
                  'platform': platform}
        headers = {"X-Api-Key": x_api_key}

        response = requests.post(url, files=files, headers=headers, data=values)


        # Check if request was successful
        response.raise_for_status()

        if debug:
            print("\nServer Response:")

        # Try to parse JSON response
        try:
            json_response = response.json()
            if debug:
                print(json.dumps(json_response, indent=2))
            return json_response['eventDetails']['reportId']
        except ValueError:
            print(response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"Error uploading file: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def get_last_version_id(project_id):
    """
    Gets the version id of the latest valid version uploaded for the project

    Args:
        project_id (str): the project id for which we are getting the latest version

    Returns:
        version_id (str): the version id of the latest valid version uploaded for the project or '' if not found
        version_name (str): the version name of the latest valid version uploaded for the project

    """
    try:
        url = backend_host_url + '/api/v1/graph/xapi-project-versions'
        if debug:
            print(f"To URL: {url}")

        headers = {"X-Api-Key": x_api_key}
        values = {'projectId': project_id,
                  'app': 'diag_poc'}

        response = requests.post(url, headers=headers, data=values)


        # Check if request was successful
        response.raise_for_status()

        if debug:
            print("\nServer Response:")

        # Try to parse JSON response
        version_id = ''
        version_name = ''
        version_date = '0000-00-00'
        try:
            json_response = response.json()
            if debug:
                print(json.dumps(json_response, indent=2))
            for version in json_response['message']:
                if version[0]['properties']['status'] == 0:
                    if version[0]['properties']['end_dt'] > version_date:
                        version_id = version[0]['properties']['version_id']
                        version_name = version[0]['properties']['version_name']
                        version_date = version[0]['properties']['end_dt']
            return version_id, version_name
        except ValueError:
            print(response.text)
            return "", ""

    except requests.exceptions.RequestException as e:
        print(f"Error error getting latest version id: {e}")
        return "", ""
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "", ""

def get_versions(project_id):
    """
    Returns list of all version objects for the project

    Args:
        project_id (str): the projects id for which we are getting the version objects

    Returns:
        versions ([Object]): list of version objects for the project or [] if none found

    """
    try:
        url = backend_host_url + '/api/v1/graph/xapi-project-versions'
        if debug:
            print(f"To URL: {url}")

        headers = {"X-Api-Key": x_api_key}
        values = {'projectId': project_id,
                  'app': 'diag_poc'}

        response = requests.post(url, headers=headers, data=values)


        # Check if request was successful
        response.raise_for_status()

        if debug:
            print("\nServer Response:")

        # Try to parse JSON response
        try:
            json_response = response.json()
            if debug:
                print(json.dumps(json_response, indent=2))
            versions = []
            for version in json_response['message']:
                versions.append(version[0])
            return versions
        except ValueError:
            print(response.text)
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error error getting latest version id: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def get_project_id(project_name):
    """
    Returns the project id for the project with the given project name

    Args:
        project_name (str): the name of the project we are searching

    Returns:
        project_id (str): project id for the matched project or '' if not found

    """
    try:
        url = backend_host_url + '/api/v1/projects/xapi-list-all'
        if debug:
            print(f"To URL: {url}")

        headers = {"X-Api-Key": x_api_key}

        response = requests.get(url, headers=headers)

        # Check if request was successful
        response.raise_for_status()

        if debug:
            print("\nServer Response:")

        # Try to parse JSON response
        try:
            json_response = response.json()
            if debug:
                print(json.dumps(json_response, indent=2))
            for project in json_response:
                if project['name'] == project_name:
                    return project['id'], project['architecture']
            return None, None
        except ValueError:
            print(response.text)
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error getting project id: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None

def get_projects():
    """
    Returns list of all project objects for the company

    Args:

    Returns:
        projects ([Object]): list of project objects for the company

    """
    try:
        url = backend_host_url + '/api/v1/projects/xapi-list-all'
        if debug:
            print(f"To URL: {url}")

        headers = {"X-Api-Key": x_api_key}

        response = requests.get(url, headers=headers)

        # Check if request was successful
        response.raise_for_status()

        if debug:
            print("\nServer Response:")
        projects = []
        # Try to parse JSON response
        try:
            json_response = response.json()
            if debug:
                print(json.dumps(json_response, indent=2))
            for project in json_response:
                projects.append(project)
            return projects
        except ValueError:
            print(response.text)
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error getting project id: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def upload_finished(project_id, report_id):
    """
    Checks the status of the report with given report id

    Args:
        project_id (str): the projects id for which the report was created
        report_id (str): the report id of the report we are uploading

    Returns:
        (finished, status) (boolean, int): returns the status of the upload

    """
    try:
        url = backend_host_url + '/api/v1/reports/xapi-progress'
        if debug:
            print(f"To URL: {url}")

        values = {'projectId': project_id,
                  'reportId': report_id}

        response = requests.post(url, data=values)

        # Check if request was successful
        response.raise_for_status()

        if debug:
            print("Server Response:")

        # Try to parse JSON respons
        try:
            json_response = response.json()
            if debug:
                print(json.dumps(json_response, indent=2))
            status = json_response['progress']['status']

            if status == 1 or status == 0:
                return (True, status)
            else:
                return (False, None)

        except ValueError:
            print(response.text)
            return (True, 0)

    except requests.exceptions.RequestException as e:
        print(f"Error error getting latest version id: {e}")
        return (True, 0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return (True, 0)


def full_upload(file_path, version_name, project_name, use_latest=True, compare_version_id=''):

    project_id, platform = get_project_id(project_name)
    if project_id is None:
        print("Uploading failed, Project does not exist.")
        exit(-1)

    if use_latest:
        compare_version_id, _ = get_last_version_id(project_id)

    reportId = upload_binary(file_path, version_name, compare_version_id, project_id, platform)

    if reportId != '':
        print(
            f"Uploaded binary Report ID: {reportId}, Compare Version ID: {compare_version_id}, Project ID: {project_id}"
        )
    else:
        print("Uploading failed, See previous message for more details.")
        exit(-1)

    finished = False
    status = 0

    print("Waiting for processing to finish")
    tries = 0
    while not finished:
        time.sleep(10)
        finished, status = upload_finished(project_id, reportId)
        if tries > 360:
            finished = True
            print("Processing not finished after 60 minutes. Please manually check status on the Loci Platform.")
            exit(-1)

    return status


