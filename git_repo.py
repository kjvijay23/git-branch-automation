import pandas as pd
from github import Github
from datetime import datetime
import logging

# Token that has administrator privilege to access all the repos, can be generated from developer settings
git_access_token = ''


def setup_logging():
    '''
    Configuring logger at info level, writes to a file and console
    '''
    logger = logging.getLogger()
    logpath = 'Git_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.log'
    for handler in logger.handlers:
        logger.removeHandler(handler)
    fh = logging.FileHandler(logpath)
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s-%(lineno)s - message: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)


def branch_protection(repo):
    '''
    Parameters: repo - A Git repository object
    Iterates through branches to apply the branch protection rule for the master branch
    '''
    for branch in repo.get_branches():
        if branch.name == 'master':
            branch.edit_protection(required_approving_review_count=1, strict=True, enforce_admins=True, team_push_restrictions=['admin'])
            logging.info("Enabled protection rule for {} branch in {} repo".format(branch.name, repo.name))
            logging.info("Branch URL {}".format(branch.get_protection().url))
            logging.info("Ensuring restriction - Getting the current teams and users from repo")
            logging.info("Teams - {}".format([i for i in branch.get_team_push_restrictions()]))
            logging.info("Users - {}".format([j for j in branch.get_user_push_restrictions()]))
            logging.info("----------END----------")


def add_teams(org):
    '''
    Parameters: org - A Git object which is intialised with organization
    Iterates through each repository to add admin team as the collaborator and removes all other admin members from the repo
    '''
    team = [i for i in org.get_teams() if i.name == 'Admin'][0]
    logging.info("Retrieved the Admin team API")
    for repo in org.get_repos():
        if not repo.archived:
            logging.info("{}".format(repo.name))
            team.set_repo_permission(repo, 'admin')
            logging.info("Added Admin team to {} repo".format(repo.name))
            for coll in repo.get_collaborators():
                if repo.get_collaborator_permission(coll) == 'admin':
                    repo.remove_from_collaborators(coll.login)
                    logging.info("Removed collaborator {} from {}".format(coll.login, repo.name))
            branch_protection(repo)


def protect_new_repo(org, repo_name):
    team = [i for i in org.get_teams() if i.name == 'Admin'][0]
    repo = org.get_repo(repo_name)
    if not repo.archived:
        logging.info("{}".format(repo.name))
        team.set_repo_permission(repo, 'admin')
        logging.info("Added Admin team to {} repo".format(repo.name))
        for coll in repo.get_collaborators():
            if repo.get_collaborator_permission(coll) == 'admin':
                repo.remove_from_collaborators(coll.login)
                logging.info("Removed collaborator {} from {}".format(coll.login, repo.name))
        branch_protection(repo)


def get_repo_csv(org):
    '''
    Parameters: org - A Git object which is intialised with organizatio
    Iterates through each repository and pulls out repo details like repo is archived, master branch is protected and writes into a CSV
    '''
    df = pd.DataFrame(columns=['Repository', 'IS_ARCHIVED', 'Branch', 'IS_PROTECTED'])
    logging.info("Initialized dataframe and retrieving data from the repos")
    for repo in org.get_repos():
        for branch in repo.get_branches():
            if branch.name == 'master':
                df = df.append(pd.DataFrame([[repo.name, repo.archived, branch.name, branch.protected]], columns=df.columns))
    df = df.reset_index(drop=True)
    df.to_csv("Repositories.csv", index=False)
    logging.info("Got the Repositories.csv")


if __name__ == '__main__':
    git = Github(git_access_token)
    org = git.get_organization('organization_name')
    setup_logging()
    protect_new_repo(org, 'repository_name')
    # add_teams(org)
    # get_repo_csv(org)
