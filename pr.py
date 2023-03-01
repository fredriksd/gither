#! /usr/bin/env python

import argparse
import subprocess
import sys

EXECUTABLE_NAME = "pr"

class PullRequest:
    def __init__(self, branch):
        self.branch = branch
        self.description = None

    def make_description():
        editor = os.environ("EDITOR")

        if editor is None:
            print("Warning: $EDITOR is not set. Defaulting to vim...")
            editor = "vim"

        template_document = "~/pr/templates/change_description.md"

        subprocess.run([editor,]

class Branch:
    def __init__(self, branch):
        self.branch = branch
        self.main_branch = find_main_branch()
        
        if self.main_branch == None:
            raise RuntimeError(f"Could not find main branch for current repository")

    def checkout(self, branch):
        args = ["git", "checkout", branch]
        subprocess.run(args)

    def rebase(self):
        args = ["git", "rebase", "--interactive", self.main_branch]
        rebase_cmd = subprocess.run(args)

        if rebase_cmd.returncode != 0:
            raise RuntimeError(f"Could not perform rebase against "
                               f"\"{self.main_branch}\" for \"{self.branch}\"")

    def pull(self, from_main = False):
        args = ["git", "pull"]
        if from_main == True:
            self.checkout(self.main_branch)
        pull_cmd = subprocess.run(args)

        if pull_cmd.returncode != 0:
            raise RuntimeError(f"Could not perform git pull for branch \"{self.branch}\"")

        if from_main == True:
            self.checkout(self.branch)

def get_args():
    parser = argparse.ArgumentParser(
            prog = EXECUTABLE_NAME,
            description = "Convenience script to create pull requests")
    parser.add_argument("--title",
                        dest = "title",
                        required = True)

    args = parser.parse_args()
    return args

def check_for_gh():
    args = ["gh", "--version"]
    version_cmd = subprocess.run(args,
                                 capture_output = True,
                                 encoding = "UTF-8")

    if version_cmd.returncode != 0:
        raise RuntimeError(f"Failed to call \"{' '.join(args)}\"):"
                           f"{version_process.stderr}")
    print(f"Found gh: {version_cmd.stdout}")

def find_main_branch():
    args = ["git", "branch"]
    branches_cmd = subprocess.run(args,
                              capture_output = True,
                              encoding = "UTF-8")
    if branches_cmd.returncode != 0:
        raise RuntimeError(f"Failed to call \"{' '.join(args)}\":"
                           f"{branches_cmd.stderr}")

    branches = [ branch.strip(" ").strip("* ") for branch in
                branches_cmd.stdout.split("\n") ]

    for branch in branches:
        if branch == "main" or branch == "master":
            return branch;
    return None;
    
    return main_branch_re.match(branches.stdout)

def find_current_branch():
    args = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    current_branch_cmd = subprocess.run(args,
                                    capture_output = True,
                                    encoding = "UTF-8")
    return Branch(current_branch_cmd.stdout.strip())

def fail_if_branch_is_main(branch):
    if branch.branch == branch.main_branch:
        raise RuntimeError(
        """
        Branch you want to create PR to cannot be the same
        as the main / master branch!
        """)

def run(args, capture_output = False):
    cmd = subprocess.run(args,
                         capture_output = capture_output,
                         encoding = "UTF-8")

    if cmd.returncode != 0:
        raise RuntimeError(
                f"""
                Failed to call \"{" ".join(args)}\".
                stderr:
                    {cmd.stderr}
                """)

def main():
    try:
        args = get_args()
        check_for_gh()

        current_branch = find_current_branch()
        fail_if_branch_is_main(current_branch)

        print(f"Pulling from {current_branch.main_branch}...")
        current_branch.pull(from_main = True)
        print(f"Rebasing against {current_branch.main_branch}...")
        current_branch.rebase()

    except Exception as e:
        sys.exit(f"Error: {e}")

if __name__ == "__main__":
    main()
