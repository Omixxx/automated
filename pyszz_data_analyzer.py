import sys
import json


def main(data_report):
    try:
        with open(data_report, 'r') as f:
            json_data = json.load(f)
            for item in json_data:
                print(item)
    except ValueError:
        print("file is not json format")
        sys.exit(1)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("usage: python pyszz_data_analyzer.py \
                <path/to/pyszz/output.json>")
        sys.exit(1)

    main(sys.argv[1])
