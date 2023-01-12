import sys
import os
import json
import subprocess


def retrive_json_data(data_report):
    try:
        with open(data_report, 'r') as f:
            json_data = json.load(f)
    except Exception as e:
        print(e)
        sys.exit(1)
    f.close()
    return json_data


def calculate_fix_commit_percentage(data_report, repo_path):
    json_data = retrive_json_data(data_report)
    fix_commit = len(json_data)
    os.chdir(repo_path)
    total_commit = len(
        subprocess.run(
            "git log --pretty=format:'%H'",
            shell=True,
            stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines())
    return (fix_commit/total_commit)*100


def identify_leading_security_vulnerabilities_developer(data_report, repo_path):
    leading_vulnerability_hashes = list()
    json_data = retrive_json_data(data_report)

    for item in json_data:
        map(lambda entry: leading_vulnerability_hashes.extend(
            entry), item['inducing_commit_hash'])

    os.chdir(repo_path)

    git_logs = subprocess.run(
        "git log --pretty=format:'%H, %an, %ae'",
        shell=True, capture_output=True
    ).stdout.decode(' utf-8').splitlines()

    return list(filter(lambda item: item.split(
        ',')[0] in leading_vulnerability_hashes, git_logs))


def main(data_report, repo_path):
    print("Percentage of fix commit: ", calculate_fix_commit_percentage(
        data_report, repo_path))
    print("Leading security vulnerabilities developer: ",
          identify_leading_security_vulnerabilities_developer(
              data_report, repo_path))


if __name__ == "__main__":

    if len(sys.argv) != 3 or sys.argv[-1] == "-h":
        print("usage: \npython3 pyszz_data_analyzer.py <path/to/pyszz/output.json>")
        sys.exit(1)
    if not os.path.exists(sys.argv[2]
                          or not os.path.isdir(sys.argv[2])
                          or not os.path.exists(sys.argv[2] + os.sep + ".git")
                          ):
        print("the path to the repository is not valid.\n" +
              " make sure is a directory and it is git initialized")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
