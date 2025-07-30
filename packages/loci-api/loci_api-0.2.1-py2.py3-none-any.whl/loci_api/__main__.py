import sys

from loci_api import api_helper

def print_usage():
    print("""
    Usage: 
        loci_api <command> <args...>
    
    Available Commands:
        loci_api upload <path-to-binary> <project-name> <new-version-name> [compare_version_name]
        loci_api upload_last <path-to-binary> <project-name> <new-version-name>
        loci_api list_versions <project-name>
        loci_api last_version <project-name>
        loci_api list_projects

    """)
    exit(-1)

if len(sys.argv) < 2:
    print_usage()
    sys.exit(0)

# input params

command = sys.argv[1]

if command == 'upload':
    if (len(sys.argv) < 5):
        print("Missing arguments")
        print_usage()

    file_path = sys.argv[2]
    project_name = sys.argv[3]
    version_name = sys.argv[4]
    compare_version_id = ''
    if len(sys.argv) > 5:
        compare_version_name = sys.argv[5]
        project_id, _ = api_helper.get_project_id(project_name)
        versions = api_helper.get_versions(project_id)
        for version in versions:
            if compare_version_name == version['properties']['version_name']:
                compare_version_id = version['properties']['version_id']

    status = api_helper.full_upload(file_path, version_name, project_name, use_latest=False, compare_version_id=compare_version_id)
    exit(status)
elif command == 'upload_last':
    if len(sys.argv) < 5:
        print("Missing arguments")
        print_usage()

    file_path = sys.argv[2]
    project_name = sys.argv[3]
    version_name = sys.argv[4]
    status = api_helper.full_upload(file_path, version_name, project_name, use_latest=True, compare_version_id='')
    exit(status)
elif command == 'list_versions':
    if len(sys.argv) < 3:
        print("Missing arguments")
        print_usage()

    project_name = sys.argv[2]
    project_id, _ = api_helper.get_project_id(project_name)
    versions = api_helper.get_versions(project_id)
    version_names = []
    for version in versions:
        version_names.append(version['properties']['version_name'])
    print('"' + '","'.join(version_names) + '"')
    exit(0)
elif command == 'last_version':
    if len(sys.argv) < 3:
        print("Missing arguments")
        print_usage()

    project_name = sys.argv[2]
    project_id, _ = api_helper.get_project_id(project_name)
    version_id, version_name = api_helper.get_last_version_id(project_id)
    print('"' + version_name + '"')
    exit(0)
elif command == 'list_projects':
    projects = api_helper.get_projects()
    project_names = []
    for project in projects:
        project_names.append(project['name'])
    print('"' + '","'.join(project_names) + '"')
else:
    print_usage()
    exit(0)