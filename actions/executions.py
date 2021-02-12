from jira import JIRA

jac=None


if jac==None:
    jac = JIRA('https://tools.publicis.sapient.com/jira',auth=('USERNAME','PASSWORD'))

    

def get_projects():
    global jac
    projects = jac.projects()
    projects_dict={p.id:p.name for p in projects}
    return projects_dict

def get_issues(project):
    all_proj_issues = jac.search_issues('project={} and assignee = currentUser()'.format(project))
    issue_keys=[keys.key for keys in all_proj_issues]
    return issue_keys



def get_issue_detail(issue_id):
    issue = jac.issue(issue_id)
    print("getting issue details for {}".format(issue_id))
    issue_detail={'summary':issue.fields.summary,
                  'status':issue.fields.status.name,
                  'assignee':issue.fields.assignee.displayName
                  }
    issue_detail_list=[{"title":issue.fields.summary,"status":issue.fields.status.name,"assignee":issue.fields.assignee.displayName,"type":"jira"}]
    return issue_detail_list
    
    
def create_issue(project,summary,description,assginee):

    new_issue = jac.create_issue(project=project, summary=summary,
                              description=description, issuetype={'name': 'Story'})
    jac.assign_issue(new_issue, assginee)

    return new_issue.key
    
    
    
if __name__ == '__main__':
    issue_dict = {
    'project': {'id': 60502},
    'summary': 'New issue from jira_manager-python',
    'description': 'Look into this one',
    'issuetype': {'name': 'Bug'},
    }
    create_issue(issue_dict)
    get_projects()