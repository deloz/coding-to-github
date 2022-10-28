import json
import math
import os
import re
import shutil

import requests
from github import Github

# 申请token visit this url: https://github.com/settings/tokens
GITHUB_TOKEN = 'github-token'
CODING_TOKEN = 'coding-token'

coding_repo_list = []


def coding_request(params):
    r = requests.post('https://e.coding.net/open-api', headers={
        'Authorization': 'token {}'.format(CODING_TOKEN),
    }, data=json.dumps(params))

    return r.json()


def query_coding(repo_save_dir, page=1):
    print('current coding project page: {}'.format(page))

    result = coding_request({
        'Action': 'DescribeCodingProjects',
        'PageNumber': page,
        'PageSize': 100,
    })

    total_count = result['Response']['Data']['TotalCount']

    for project in result['Response']['Data']['ProjectList']:
        repo_info = coding_request({
            'Action': 'DescribeProjectDepotInfoList',
            'ProjectId': project['Id'],
        })

        for repo in repo_info['Response']['DepotData']['Depots']:
            project_repo_name = '{}-{}'.format(project['Name'], repo['Name'])
            coding_repo_list.append({
                'repo_name': repo['Name'],
                'repo_ssh_url': repo['SshUrl'],
                'repo_description': re.sub("[\n\t\b]", '', repo['Description']),
                'project_name': project['Name'],
                'project_archived': project['Archived'],
                'project_repo_name': project_repo_name,
            })
            os.system('git -C {} clone {} {}'.format(repo_save_dir, repo['SshUrl'], project_repo_name))
            print('clone to local OK: {}'.format(project_repo_name))

    total_page = math.ceil(total_count / 100)
    if total_page > page:
        query_coding(repo_save_dir, page + 1)


if __name__ == '__main__':
    current_dir = os.getcwd()
    repos_dir = '{}/repos'.format(current_dir)

    print('remove directory: {}'.format(repos_dir))
    shutil.rmtree(repos_dir)

    print('create directory: {}'.format(repos_dir))
    os.mkdir(repos_dir)

    query_coding(repo_save_dir=repos_dir)

    g = Github(GITHUB_TOKEN)
    user = g.get_user()

    github_repo_names = [repo.name for repo in user.get_repos()]

    duplicate_names = []

    for v in coding_repo_list:
        work_dir = '{}/{}'.format(repos_dir, v['project_repo_name'])
        print('go to dir: {}'.format(work_dir))
        os.chdir(work_dir)

        if v['project_repo_name'] in github_repo_names:
            duplicate_names.append(v['project_repo_name'])
            continue

        r = user.create_repo(v['project_repo_name'], description=v['repo_description'], private=True)
        github_repo_full_name = r.full_name
        print('github repo created : {}'.format(github_repo_full_name))

        os.system('git remote set-url origin git@github.com:{}.git'.format(github_repo_full_name))
        os.system('git push --set-upstream origin master')
        os.system('git push --tags')
        print('push to github OK, github repo: {}'.format(github_repo_full_name))

    print('duplicate github names: ', duplicate_names)
