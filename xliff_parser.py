#!/usr/bin/env python3

import sys
import os

import untangle


report1 = "./needs-translation-report.txt"
report2 = "./needs-review-translation-report.txt"


def get_dir():
    n = len(sys.argv)
    if len(sys.argv) != 2:
        print("Wrong number of arguments. E.g. python3 xliff_parser.py /your/dir/path")
        sys.exit(1)
    dir = sys.argv[1]
    if dir != "." and os.path.isdir(dir):
        return dir
    else:
        print(f"The directory '{dir}' does not exist.")
        sys.exit(1)


def write_to_file(file_path, string_to_write):
    with open(file_path, 'a') as file:
        file.write(string_to_write)


def parse_xliff(file_path):
    needs_trans_count = 0
    needs_trans_details = ""
    needs_review_trans_count = 0
    needs_review_trans_details = ""
    with open(file_path) as file:
        doc = untangle.parse(file)
        for t in doc.xliff.file.body.transunit:
            if t['translate'] is None:
                if t.target['state'] == "needs-translation": 
                    needs_trans_count += 1
                    needs_trans_details += file_path + ": \n" + str(t) + "\n"
                if t.target['state'] == "needs-review-translation":
                    needs_review_trans_count += 1
                    needs_review_trans_details += file_path + ": \n" + str(t) + "\n"
    return file_path + ": " + str(needs_trans_count), needs_trans_details, \
            file_path + ": " + str(needs_review_trans_count), needs_review_trans_details


def traverse_dir(dir):
    needs_trans_sums = []
    needs_trans_details = []
    needs_review_trans_sums = []
    needs_review_trans_details = []
    for root, dirs, files in os.walk(dir):
        for file_name in files:
            if file_name.endswith(".xliff"):
                file_path = os.path.join(root, file_name)
                needs_trans_count, needs_trans_result, needs_review_trans_count, needs_review_trans_result = parse_xliff(file_path)
                needs_trans_sums.append(needs_trans_count)
                needs_trans_details.append(needs_trans_result)
                needs_review_trans_sums.append(needs_review_trans_count)
                needs_review_trans_details.append(needs_review_trans_result)
    write_to_file(report1, "====================Summary====================\n\n" \
            + "\n".join(needs_trans_sums))
    write_to_file(report1, "\n\n====================Details====================\n\n" \
            + "\n".join(needs_trans_details))
    write_to_file(report2, "====================Summary====================\n\n" \
            + "\n".join(needs_review_trans_sums))
    write_to_file(report2, "\n\n====================Details====================\n\n" \
            + "\n".join(needs_review_trans_details))


def remove_if_exist(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


if __name__ == "__main__":
    remove_if_exist(report1)
    remove_if_exist(report2)
    traverse_dir(get_dir())
