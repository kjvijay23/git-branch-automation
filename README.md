## Goal

Enabling **master** branch protection on all the repositories across the organization

## Rules

Ensure the below rules are added for all the repos
- Restrict direct push/commits to master branch 
- Only Owner(s) can create repositories
- Only member(s) of Admin team can access the repository settings
- Pull request to master branch requires atleast 1 reviewers
- Only member(s) of Admin team can merge the pull request

## How it works

* Run the git_repo.py
* Requires Git access token with administrator privilege to access all the repos, can be generated from developer settings

#### Code Flow

![Git_repo](https://user-images.githubusercontent.com/91729608/159126567-ba294119-2d3c-42fb-93de-2509f2e91cbd.png)

#### Tech Stack
  - Python
#### Requirements
| Tool | Version |
| ------ | ------ |
| Python | >3.5 |
| Pandas | 1.0.1 |
| PyGithub | 1.51 |


Run command `pip install -r requirements.txt`. This file contains all the necessary libraries  to run the job.

#### Usage:
```sh
python3 git_repo.py
```