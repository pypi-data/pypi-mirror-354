import time

import requests
import os
import json

backend_host_url = os.environ['LOCI_BACKEND_URL']
x_api_key = os.environ['LOCI_API_KEY']


def upload_binary(file_path, version_name, compare_version_id, project_id, platform):
    """
    Uploads a file via POST request

    Args:
        url (str): The API endpoint URL
        file_path (str): Path to the file to upload
        field_name (str): The form field name for the file (default: 'file')
    """
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist")
        return None

    try:
        url = backend_host_url + '/api/v1/reports/xapi-upload'
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

        print("\nServer Response:")

        # Try to parse JSON response
        try:
            json_response = response.json()
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
    try:
        url = backend_host_url + '/api/v1/graph/xapi-project-versions'
        print(f"To URL: {url}")

        headers = {"X-Api-Key": x_api_key}
        values = {'projectId': project_id,
                  'app': 'diag_poc'}

        response = requests.post(url, headers=headers, data=values)


        # Check if request was successful
        response.raise_for_status()

        print("\nServer Response:")

        # Try to parse JSON response
        version_id = ''
        version_date = '0000-00-00'
        try:
            json_response = response.json()
            print(json.dumps(json_response, indent=2))
            for version in json_response['message']:
                if version[0]['properties']['status'] == 0:
                    if version[0]['properties']['end_dt'] > version_date:
                        version_id = version[0]['properties']['version_id']
                        version_date = version[0]['properties']['end_dt']
            return version_id
        except ValueError:
            print(response.text)
            return ""

    except requests.exceptions.RequestException as e:
        print(f"Error error getting latest version id: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ""

def get_versions(project_id):
    try:
        url = backend_host_url + '/api/v1/graph/xapi-project-versions'
        print(f"To URL: {url}")

        headers = {"X-Api-Key": x_api_key}
        values = {'projectId': project_id,
                  'app': 'diag_poc'}

        response = requests.post(url, headers=headers, data=values)


        # Check if request was successful
        response.raise_for_status()

        print("\nServer Response:")

        # Try to parse JSON response
        try:
            json_response = response.json()
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
    try:
        url = backend_host_url + '/api/v1/projects/xapi-list-all'
        print(f"To URL: {url}")

        headers = {"X-Api-Key": x_api_key}

        response = requests.get(url, headers=headers)

        # Check if request was successful
        response.raise_for_status()

        print("\nServer Response:")

        # Try to parse JSON response
        try:
            json_response = response.json()
            print(json.dumps(json_response, indent=2))
            for project in json_response:
                if project['name'] == project_name:
                    return project['id']
            return None
        except ValueError:
            print(response.text)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error getting project id: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def upload_finished(project_id, report_id):
    try:
        url = backend_host_url + '/api/v1/reports/xapi-progress'
        print(f"To URL: {url}")

        values = {'projectId': project_id,
                  'reportId': report_id}

        response = requests.post(url, data=values)

        # Check if request was successful
        response.raise_for_status()

        print("Server Response:")

        # Try to parse JSON respons
        try:
            json_response = response.json()
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


def full_upload(file_path, version_name, platform, project_name, use_latest=True, compare_version_id=''):

    project_id = get_project_id(project_name)
    if project_id is None:
        print("Uploading failed, Project does not exist.")
        exit(-1)

    if use_latest:
        compare_version_id = get_last_version_id(project_id)

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
    while not finished:
        finished, status = upload_finished(project_id, reportId)
        time.sleep(10)

    return status


