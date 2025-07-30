from ..repos import APIRepo


def get_projects(user):
    repo = APIRepo()
    projects = repo.retrieve_projects(user)
    return [project["name"] for project in projects]


def get_projects_in_workspace(user, workspace):
    repo = APIRepo()
    projects_in_workspace, error = repo.retrieve_projects_in_workspace(user, workspace)
    if error:
        raise Exception("Error retrieving projects in workspace")
    return [project['name'] for project in projects_in_workspace]
