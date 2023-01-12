import sys
import json


def is_json(file):
    try:
        with open(file, 'r') as f:
            json_data = json.load(f)
            if json_data:
                return True
            else:
                return False
    except ValueError:
        return False


def main(data_report):
    try:
        with open(data_report, 'r') as f:
            json_data = json.load(f)
            for item in json_data:
                print(item)
    except ValueError:
        print("something went wrong")
        sys.exit(1)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("usage: python pyszz_data_analyzer.py \
                <path/to/pyszz/output.json>")
        sys.exit(1)

    if not is_json(sys.argv[1]):
        print("error: the file is not a json file")
        sys.exit(1)

    main(sys.argv[1])
