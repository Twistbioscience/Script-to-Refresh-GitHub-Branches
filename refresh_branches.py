import requests
import sys
import json
from datetime import datetime

# Replace with your own access token
ACCESS_TOKEN = 'your-github-token'
GITHUB_API_BASE_URL = 'https://api.github.com'

ORG_NAME = 'Twistbioscience'

REPO_NAMES = [
    'repo1',
    'repo2'
]

#Replace with your source and target branch names
SOURCE_BRANCH = 'staging'
TARGET_BRANCH = 'pdx-uat-b'

def create_branch(repo, new_branch, source_branch):
    url = f'{GITHUB_API_BASE_URL}/repos/{ORG_NAME}/{repo}/git/refs/heads/{source_branch}'
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    source_sha = response.json()['object']['sha']
    url = f'{GITHUB_API_BASE_URL}/repos/{ORG_NAME}/{repo}/git/refs'
    data = {'ref': f'refs/heads/{new_branch}', 'sha': source_sha}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

def create_pull_request(repo, title, source_branch, target_branch):
    url = f'{GITHUB_API_BASE_URL}/repos/{ORG_NAME}/{repo}/pulls'
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}
    data = {'title': title, 'head': source_branch, 'base': target_branch}
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    elif response.status_code == 422:
        return None
    else:
        response.raise_for_status()

def process_repo(repo_name, dry_run=True):
    try:
        today = datetime.today()
        source_clone_name = f'{SOURCE_BRANCH}_clone_{today.month:02d}{today.day:02d}{today.minute:02d}'
        create_branch(repo_name, source_clone_name, SOURCE_BRANCH)
        
        pr_title = f'Refresh {TARGET_BRANCH} with {SOURCE_BRANCH}'
        pull_request = create_pull_request(repo_name, pr_title, source_clone_name, TARGET_BRANCH)

        if pull_request:
            if dry_run:
                return repo_name, pull_request['html_url'], pull_request['diff_url']
            else:
                return repo_name, pull_request['html_url']
        else:
            return repo_name, "No refresh needed"
    except requests.exceptions.RequestException as e:
        print(f'Error processing {repo_name}: {e}', file=sys.stderr)
        return repo_name, "error"

def main():
    dry_run = True
    results = []

    for repo_name in REPO_NAMES:
        result = process_repo(repo_name, dry_run)
        results.append(result)

    for repo_result in results:
        if len(repo_result) == 3:
            repo_name, pr_url, diff_url = repo_result
            print(f'{repo_name}: Diff URL - {diff_url}')
        else:
            repo_name, status = repo_result
            print(f'{repo_name}: {status}')

    if dry_run:
        confirm = input("Do you want to create the pull requests? (y/n): ")
        if confirm.lower() == "y":
            dry_run = False
            confirmed_results = []

            for repo_name in REPO_NAMES:
                result = process_repo(repo_name, dry_run)
                confirmed_results.append(result)

            for repo_name, status in confirmed_results:
                print(f'{repo_name}: {status}')

if __name__ == '__main__':
    main()