import sys
import os
import json
import subprocess


def extract_data_from_json(data_report):
    try:
        with open(data_report, 'r') as f:
            json_data = json.load(f)
    except Exception as e:
        print(e)
        sys.exit(1)
    f.close()
    return json_data


def calculate_fix_commit_percentage(data_report, repo_path):
    json_data = extract_data_from_json(data_report)
    fix_commit = len(json_data)
    total_commit = len(
        subprocess.run(
            f"cd {repo_path} && git log --pretty=format:'%H'",
            shell=True,
            stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines())
    return (fix_commit/total_commit)*100


def identify_leading_security_vulnerabilities_developer(data_report, repo_path):
    json_data = extract_data_from_json(data_report)
    leading_vulnerability_hashes = list()
    for entry in json_data:
        leading_vulnerability_hashes.extend(entry['inducing_commit_hash'])

    git_logs = subprocess.run(
        f"cd {repo_path} && git log --pretty=format:'%H, %an, %ae'",
        shell=True, capture_output=True
    ).stdout.decode(' utf-8').splitlines()

    relevant_commits = list(
        filter(lambda item: leading_vulnerability_hashes.__contains__(
            item.split(',')[0]), git_logs))

    commits_no_hash = list(
        map(lambda item: item.split(',')[1:], relevant_commits))

    dev_bugs = dict()
    for item in commits_no_hash:
        if item[0] not in dev_bugs:
            dev_bugs.update({item[0]: 1})
            continue

        introduced_vulnerability_number = dev_bugs.get(item[0])
        assert introduced_vulnerability_number is not None
        introduced_vulnerability_number += 1
        dev_bugs.update({item[0]: introduced_vulnerability_number})

    return dev_bugs


def main(data_report, repo_path):
    print("Leading security vulnerabilities developer: ")
    devs = identify_leading_security_vulnerabilities_developer(
        data_report, repo_path)
    for dev in devs:
        print(f"{dev}: {devs.get(dev)}")

    percentage = round(calculate_fix_commit_percentage(
        data_report, repo_path), 2)
    print(f"Percentage of fix commit: {percentage}%")


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
