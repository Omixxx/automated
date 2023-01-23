import sys
import os
import json
import subprocess
from termcolor import colored
from typing import Counter


def get_git_raw_logs(repo_path, git_log_format):
    return subprocess.run(
        f"cd {repo_path} && git log --pretty=format:'{git_log_format}'",
        shell=True, capture_output=True
    ).stdout.decode(' utf-8').splitlines()


def extract_data_from_json(data_report):
    try:
        with open(data_report, 'r') as f:
            json_data = json.load(f)
    except Exception as e:
        print(e)
        sys.exit(1)
    f.close()
    return json_data


def most_commits_dev(repo_path):
    git_logs = get_git_raw_logs(repo_path, '%an')
    return Counter(git_logs).most_common(2)


def calculate_fix_commit_percentage(data_report, repo_path):
    json_data = extract_data_from_json(data_report)
    fix_commit = len(json_data)
    total_commit = get_git_raw_logs(repo_path, '%H').__len__()
    return (fix_commit/total_commit)*100


def identify_leading_security_vulnerabilities_developer(data_report, repo_path):
    json_data = extract_data_from_json(data_report)
    leading_vulnerability_hashes = list()
    for entry in json_data:
        leading_vulnerability_hashes.extend(entry['inducing_commit_hash'])

    git_logs = get_git_raw_logs(repo_path, '%H, %an, %ae')
    relevant_logs = list(
        filter(lambda item: leading_vulnerability_hashes.__contains__(
            item.split(',')[0]), git_logs))

    logs_no_hash = list(map(lambda item: item.split(',')[1:], relevant_logs))

    # make a list of tuples so that is now hashble and can be used in Counter
    tuple_logs = list(
        map(lambda item: (item[0], item[1].strip()), logs_no_hash))

    return Counter(tuple_logs).most_common()


def main(data_report, repo_path):
    print("# Leading security vulnerabilities developer:")
    devs = identify_leading_security_vulnerabilities_developer(
        data_report, repo_path)
    for dev in devs:
        print(colored(f" {dev[0][0]}", "yellow") + colored(f" ({dev[0][1]}) ",
              "white") + colored(f"{dev[1]}", "red"))

    percentage = round(calculate_fix_commit_percentage(
        data_report, repo_path), 2)
    print("\n# " + "Percentage of fix commit: " +
          colored(f"{percentage}%", "green"))

    commits = most_commits_dev(repo_path)
    print(
        "\n# Developers who did the most number of commits:\n  " +
        colored(f"{commits[0][0]} ", "yellow") + "with " +
        colored(f"{commits[0][1]} ", "blue") + "commits\n  " +
        colored(f"{commits[1][0]} ", "yellow") + "with " +
        colored(f"{commits[1][1]} ", "blue") + "commits"

    )


if __name__ == "__main__":

    if len(sys.argv) != 3 or sys.argv[-1] == "-h":
        print(
            "usage: \npython3 pyszz_data_analyzer.py [path/to/pyszz/output.json] [path/to/git/repo]")
        sys.exit(1)
    if not os.path.exists(sys.argv[2]
                          or not os.path.isdir(sys.argv[2])
                          or not os.path.exists(sys.argv[2] + os.sep + ".git")
                          ):
        print("the path to the repository is not valid.\n" +
              " make sure is a directory and it is git initialized")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
