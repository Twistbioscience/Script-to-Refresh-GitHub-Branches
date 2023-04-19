# GitHub Branch Refresh Script

This Python script helps you create branches and pull requests to update/refresh a target branch with a source branch in multiple repositories under a GitHub organization.

## Setup

Before using the script, you need to generate a GitHub access token and add it to the script.

### Generating a GitHub Access Token

1. Go to your GitHub settings page: https://github.com/settings/tokens
2. Click "Generate new token."
3. Enter a descriptive name for the token in the "Note" field.
4. Under the "Select scopes" section, check the `repo` box to grant full control of private repositories.
5. Click "Generate token" at the bottom of the page.
6. You will need to authorize your PAT with the Twist SSO
7. Copy the generated token.

### Adding the Access Token to the Script

1. Open the Python script file.
2. Replace the placeholder value `'your_access_token_here'` with the actual access token you generated in the previous step:

```python
ACCESS_TOKEN = 'your_actual_access_token_here'
```

### Customizing the Script
1. Update the ORG_NAME variable with the name of your GitHub organization:

```python
ORG_NAME = 'your_organization_name_here'
```

2. Replace the existing list of repository names in the REPO_NAMES variable with your own repositories:
```python
REPO_NAMES = [
    'your_repo_name_1_here',
    'your_repo_name_2_here',
    'your_repo_name_3_here',
    # ...
]
```

3. Set the SOURCE_BRANCH and TARGET_BRANCH variables to the appropriate branch names:

```python
SOURCE_BRANCH = 'source_branch_name_here'
TARGET_BRANCH = 'target_branch_name_here'

```

### Running the Script
1. Make sure you have Python 3 installed on your machine.
2. Install the requests library if you haven't already:

```
pip install requests

```

3. Run the script 
```
python refresh_branches.py

```
or 
```
python3 refresh_branches.py

```

The script will create branches and pull requests for each repository in the REPO_NAMES list. The output will include the repository name along with the pull request link or "no refresh needed" status.

### Understanding the script output 
```
repo_name_1: https://github.com/your_organization_name_here/repo_name_1/pull/123
repo_name_2: no refresh needed
repo_name_3: https://github.com/your_organization_name_here/repo_name_3/pull/124

```

In this example, the script created a pull request for repo_name_1 and repo_name_3 and provided their links. For repo_name_2, there were no changes to merge, so the output shows "no refresh needed."

Please note that the actual pull request URLs and the number of repositories in the output will depend on your organization and repository settings.


### Troubleshooting
If you encounter any errors, double-check that you have entered the correct organization name, repository names, branch names, and access token in the script. Make sure your access token has the necessary permissions (e.g., repo access) to perform the required operations. If you are still facing issues, ensure that you have the required permissions to access the repositories, branches, and create pull requests within the organization.


