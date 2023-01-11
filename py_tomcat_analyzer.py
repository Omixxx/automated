from shutil import which
import os
import subprocess
import sys

GET_LOGS = "git log --pretty=format:\"hash:'%h' commit_message:'%s' auth_name:'%an' auth_email:'%ae'\""


def generate_logs(repo_path):
    output = subprocess.run(
        ['powershell.exe', f'cd {repo_path}; {GET_LOGS}'],
        stdout=subprocess.PIPE,
    )

    return output.stdout.splitlines()


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


def main(logs):

    for line in logs:
        print(f'\n\n---> {line}')

    print('fine')


if __name__ == '__main__':
    assert which('git') is not None, 'git is not installed'

    if len(sys.argv) != 2:
        print('Usage: "python3 name of the program [path_of_the_repository]"')
        sys.exit(-1)

    REPO_PATH = str(sys.argv[1])
    if not is_valid_repo(REPO_PATH):
        sys.exit(1)

    main(generate_logs(REPO_PATH))
