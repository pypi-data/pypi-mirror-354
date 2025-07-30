import os
import gitlab
import base64

class GitLabClient:
    def __init__(self):
        self.url = os.getenv("GITLAB_URL")
        self.token = os.getenv("GITLAB_TOKEN")
        if not self.url or not self.token:
            raise ValueError("GITLAB_URL and GITLAB_TOKEN must be set in environment variables.")
        self.gl = gitlab.Gitlab(self.url, private_token=self.token, ssl_verify=False)

    def get_merge_request(self, project_id, mr_iid):
        return self.gl.projects.get(project_id).mergerequests.get(mr_iid)

    def get_merge_request_diff(self, project_id, mr_iid):
        mr = self.get_merge_request(project_id, mr_iid)
        return mr.diffs.list()

    def post_comment(self, project_id, mr_iid, body):
        mr = self.get_merge_request(project_id, mr_iid)
        return mr.notes.create({'body': body})

    def approve_mr(self, project_id, mr_iid):
        mr = self.get_merge_request(project_id, mr_iid)
        return mr.approve()

    def unapprove_mr(self, project_id, mr_iid):
        mr = self.get_merge_request(project_id, mr_iid)
        return mr.unapprove()

    def add_reviewer(self, project_id, mr_iid, reviewer_ids):
        mr = self.get_merge_request(project_id, mr_iid)
        current_ids = [u['id'] for u in getattr(mr, 'reviewers', [])]
        updated_ids = list(set(current_ids + reviewer_ids))
        updated_data = mr.manager.update(mr.get_id(), {'reviewer_ids': updated_ids, 'title': mr.title})
        if updated_data:
            mr._update_attrs(updated_data)
        return mr

    def get_user_by_username(self, username):
        users = self.gl.users.list(username=username)
        return users[0] if users else None

    def get_project_by_path(self, path):
        return self.gl.projects.get(path)

    def get_merge_request_changes(self, project_id, mr_iid):
        mr = self.get_merge_request(project_id, mr_iid)
        return mr.changes()['changes']

    def get_merge_request_comments(self, project_id, mr_iid):
        mr = self.get_merge_request(project_id, mr_iid)
        return mr.notes.list()

    def list_project_files(self, project_id, path="", recursive=True):
        project = self.gl.projects.get(project_id)
        files = []
        tree = project.repository_tree(path=path, recursive=recursive, all=True)
        for item in tree:
            if item['type'] == 'blob':  # Only include files, not directories
                files.append(item['path'])
        return files

    def get_file_content(self, project_id, file_path, ref="main"):
        project = self.gl.projects.get(project_id)
        f = project.repository_files.get(file_path=file_path, ref=ref)
        return base64.b64decode(f.content).decode('utf-8')

    def list_group_projects(self, group_name):
        group = self.gl.groups.get(group_name)
        projects = group.projects.list(all=True)
        return [
            {
                'id': p.id,
                'name': p.name,
                'path_with_namespace': p.path_with_namespace
            } for p in projects
        ]

    def list_open_merge_requests(self, project_id):
        project = self.gl.projects.get(project_id)
        mrs = project.mergerequests.list(state='opened', all=True)
        return [
            {
                'iid': mr.iid,
                'title': mr.title,
                'state': mr.state,
                'author': getattr(mr.author, 'name', None),
                'web_url': mr.web_url
            } for mr in mrs
        ]

    def list_group_projects_recursive(self, group_name):
        def collect_projects(group):
            projects = [
                {
                    'id': p.id,
                    'name': p.name,
                    'path_with_namespace': p.path_with_namespace
                } for p in group.projects.list(all=True)
            ]
            for subgroup in group.subgroups.list(all=True):
                subgroup_obj = self.gl.groups.get(subgroup.id)
                projects.extend(collect_projects(subgroup_obj))
            return projects
        root_group = self.gl.groups.get(group_name)
        return collect_projects(root_group)

    def list_group_open_merge_requests(self, group_name):
        group = self.gl.groups.get(group_name)
        mrs = group.mergerequests.list(state='opened', include_subgroups=True, all=True)
        return [
            {
                'project_id': mr.project_id,
                'project_name': getattr(mr, 'project_id', None),  # Optionally resolve name if needed
                'iid': mr.iid,
                'title': mr.title,
                'state': mr.state,
                'author': getattr(mr.author, 'name', None),
                'web_url': mr.web_url
            } for mr in mrs
        ] 