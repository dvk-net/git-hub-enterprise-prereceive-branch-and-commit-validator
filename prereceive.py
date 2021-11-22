#!/usr/bin/python

import sys
import fileinput
import subprocess
import re
# feature togglers

CHECK_BANCH_NAME = True
CHECK_COMMIT = True
BRANCH_SKIP_CHECK_TYPES = [
    'master',
    'development'
]
BRANCH_TYPES = [
    'feature',
    'bugfix',
    'release'
]
PROJECT_CODES = [
    'SOFA',
    'DOIT',
    'BOSCH'
]

ZERO_COMMIT = "0000000000000000000000000000000000000000"
# construct branch_name regexp
# (?:(?:feature)|(?:bug))/(?:(?:SOFA\-)|(?:DOIT\-))[0-9]+\-[a-zA-Z0-9\-]+
# <BRANCH_TYPE>/<PROJECT_CODES>-<JIRA-TIKET-ID>-short-task-description

branch_pattern = "(?:"
BRANCH_TYPES = [fr"(?:{branch_type})" for branch_type in BRANCH_TYPES ]
PROJECT_CODES = [fr"(?:{code}\-)" for code in PROJECT_CODES ]

branch_pattern += "|".join(BRANCH_TYPES) # combine all types into a string
branch_pattern += r")/"
branch_pattern += "(?:"
branch_pattern += "|".join(PROJECT_CODES) # combine all codes into a string
branch_pattern += r")"
branch_pattern += r"[0-9]+\-[a-zA-Z0-9\-]+$"


commit_message_pattern = """"""

def is_branch_name_valid(branch_ref):
    branch_name = branch_ref[11:] # exclude refs/heads/
    if branch_name in BRANCH_SKIP_CHECK_TYPES:
        return
    if not re.search(branch_pattern, branch_name):
        print(f"You branch name '{branch_name}' does not follow the required pattern - '<BRANCH_TYPE>/<PROJECT_CODES>-<JIRA-TIKET-ID>-short-task-description'")
        sys.exit(1)

def is_commit_title_valid(title):
    return

def are_commits_valid(current_hash, new_hash):
    # git rev-list 200d35e484d04f0fd9c
    if current_hash == ZERO_COMMIT:
        bash_cmd = ['git', 'rev-list', new_hash]
    else:
        bash_cmd = ['git', 'rev-list', current_hash, new_hash]
    print(bash_cmd)
    process = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    output, error = process.communicate()
    commits_list = output.decode().strip().split("\n")
    for commit in commits_list:
        # git log -1 --pretty=format:%B dd76884c317cc60b1009b27fc3727a13a879556e
        bash_cmd = ['git', 'log', "-1", "--pretty=format:%B", commit]
        process = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        output, error = process.communicate()
        commit = output.decode().strip()
        if not commit:
            print("Commit is empty")
            sys.exit(1)
        commit = commit.split("\n")
        if len(commit < 3):
            print("Commit has to contain TITLE NEW LINE BODY")
            sys.exit(1)
        for number, line in enumerate(commit, 0):
            if number == 0:
                is_commit_title_valid(line)
            if number == 1 and line != '':
                print("Second line of commit must be empty line")
                sys.exit(1)


def main():
    for line in fileinput.input():
        current_hash, new_hash, branch_name = line.strip().split(" ")
        if CHECK_BANCH_NAME:
            is_branch_name_valid(branch_name)
        if CHECK_COMMIT:
            are_commits_valid(current_hash, new_hash)
    sys.exit(1)

if __name__ == "__main__":
    main()
