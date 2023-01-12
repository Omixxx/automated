from shutil import which
import os
import subprocess
import sys
import json

KEYWORDS = ['CVE', 'fix security']
GET_LOGS = 'git log --pretty=format:"%h, %s, %an ,%ae"'
HASH_LINE_INDEX = 0
MESSAGE_LINE_INDEX = 1
AUTHOR_LINE_INDEX = 2
AUTHOR_EMAIL_LINE_INDEX = 3


def generate_logs(repo_path):
    output = subprocess.run(
        ['powershell.exe', f'cd {repo_path}; {GET_LOGS}'], capture_output=True
    )

    return output.stdout.decode().splitlines()


def is_valid_repo(repo_path) -> bool:

    if not os.path.isdir(repo_path):
        print('not a path, please select a valid path')
        return False

    if not os.path.isdir(repo_path + os.sep + '.git'):
        print(
            'this repository is not a git repo. please use this script on git projects'
        )
        return False

    return True


def contains_keywords(line):
    for key in KEYWORDS:
        if key in str(line):
            return True


def main(logs, repo_path):
    assert logs is not None

    filtered_logs = list(filter(contains_keywords, logs))
    output = list()

    for line in filtered_logs:
        my_line = str(line).split(',')

        output.append(
            {
                'repo_name': f'{repo_path}',
                'fix_commit_hash': f'{my_line[HASH_LINE_INDEX]}',
            }
        )
    json_str = json.dumps(output, indent=4)

    with open('data.json', 'w') as f:
        f.write(json_str)


if __name__ == '__main__':
    assert which('git') is not None, 'git is not installed'

    if len(sys.argv) != 2:
        print(
            'Usage: "python3 pyszz_json_generator [path_of_the_repository] "'
        )
        sys.exit(-1)

    REPO_PATH = str(sys.argv[1])
    if not is_valid_repo(REPO_PATH):
        sys.exit(1)

    main(generate_logs(REPO_PATH), REPO_PATH)
